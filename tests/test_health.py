"""
Testes para health check endpoint.
"""
from fastapi.testclient import TestClient
import pytest

pytestmark = [pytest.mark.smoke, pytest.mark.integration]

from app.main import app

client = TestClient(app)


def test_health_endpoint_structure():
    """Testa que o endpoint health retorna a estrutura correta."""
    response = client.get("/health")

    # Aceita tanto 200 (banco OK) quanto 503 (banco não disponível)
    assert response.status_code in [200, 503]

    data = response.json()

    # Se status 200, verifica estrutura de sucesso
    if response.status_code == 200:
        assert "status" in data
        assert "database" in data
        assert "version" in data
    # Se status 503, verifica que tem mensagem de erro
    else:
        assert "detail" in data
