from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Configurações da API
    app_name: str = "MeuAT Fazendas API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Configurações do Banco de Dados
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "meuat_fazendas"

    # Paginação
    default_page_size: int = 50
    max_page_size: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # Ignora campos extras do .env
    )

    @property
    def database_url(self) -> str:
        """Obtém URL de conexão do banco."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações."""
    return Settings()
