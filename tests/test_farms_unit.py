"""
Testes unitários para endpoints de fazendas (sem banco de dados real).
"""
from fastapi.testclient import TestClient
import pytest

pytestmark = pytest.mark.unit

from app.main import app

client = TestClient(app)


def test_search_by_point_invalid_latitude():
    """Testa busca por ponto com latitude inválida."""
    payload = {
        "latitude": 91,  # Inválido: > 90
        "longitude": -46.6333,
    }
    response = client.post("/fazendas/busca-ponto", json=payload)
    assert response.status_code == 422  # Erro de validação


def test_search_by_radius_invalid_radius():
    """Testa busca por raio com raio inválido."""
    payload = {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "raio_km": -10,  # Inválido: negativo
    }
    response = client.post("/fazendas/busca-raio", json=payload)
    assert response.status_code == 422  # Erro de validação


def test_root_endpoint():
    """Testa endpoint raiz da API."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data
