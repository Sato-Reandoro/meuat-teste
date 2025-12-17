from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, Integer, String

from app.core.db import Base


class Farm(Base):
    __tablename__ = "farms"

    ogc_fid = Column(Integer, primary_key=True, index=True)
    cod_tema = Column(String(255), nullable=True)
    nom_tema = Column(String(255), nullable=True)
    cod_imovel = Column(String(255), nullable=True, index=True)
    mod_fiscal = Column(Float, nullable=True)
    num_area = Column(Float, nullable=True, index=True)  # Área em hectares
    ind_status = Column(String(255), nullable=True)
    ind_tipo = Column(String(255), nullable=True)
    des_condic = Column(String(255), nullable=True)
    municipio = Column(String(255), nullable=True, index=True)
    cod_estado = Column(String(2), nullable=True)
    dat_criaca = Column(String(255), nullable=True)
    dat_atuali = Column(String(255), nullable=True)

    # Coluna geoespacial - armazena o polígono da fazenda
    # SRID 4326 = WGS84 (Latitude/Longitude)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=False)

    def __repr__(self) -> str:
        return f"<Farm(ogc_fid={self.ogc_fid}, cod_imovel={self.cod_imovel}, area={self.num_area})>"
