# Desafio Técnico: Desenvolvedor Pleno | MeuAT

Bem-vindo à solução do desafio técnico para a vaga de Desenvolvedor Pleno no MeuAT. Este projeto implementa uma API REST geoespacial robusta para consultar fazendas em São Paulo usando Python, FastAPI e PostgreSQL + PostGIS.

---

## 📋 Funcionalidades Implementadas

### Obrigatórios ✅
- [x] **Stack**: Python 3.10+, FastAPI, PostgreSQL + PostGIS, Docker.
- [x] **Busca por ID**: Endpoint `GET /fazendas/{id}`.
- [x] **Busca por Ponto**: Endpoint `POST /fazendas/busca-ponto` (ST_Contains).
- [x] **Busca por Raio**: Endpoint `POST /fazendas/busca-raio` (ST_DWithin).
- [x] **Infraestrutura**: `docker-compose up` sobe tudo com seed automático.
- [x] **Documentação**: README claro e instruções de setup.

### Bônus e Diferenciais ⭐️
- [x] **Testes Automatizados**: Suíte completa com `pytest` (Unitários + Integração).
- [x] **Smoke Tests & CI**: Pipeline de verificação básica para GitHub Actions.
- [x] **Docs Interativa**: Swagger UI customizado com exemplos de payload.
- [x] **Paginação**: Implementada em todas as listagens para performance.
- [x] **Health Check**: Endpoint `/health` para monitoramento.
- [x] **Filtros Avançados**: Busca por nome (Município + Código) e área.
- [x] **Logs Estruturados**: Logging configurado para observabilidade.
- [x] **Índices Espaciais**: Uso de índices GIST para otimização de queries.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
- Docker e Docker Compose instalados.
- Git.

### 2. Download dos Dados (Importante ⚠️)
O sistema possui um seed automático, mas **você precisa fornecer os arquivos shapefile**.

1. **Baixe os dados** (Arquivo ZIP) aqui:
   👉 [**Download Google Drive**](https://drive.google.com/file/d/15ghpnwzdDhFqelouqvQwXlbzovtPhlFe/view?usp=sharing)

2. **Extraia** os arquivos (`.shp`, `.shx`, `.dbf`, `.prj`) para a pasta `seed/data/` na raiz do projeto.

A estrutura deve ficar assim:
```
meuat-teste/
├── seed/
│   └── data/             <-- COLOQUE OS ARQUIVOS AQUI
│       ├── AREA_IMOVEL_1.shp
│       ├── AREA_IMOVEL_1.shx
│       ...
├── app/
├── docker-compose.yml
└── ...
```

### 3. Configuração
Crie o arquivo de variáveis de ambiente:
```bash
cp .env.example .env
# Windows: copy .env.example .env
```
> **Dica**: Se a porta `5432` estiver em uso, altere `POSTGRES_PORT` no `.env` (ex: 5434).

### 4. Rodar
```bash
docker-compose up --build
```
A API estará disponível em **http://localhost:8000** assim que subir.

---

## 📚 Documentação da API

Acesse a documentação interativa para testar os endpoints:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Exemplos de Uso

#### 1. Buscar Fazendas por Raio
Encontra fazendas numraio de X km a partir de um ponto.

**POST** `/fazendas/busca-raio`
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "raio_km": 50
}
```

#### 2. Buscar Fazenda por Ponto
Descobre em qual fazenda um ponto específico está localizado.

**POST** `/fazendas/busca-ponto`
```json
{
  "latitude": -22.1234,
  "longitude": -47.5678
}
```

---

## 🧪 Guia de Testes

O projeto utiliza `pytest` para garantir a qualidade do código.

### 1. Smoke Tests (CI/CD)
Testes rápidos de "fumaça" que validam se a API sobe e conecta ao banco. Essenciais para pipelines de CI (como GitHub Actions).

### 2. Rodando Testes Localmente
Para rodar os testes na sua máquina, **o banco PostGIS deve estar rodando** via Docker.

1. Suba o banco:
   ```bash
   docker-compose up -d db
   ```
2. Rode os testes:
   ```bash
   pytest tests/
   ```
   *O sistema detecta automaticamente o ambiente local e ajusta a conexão.*

---

## 🏗️ Estrutura do Projeto

```
.
├── app/
│   ├── api/            # Controllers (Rotas da API)
│   ├── core/           # Configurações e Database
│   ├── models/         # Modelos SQLAlchemy (ORM)
│   ├── schemas/        # Schemas Pydantic (Validação)
│   └── services/       # Regras de Negócio e Queries Espaciais
├── seed/               # Script de carga de dados (ETL)
├── tests/              # Testes unitários e de integração
├── docker-compose.yml  # Orquestração
└── requirements.txt    # Dependências
```

---

## 📝 Decisões Técnicas

1.  **PostGIS & Índices GIST**:
    Utilizamos as funções nativas `ST_Contains` e `ST_DWithin` do PostGIS combinadas com índices GIST (`Generalized Search Tree`) na coluna `geometry`. Isso garante buscas espaciais extremamente performáticas, escalando para milhões de registros.

2.  **Convenção de Nomes**:
    O dataset geoespacial técnico não possui um "Nome Fantasia" amigável. Para contornar isso, definimos o "Nome" da fazenda como a combinação de **Município** + **Código do Imóvel**. Os filtros de busca textual atuam sobre esses dois campos.

3.  **Arquitetura em Camadas**:
    Separação clara entre Rotas, Serviços e Dados para facilitar a manutenção e testes. O controller apenas recebe a requisição, o service executa a lógica e o repositório/model acessa o banco.

---

**Desenvolvido para o Processo Seletivo MeuAT** 🚀
