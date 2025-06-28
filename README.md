# Brain Agriculture Backend

Backend para aplicação de agricultura inteligente desenvolvido com FastAPI, PostgreSQL e Docker.

## 🚀 Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

## 📦 Instalação e Execução

### 🐳 Com Docker (Recomendado)

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

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

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
├── Dockerfile                    # Container da aplicação
├── Dockerfile.test               # Container para testes
├── development.yml               # Docker Compose para desenvolvimento
├── docker-compose.test.yml       # Docker Compose para testes
├── entrypoint.sh                 # Script de inicialização
├── run_tests.sh                  # Script inteligente de testes
├── run_tests_docker.sh           # Script Docker de testes
├── pyproject.toml                # Configuração Poetry
├── start.py                      # Script de inicialização
└── README.md                     # Este arquivo
```

## 🔧 Comandos Úteis

### 🐳 Docker

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

## 📊 API Endpoints

### Produtores

- `GET /api/v1/produtores` - Listar todos os produtores
- `GET /api/v1/produtores/{id}` - Buscar produtor por ID
- `POST /api/v1/produtores` - Criar novo produtor
- `PUT /api/v1/produtores/{id}` - Atualizar produtor
- `DELETE /api/v1/produtores/{id}` - Excluir produtor
- `GET /api/v1/produtores/lista` - Lista resumida (ID e nome)
- `GET /api/v1/produtores/{produtor_id}/fazendas` - Fazendas de um produtor

### Fazendas

- `GET /api/v1/fazendas` - Listar todas as fazendas
- `GET /api/v1/fazendas/{id}` - Buscar fazenda por ID
- `POST /api/v1/fazendas` - Criar nova fazenda
- `PUT /api/v1/fazendas/{id}` - Atualizar fazenda
- `DELETE /api/v1/fazendas/{id}` - Excluir fazenda
- `GET /api/v1/fazendas/lista` - Lista resumida (ID e nome)
- `GET /api/v1/fazendas/estatisticas` - Estatísticas por estado
- `GET /api/v1/fazendas/estatisticas-areas` - Estatísticas de áreas
- `GET /api/v1/fazendas/resumo` - Resumo (total e área)
- `GET /api/v1/fazendas/{fazenda_id}/safras` - Safras de uma fazenda

### Safras

- `GET /api/v1/safras` - Listar todas as safras
- `GET /api/v1/safras/{id}` - Buscar safra por ID
- `POST /api/v1/safras` - Criar nova safra
- `PUT /api/v1/safras/{id}` - Atualizar safra
- `DELETE /api/v1/safras/{id}` - Excluir safra
- `GET /api/v1/safras/estatisticas-culturas` - Estatísticas de culturas
- `GET /api/v1/safras/ano/{ano}` - Safras por ano específico

### Dados Específicos

- `GET /api/v1/fazendas/{fazenda}/dados` - Dados específicos de uma fazenda

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **PostgreSQL**: Banco de dados relacional
- **SQLModel**: ORM moderno baseado em SQLAlchemy e Pydantic
- **Pydantic**: Validação de dados e serialização
- **Docker**: Containerização
- **Pytest**: Framework de testes
- **Poetry**: Gerenciamento de dependências

## 🔍 Debugging

### Logs da Aplicação

```bash
# Ver logs em tempo real
docker-compose -f development.yml logs -f app

# Ver logs de erro
docker-compose -f development.yml logs app | grep ERROR
```

### Banco de Dados

```bash
# Conectar ao banco
docker-compose -f development.yml exec db psql -U postgres -d brain_agriculture

# Ver tabelas
\dt

# Ver dados
SELECT * FROM produtor LIMIT 5;
```

### Testes

```bash
# Manter containers para debug
./run_tests_docker.sh -k

# Ver logs dos testes
docker-compose -f docker-compose.test.yml logs test-app
```

## 🚀 Deploy

Para produção, use o arquivo `deploy_conf.py` e configure as variáveis de ambiente apropriadas.

## 📝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
