"""
Schemas Pydantic para a API.
"""
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class PointSearchRequest(BaseModel):
    """Schema para busca por ponto."""

    latitude: float = Field(..., description="Coordenada de latitude")
    longitude: float = Field(..., description="Coordenada de longitude")

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("A latitude deve estar entre -90 e 90.")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("A longitude deve estar entre -180 e 180.")
        return v

    class Config:
        json_schema_extra = {"example": {"latitude": -23.5505, "longitude": -46.6333}}


class RadiusSearchRequest(BaseModel):
    """Schema para busca por raio."""

    latitude: float = Field(..., description="Coordenada de latitude")
    longitude: float = Field(..., description="Coordenada de longitude")
    raio_km: float = Field(..., description="Raio de busca em quilômetros")

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("A latitude deve estar entre -90 e 90.")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("A longitude deve estar entre -180 e 180.")
        return v

    @field_validator("raio_km")
    @classmethod
    def validate_radius(cls, v: float) -> float:
        if not (0 < v <= 1000):
            raise ValueError("O raio deve ser maior que 0 e até 1000km.")
        return v

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
