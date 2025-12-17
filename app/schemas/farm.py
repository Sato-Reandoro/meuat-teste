"""
Schemas Pydantic para a API.
"""
from typing import Any, Optional

from pydantic import BaseModel, Field


class PointSearchRequest(BaseModel):
    """Schema para busca por ponto."""

    latitude: float = Field(..., ge=-90, le=90, description="Coordenada de latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Coordenada de longitude")

    class Config:
        json_schema_extra = {"example": {"latitude": -23.5505, "longitude": -46.6333}}


class RadiusSearchRequest(BaseModel):
    """Schema para busca por raio."""

    latitude: float = Field(..., ge=-90, le=90, description="Coordenada de latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Coordenada de longitude")
    raio_km: float = Field(..., gt=0, le=1000, description="Raio de busca em quilômetros")

    class Config:
        json_schema_extra = {
            "example": {"latitude": -23.5505, "longitude": -46.6333, "raio_km": 50}
        }


class FarmBase(BaseModel):
    """Schema base da fazenda."""

    cod_imovel: Optional[str] = None
    num_area: Optional[float] = None
    municipio: Optional[str] = None
    cod_estado: Optional[str] = "SP"


class FarmResponse(FarmBase):
    """Schema de resposta da fazenda."""

    ogc_fid: int
    cod_tema: Optional[str] = None
    nom_tema: Optional[str] = None
    mod_fiscal: Optional[float] = None
    ind_status: Optional[str] = None
    ind_tipo: Optional[str] = None
    des_condic: Optional[str] = None
    dat_criaca: Optional[str] = None
    dat_atuali: Optional[str] = None
    geometry: Optional[dict[str, Any]] = None  # GeoJSON

    class Config:
        from_attributes = True


class FarmListResponse(BaseModel):
    """Resposta paginada da lista de fazendas."""

    total: int
    page: int
    page_size: int
    farms: list[FarmResponse]


class HealthResponse(BaseModel):
    """Resposta do health check."""

    status: str
    database: str
    version: str
