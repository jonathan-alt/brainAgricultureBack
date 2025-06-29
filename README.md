# Brain Agriculture Backend

Backend para aplicação de agricultura inteligente desenvolvido com FastAPI, PostgreSQL e Docker.

## 🚀 Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

## 📦 Instalação e Execução

### 🐳 Com Docker (Recomendado)

#### **Desenvolvimento**

1. **Clone o repositório:**

```bash
git clone <repository-url>
cd brainAgricultureBack
```

2. **Execute a aplicação:**

```bash
docker-compose -f development.yml up --build -d
```

3. **Acesse a aplicação:**

- **API**: http://localhost:${PORT:-8000}
- **Documentação Swagger**: http://localhost:${PORT:-8000}/docs
- **Documentação ReDoc**: http://localhost:${PORT:-8000}/redoc

> **Nota**: A porta padrão é 8000, mas pode ser alterada definindo a variável de ambiente `PORT`.

#### **Produção**

1. **Execute a aplicação:**

```bash
docker-compose -f production.yml up --build -d
```

2. **Acesse a aplicação:**

- **API**: http://localhost:${PORT:-8000}
- **Documentação Swagger**: http://localhost:${PORT:-8000}/docs
- **Documentação ReDoc**: http://localhost:${PORT:-8000}/redoc

> **Diferenças para produção:**
>
> - Sem `--reload` (não reinicia automaticamente)
> - `restart: unless-stopped` (reinicia automaticamente em caso de falha)
> - `ENVIRONMENT=production`

### 💻 Desenvolvimento Local

1. **Instale as dependências do sistema:**

```bash
sudo apt-get update && apt-get install -y build-essential libpq-dev gcc
```

2. **Instale as dependências Python:**

```bash
pip install -r requirements/development.txt
```

3. **Execute a aplicação:**

```bash
python start.py
```

## 🧪 Executando Testes

### 🐳 Via Docker (Recomendado)

```bash
# Todos os testes
./run_tests_docker.sh

# Apenas testes unitários
./run_tests_docker.sh -u

# Apenas testes de integração
./run_tests_docker.sh -i

# Com cobertura de código
./run_tests_docker.sh -c

# Com rebuild da imagem
./run_tests_docker.sh -c -b
```

### 💻 Via Local

```bash
# Todos os testes
pytest

# Apenas testes unitários
pytest tests/unit/

# Com cobertura
pytest --cov=app --cov-report=html
```

### 🔧 Script Inteligente

```bash
# Detecta automaticamente se usar Docker ou local
./run_tests.sh

# Forçar Docker
./run_tests.sh -d

# Forçar local
./run_tests.sh -l
```

## 📁 Estrutura do Projeto

```
brainAgricultureBack/
├── app/                           # Código da aplicação
│   ├── brain_agriculture/         # Módulo principal
│   │   ├── api/v1/               # Rotas da API
│   │   ├── models/               # Modelos do banco
│   │   ├── repositories/         # Camada de acesso a dados
│   │   ├── schemas/              # Schemas Pydantic
│   │   └── services/             # Lógica de negócio
│   ├── core/                     # Configurações core
│   └── shared/                   # Utilitários compartilhados
├── tests/                        # Testes automatizados
│   ├── unit/                     # Testes unitários
│   ├── integration/              # Testes de integração
│   └── conftest.py               # Configurações de teste
├── requirements/                 # Dependências Python
├── scripts/                      # Scripts utilitários
├── Dockerfile                    # Container da aplicação (desenvolvimento)
├── Dockerfile.prod               # Container da aplicação (produção)
├── Dockerfile.test               # Container para testes
├── development.yml               # Docker Compose para desenvolvimento
├── production.yml                # Docker Compose para produção
├── docker-compose.test.yml       # Docker Compose para testes
├── entrypoint.sh                 # Script de inicialização (produção)
├── entrypoint.dev.sh             # Script de inicialização (desenvolvimento)
├── run_tests.sh                  # Script inteligente de testes
├── run_tests_docker.sh           # Script Docker de testes
├── pyproject.toml                # Configuração Poetry
├── start.py                      # Script de inicialização
└── README.md                     # Este arquivo
```

## 🔧 Comandos Úteis

### 🐳 Docker

#### **Desenvolvimento**

```bash
# Iniciar aplicação
docker-compose -f development.yml up --build -d

# Parar aplicação
docker-compose -f development.yml down

# Ver logs
docker-compose -f development.yml logs -f

# Rebuild e reiniciar
docker-compose -f development.yml up --build --force-recreate -d
```

#### **Produção**

```bash
# Iniciar aplicação
docker-compose -f production.yml up --build -d

# Parar aplicação
docker-compose -f production.yml down

# Ver logs
docker-compose -f production.yml logs -f

# Rebuild e reiniciar
docker-compose -f production.yml up --build --force-recreate -d

# Verificar status
docker-compose -f production.yml ps
```

### 🧪 Testes

```bash
# Executar todos os testes
./run_tests_docker.sh

# Testes com cobertura
./run_tests_docker.sh -c

# Apenas testes unitários
./run_tests_docker.sh -u

# Manter containers para debug
./run_tests_docker.sh -k
```

### 💻 Desenvolvimento

```bash
# Formatar código
black .

# Ordenar imports
isort .

# Verificar linting
flake8 .

# Executar testes localmente
pytest
```

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **PostgreSQL**: Banco de dados relacional
- **SQLModel**: ORM moderno baseado em SQLAlchemy e Pydantic
- **Pydantic**: Validação de dados e serialização
- **Docker**: Containerização
- **Pytest**: Framework de testes
- **Poetry**: Gerenciamento de dependências
