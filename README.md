# MeuAT Fazendas API 🌾

API REST para busca de fazendas por localização geográfica usando Python, FastAPI e PostgreSQL com PostGIS.

## 🚀 Início Rápido

### Pré-requisitos
- Docker
- Docker Compose
- Arquivos shapefile das fazendas (`.shp`, `.shx`, `.dbf`, `.prj`)

### Como Executar

1. **Clone o repositório**
```bash
git clone <repository-url>
cd meuat
```

2. **Adicione os dados shapefile**

Coloque os arquivos shapefile na pasta `seed/data/`:
```
seed/data/
├── AREA_IMOVEL_1.shp
├── AREA_IMOVEL_1.shx
├── AREA_IMOVEL_1.dbf
└── AREA_IMOVEL_1.prj
```

3. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto (copie de `.env.example`):
```bash
cp .env.example .env
```

**Importante**: Se você já tem PostgreSQL instalado na porta 5432, ajuste `DB_HOST_PORT` no `.env` para outra porta (ex: 5434).

4. **Inicie a aplicação**
```bash
docker-compose up --build
```

Pronto! 🎉 A API estará rodando em `http://localhost:8000`

Os dados serão carregados automaticamente no banco de dados.

## 📚 Documentação da API

Acesse a documentação interativa em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### Health Check
```http
GET /health
```
Verifica o status da API e conexão com o banco de dados.

### Buscar Fazenda por ID
```http
GET /fazendas/{id}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Fazenda Exemplo",
  "area_hectares": 150.5,
  "municipality": "Ribeirão Preto",
  "state": "SP",
  "geometry": { ... }
}
```

### Buscar Fazendas por Ponto
```http
POST /fazendas/busca-ponto
```

**Body:**
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333
}
```

Retorna fazendas que contêm o ponto especificado (usando `ST_Contains`).

### Buscar Fazendas por Raio
```http
POST /fazendas/busca-raio
```

**Body:**
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "raio_km": 50
}
```

**Query Parameters (opcionais):**
- `page`: Número da página (padrão: 1)
- `page_size`: Resultados por página (padrão: 50, máximo: 100)
- `name`: Filtrar por nome da fazenda
- `min_area`: Área mínima em hectares
- `max_area`: Área máxima em hectares

Retorna fazendas dentro do raio especificado (usando `ST_DWithin`).

## 🏗️ Arquitetura

```
meuat/
├── app/                    # Aplicação FastAPI
│   ├── api/               # Endpoints da API
│   ├── core/              # Configurações e database
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Schemas Pydantic
│   └── services/          # Lógica de negócio
├── seed/                  # Sistema de seed
│   ├── data/             # Dados shapefile
│   └── load_shapefiles.py
├── tests/                 # Testes automatizados
└── docker-compose.yml     # Orquestração Docker
```

## 🧪 Testes

### Executar testes localmente
```bash
pip install -r requirements.txt
pytest tests/ -v --cov=app
```

### Executar testes no Docker
```bash
docker-compose run --rm api pytest tests/ -v
```

## 🔍 Recursos Implementados

### Obrigatórios ✅
- ✅ Python 3.11 + FastAPI
- ✅ PostgreSQL com PostGIS
- ✅ Docker + Docker Compose
- ✅ Endpoint `GET /fazendas/{id}`
- ✅ Endpoint `POST /fazendas/busca-ponto`
- ✅ Endpoint `POST /fazendas/busca-raio`
- ✅ Seed automático ao iniciar containers
- ✅ README com instruções

### Bônus Implementados 🌟
- ✅ **Testes automatizados** - pytest com smoke tests
- ✅ **Documentação Swagger** - customizada com exemplos
- ✅ **Paginação** - em todos os endpoints de busca
- ✅ **Health check** - `GET /health`
- ✅ **CI básico** - GitHub Actions com lint e testes
- ✅ **Filtros adicionais** - nome, área mínima/máxima
- ✅ **Índices espaciais** - GIST index no campo geometry
- ✅ **Logs estruturados** - JSON structured logging

## 🛠️ Desenvolvimento

### Configuração do ambiente local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Lint e formatação
```bash
# Verificar código
ruff check app/ tests/

# Formatar código
ruff format app/ tests/
```

### Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário:

```bash
cp .env.example .env
```

## 📊 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL + PostGIS** - Banco de dados com extensão geoespacial
- **SQLAlchemy** - ORM Python
- **GeoAlchemy2** - Extensão do SQLAlchemy para tipos geoespaciais
- **Pydantic** - Validação de dados
- **Docker** - Containerização
- **Pytest** - Framework de testes
- **Ruff** - Linter e formatter Python
- **GitHub Actions** - CI/CD

## 🗺️ PostGIS - Operações Espaciais

A API utiliza as seguintes funções PostGIS:

- **ST_Contains**: Verifica se um ponto está dentro de um polígono
- **ST_DWithin**: Encontra geometrias dentro de uma distância específica
- **ST_AsGeoJSON**: Converte geometrias para formato GeoJSON
- **ST_Transform**: Transforma coordenadas entre sistemas de referência

## 📝 Notas Técnicas

- **SRID 4326**: Sistema de coordenadas WGS84 (GPS)
- **Índices GIST**: Otimizam queries espaciais
- **Paginação**: Previne sobrecarga com grandes datasets
- **Logs estruturados**: Facilitam monitoramento em produção

## 🐛 Troubleshooting

### Seed não carrega os dados
Verifique se os arquivos shapefile estão na pasta `seed/data/`:
```bash
ls -la seed/data/
```

### Erro de conexão com banco de dados
Aguarde o banco estar pronto. O health check deve retornar:
```bash
curl http://localhost:8000/health
```

### Resetar banco de dados
```bash
docker-compose down -v
docker-compose up --build
```

## 📄 Licença

Este projeto foi desenvolvido como parte de um desafio técnico para a vaga de Desenvolvedor Pleno no MeuAT.

---

**Desenvolvido com ❤️ para o MeuAT**
