"""
Farm API endpoints.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.logging import get_logger
from app.schemas.farm import FarmListResponse, FarmResponse, PointSearchRequest, RadiusSearchRequest
from app.services.farm_queries import FarmQueryService

logger = get_logger(__name__)
router = APIRouter()
settings = get_settings()


def _build_farm_response(farm, db: Session) -> FarmResponse:
    """Helper para montar a resposta da fazenda com geometria GeoJSON."""
    geojson = FarmQueryService.farm_to_geojson(farm, db)
    return FarmResponse(
        ogc_fid=farm.ogc_fid,
        cod_imovel=farm.cod_imovel,
        num_area=farm.num_area,
        municipio=farm.municipio,
        cod_estado=farm.cod_estado,
        cod_tema=farm.cod_tema,
        nom_tema=farm.nom_tema,
        mod_fiscal=farm.mod_fiscal,
        ind_status=farm.ind_status,
        ind_tipo=farm.ind_tipo,
        des_condic=farm.des_condic,
        dat_criaca=farm.dat_criaca,
        dat_atuali=farm.dat_atuali,
        geometry=geojson,
    )


@router.get("/fazendas/{farm_id}", response_model=FarmResponse, tags=["Fazendas"])
async def get_farm(farm_id: int, db: Session = Depends(get_db)):
    """
    Busca uma fazenda específica por ID.

    Args:
        farm_id: ID da fazenda

    Returns:
        Detalhes da fazenda com geometria em formato GeoJSON
    """
    logger.info(f"GET /fazendas/{farm_id}")

    service = FarmQueryService(db)
    farm = service.get_farm_by_id(farm_id)

    if not farm:
        logger.warning(f"Farm {farm_id} not found")
        raise HTTPException(status_code=404, detail="Farm not found")

    return _build_farm_response(farm, db)


@router.post("/fazendas/busca-ponto", response_model=FarmListResponse, tags=["Fazendas"])
async def search_by_point(
    request: PointSearchRequest,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Resultados por página"),
    db: Session = Depends(get_db),
):
    """
    Busca fazendas que contêm um ponto específico.

    Utiliza PostGIS ST_Contains para encontrar fazendas cujo polígono contém as coordenadas informadas.

    Args:
        request: Coordenadas do ponto (latitude, longitude)
        page: Número da página para paginação
        page_size: Quantidade de resultados por página

    Returns:
        Lista de fazendas que contêm o ponto
    """
    logger.info(f"POST /fazendas/busca-ponto - lat: {request.latitude}, lon: {request.longitude}")

    service = FarmQueryService(db)
    farms, total = service.search_by_point(
        latitude=request.latitude,
        longitude=request.longitude,
        page=page,
        page_size=min(page_size, settings.max_page_size),
    )

    farm_responses = [_build_farm_response(farm, db) for farm in farms]

    return FarmListResponse(total=total, page=page, page_size=page_size, farms=farm_responses)


@router.post("/fazendas/busca-raio", response_model=FarmListResponse, tags=["Fazendas"])
async def search_by_radius(
    request: RadiusSearchRequest,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Resultados por página"),
    name: Optional[str] = Query(None, description="Filtrar por nome da fazenda (busca parcial)"),
    min_area: Optional[float] = Query(None, ge=0, description="Área mínima em hectares"),
    max_area: Optional[float] = Query(None, ge=0, description="Área máxima em hectares"),
    db: Session = Depends(get_db),
):
    """
    Busca fazendas dentro de um raio a partir de um ponto.

    Utiliza PostGIS ST_DWithin para encontrar fazendas dentro da distância especificada.

    Args:
        request: Coordenadas do ponto e raio de busca em quilômetros
        page: Número da página para paginação
        page_size: Quantidade de resultados por página
        name: Filtro opcional de nome (busca parcial)
        min_area: Filtro opcional de área mínima
        max_area: Filtro opcional de área máxima

    Returns:
        Lista de fazendas dentro do raio especificado
    """
    logger.info(
        f"POST /fazendas/busca-raio - lat: {request.latitude}, "
        f"lon: {request.longitude}, radius: {request.raio_km}km"
    )

    service = FarmQueryService(db)
    farms, total = service.search_by_radius(
        latitude=request.latitude,
        longitude=request.longitude,
        radius_km=request.raio_km,
        page=page,
        page_size=min(page_size, settings.max_page_size),
        name_filter=name,
        min_area=min_area,
        max_area=max_area,
    )

    farm_responses = [_build_farm_response(farm, db) for farm in farms]

    return FarmListResponse(total=total, page=page, page_size=page_size, farms=farm_responses)
