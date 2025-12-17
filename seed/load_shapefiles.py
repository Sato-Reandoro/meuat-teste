import logging
import os
import sys
import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configura logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def wait_for_db(host, port, user, password, database, max_retries=30):
    """Aguarda o banco de dados estar pronto."""
    logger.info(f"Aguardando banco {database} em {host}:{port}...")

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, database=database
            )
            conn.close()
            logger.info("Banco de dados pronto!")
            return True
        except psycopg2.OperationalError:
            logger.info(f"Tentativa {i+1}/{max_retries}: Banco ainda não está pronto...")
            time.sleep(2)

    logger.error("Tempo limite de espera do banco excedido")
    return False


def setup_database(host, port, user, password, database):
    """Configura banco com extensão PostGIS."""
    logger.info("Configurando banco de dados...")

    try:
        # Conecta ao banco
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Habilita extensão PostGIS
        logger.info("Habilitando extensão PostGIS...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

        cur.close()
        conn.close()
        logger.info("Configuração do banco concluída com sucesso")
        return True

    except Exception as e:
        logger.error(f"Erro ao configurar banco: {e}")
        return False


def load_shapefile(host, port, user, password, database, shapefile_path):
    """Carrega shapefile no banco usando ogr2ogr."""
    logger.info(f"Carregando shapefile: {shapefile_path}")

    # Monta comando ogr2ogr
    # -f PostgreSQL: formato de saída
    # -nln farms: nome da tabela
    # -nlt PROMOTE_TO_MULTI: promove geometria para MULTI*
    # -lco GEOMETRY_NAME=geometry: nome da coluna de geometria
    # -lco SPATIAL_INDEX=GIST: cria índice espacial GIST

    pg_connection = f"PG:host={host} port={port} dbname={database} user={user} password={password}"

    cmd = [
        "ogr2ogr",
        "-f",
        "PostgreSQL",
        pg_connection,
        shapefile_path,
        "-nln",
        "farms",
        "-nlt",
        "PROMOTE_TO_MULTI",
        "-lco",
        "GEOMETRY_NAME=geometry",
        "-lco",
        "PRECISION=NO",  # Evita overflow de campos numéricos
        "-t_srs",
        "EPSG:4326",
        "-overwrite",  # Sobrescreve se existir
    ]

    logger.info(f"Executando: {' '.join(cmd)}")

    import subprocess

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info("Shapefile carregado com sucesso")
        logger.debug(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao carregar shapefile: {e}")
        logger.error(f"stdout: {e.stdout}")
        logger.error(f"stderr: {e.stderr}")
        return False


def post_process_data(host, port, user, password, database):
    """Pós-processamento para adicionar índices."""
    logger.info("Pós-processando dados...")

    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Cria índice espacial se não existir
        logger.info("Garantindo índice espacial...")
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS farms_geometry_idx
            ON farms USING GIST (geometry);
        """
        )

        # Índice em municipio
        logger.info("Criando índice de município...")
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS farms_municipio_idx
            ON farms (municipio);
        """
        )

        # Índice em num_area
        logger.info("Criando índice de área...")
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS farms_num_area_idx
            ON farms (num_area);
        """
        )

        # Índice em cod_imovel
        logger.info("Criando índice de cod_imovel...")
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS farms_cod_imovel_idx
            ON farms (cod_imovel);
        """
        )

        cur.close()
        conn.close()

        logger.info("Pós-processamento concluído")
        return True

    except Exception as e:
        logger.error(f"Erro no pós-processamento: {e}")
        return False


def main():
    """Função principal de seed."""
    # Obtém credenciais do ambiente
    db_host = os.getenv("POSTGRES_HOST", "db")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = os.getenv("POSTGRES_DB", "meuat_fazendas")

    # Caminho do Shapefile
    data_dir = "/seed/data"
    shapefile_name = "AREA_IMOVEL_1.shp"
    shapefile_path = os.path.join(data_dir, shapefile_name)

    logger.info("Iniciando processo de seed...")
    logger.info(f"Banco: {db_host}:{db_port}/{db_name}")
    logger.info(f"Shapefile: {shapefile_path}")

    # Verifica se shapefile existe
    if not os.path.exists(shapefile_path):
        logger.error(f"Shapefile não encontrado: {shapefile_path}")
        logger.error("Verifique se o volume de dados está montado em /seed/data")
        sys.exit(1)

    # Aguarda banco
    if not wait_for_db(db_host, db_port, db_user, db_password, db_name):
        logger.error("Não foi possível conectar ao banco")
        sys.exit(1)

    # Setup banco
    if not setup_database(db_host, db_port, db_user, db_password, db_name):
        logger.error("Falha ao configurar banco")
        sys.exit(1)

    # Carrega shapefile
    if not load_shapefile(db_host, db_port, db_user, db_password, db_name, shapefile_path):
        logger.error("Falha ao carregar shapefile")
        sys.exit(1)

    # Pós-processamento
    if not post_process_data(db_host, db_port, db_user, db_password, db_name):
        logger.warning("Pós-processamento teve problemas, mas continuando...")

    logger.info("Processo de seed concluído com sucesso!")


if __name__ == "__main__":
    main()
