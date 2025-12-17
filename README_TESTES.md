# Guia de Testes

## Rodando os Testes

### Testes Unitários (sem banco de dados)
Testes rápidos que NÃO precisam de conexão com banco:

```bash
pytest tests/test_farms_unit.py tests/test_health.py -v
```

✅ **5 testes passando**

### Testes de Integração (com banco de dados)
Testes que usam o banco de dados Docker:

#### Pré-requisito: Docker rodando
```bash
docker ps
# Deve mostrar: meuat_api e meuat_postgis
```

#### Rodando os testes
```bash
pytest tests/test_farms_smoke.py -v
```

**✨ Configuração automática:** Os testes já estão configurados para conectar em `localhost:5434` automaticamente (onde o Docker expõe o banco). Você não precisa configurar nada!

### Todos os Testes
```bash
pytest tests/ -v
```

### Com Coverage
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Como Funciona

- **Aplicação no Docker**: Usa `POSTGRES_HOST=db` (rede interna do Docker)
- **Testes locais**: Automaticamente usam `POSTGRES_HOST=localhost` e porta `5434`

A configuração é feita automaticamente pelo arquivo `tests/conftest.py` 🎯
