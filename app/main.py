from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import farms, health
from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()

# Configura logs
setup_logging(level="DEBUG" if settings.debug else "INFO")

# Cria aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API para busca de fazendas por localização geográfica usando PostGIS.

    ## Funcionalidades

    * **Busca por ID** - Obtém dados de uma fazenda específica
    * **Busca por Ponto** - Encontra fazendas que contêm um ponto específico
    * **Busca por Raio** - Encontra fazendas dentro de um raio a partir de um ponto
    * **Health Check** - Verifica status da API e conexão com banco de dados

    ## Tecnologias

    * FastAPI
    * PostgreSQL + PostGIS
    * SQLAlchemy + GeoAlchemy2
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas
app.include_router(health.router)
app.include_router(farms.router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }
