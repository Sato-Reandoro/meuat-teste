"""
Serviço de consultas de fazendas com operações espaciais PostGIS.
"""
import json
from typing import Optional

from geoalchemy2.functions import ST_Covers
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.farm import Farm

logger = get_logger(__name__)


class FarmQueryService:
    """Executa consultas espaciais de fazendas."""

    def __init__(self, db: Session):
        self.db = db

    def get_farm_by_id(self, farm_id: int) -> Optional[Farm]:
        """Busca fazenda por ID (ogc_fid)."""
        logger.info(f"Buscando fazenda ID: {farm_id}")
        return self.db.query(Farm).filter(Farm.cod_imovel == farm_id).first()

    def search_by_point(
        self,
        latitude: float,
        longitude: float,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[Farm], int]:
        """
        Busca fazendas contendo o ponto (ST_Covers).
        Retorna (lista_fazendas, total).
        """
        logger.info(f"Buscando fazendas contendo ponto: ({latitude}, {longitude})")

        # Ponto em WGS84 (SRID 4326). Ordem correta: (lon, lat)
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

        query = self.db.query(Farm).filter(ST_Covers(Farm.geometry, point))

        total = query.count()

        offset = (page - 1) * page_size
        farms = query.offset(offset).limit(page_size).all()

        logger.info(f"Encontradas {total} fazendas contendo o ponto")
        return farms, total

    def search_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
        page: int = 1,
        page_size: int = 50,
        name_filter: Optional[str] = None,
        min_area: Optional[float] = None,
        max_area: Optional[float] = None,
    ) -> tuple[list[Farm], int]:
        logger.info(
            f"Buscando fazendas num raio de {radius_km}km do ponto: ({latitude}, {longitude})"
        )

        # Ponto em WGS84 (SRID 4326)
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

        # Converte km para metros (ST_DWithin em geography usa metros)
        radius_m = radius_km * 1000

        # ST_DWithin usando geography para distância real (metros)
        query = self.db.query(Farm).filter(
            func.ST_DWithin(
                func.Geography(Farm.geometry),
                func.Geography(point),
                radius_m,
            )
        )

        # Filtros opcionais
        if name_filter:
            query = query.filter(
                (Farm.cod_imovel.ilike(f"%{name_filter}%"))
                | (Farm.municipio.ilike(f"%{name_filter}%"))
            )

        if min_area is not None:
            query = query.filter(Farm.num_area >= min_area)

        if max_area is not None:
            query = query.filter(Farm.num_area <= max_area)

        total = query.count()

        offset = (page - 1) * page_size
        farms = query.offset(offset).limit(page_size).all()

        logger.info(f"Encontradas {total} fazendas no raio de {radius_km}km")
        return farms, total

    @staticmethod
    def farm_to_geojson(farm: Farm, db: Session) -> dict | None:
        """Converte geometria da fazenda para GeoJSON."""
        if not farm.geometry:
            return None

        geojson_str = db.scalar(func.ST_AsGeoJSON(farm.geometry))
        return json.loads(geojson_str) if geojson_str else None
