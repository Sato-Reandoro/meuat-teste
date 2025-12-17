import logging
import pytest

from fastapi.testclient import TestClient

from app.main import app

# Aplica marcador smoke para todos os testes neste arquivo
pytestmark = pytest.mark.smoke

# Configura logger para os testes
logger = logging.getLogger(__name__)

client = TestClient(app)


def test_get_farm_not_found():
    """Teste: Buscar fazenda inexistente retorna 404."""
    farm_id = 999999
    logger.info(f"Testando busca de fazenda inexistente: ID {farm_id}")

    response = client.get(f"/fazendas/{farm_id}")

    logger.info(f"Status code recebido: {response.status_code}")
    assert response.status_code == 404


def test_search_by_point_valid_request():
    """Teste: Busca por ponto com coordenadas válidas."""
    logger.info("Testando busca por ponto com coordenadas válidas")
    payload = {"latitude": -23.5505, "longitude": -46.6333}
    logger.info(f"Payload enviado: {payload}")

    response = client.post("/fazendas/busca-ponto", json=payload)

    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    logger.info(f"Total de fazendas encontradas: {data.get('total')}")

    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "farms" in data
    assert isinstance(data["farms"], list)


def test_search_by_point_invalid_latitude():
    """Teste: Busca por ponto com latitude inválida (>90)."""
    logger.info("Testando busca por ponto com latitude inválida (>90)")
    payload = {
        "latitude": 91,  # Inválido: maior que 90
        "longitude": -46.6333,
    }
    logger.info(f"Payload enviado: {payload}")

    response = client.post("/fazendas/busca-ponto", json=payload)

    logger.info(f"Status code esperado: 422, Recebido: {response.status_code}")
    assert response.status_code == 422


def test_search_by_radius_valid_request():
    """Teste: Busca por raio com parâmetros válidos."""
    logger.info("Testando busca por raio com parâmetros válidos")
    payload = {"latitude": -23.5505, "longitude": -46.6333, "raio_km": 50}
    logger.info(f"Payload enviado: {payload}")

    response = client.post("/fazendas/busca-raio", json=payload)

    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    logger.info(f"Total de fazendas encontradas no raio de 50km: {data.get('total')}")

    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "farms" in data
    assert isinstance(data["farms"], list)


def test_search_by_radius_invalid_radius():
    """Teste: Busca por raio inválido (negativo)."""
    logger.info("Testando busca por raio com raio negativo")
    payload = {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "raio_km": -10,  # Inválido: negativo
    }
    logger.info(f"Payload enviado: {payload}")

    response = client.post("/fazendas/busca-raio", json=payload)

    logger.info(f"Status code esperado: 422, Recebido: {response.status_code}")
    assert response.status_code == 422


def test_search_by_radius_with_pagination():
    """Teste: Busca por raio com paginação."""
    logger.info("Testando busca por raio com paginação (page=1, page_size=10)")
    payload = {"latitude": -23.5505, "longitude": -46.6333, "raio_km": 100}

    response = client.post("/fazendas/busca-raio?page=1&page_size=10", json=payload)

    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    logger.info(f"Página retornada: {data.get('page')}")
    logger.info(f"Tamanho da página: {data.get('page_size')}")

    assert data["page"] == 1
    assert data["page_size"] == 10
