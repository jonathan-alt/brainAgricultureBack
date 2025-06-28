## Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

## Instalação e Execução

### Com Docker (Recomendado)

```bash
docker-compose -f development.yml up --build -d
```

3. Acesse a aplicação:

- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

### Desenvolvimento Local

1. Instale as dependências:

```bash
sudo apt-get update && apt-get install -y build-essential libpq-dev gcc
pip install -r requirements/development.txt
```

3. Execute a aplicação:

```bash
python start.py
```

## Estrutura do Projeto

```
brainAgricultureBack/
├── app/                    # Código da aplicação
├── docker/                 # Configurações Docker
├── requirements/           # Dependências Python
├── scripts/               # Scripts utilitários
├── Dockerfile             # Container da aplicação
├── development.yml        # Docker Compose para desenvolvimento
├── entrypoint.sh          # Script de inicialização
├── pyproject.toml         # Configuração Poetry
├── start.py              # Script de inicialização
└── README.md             # Este arquivo
```

## Comandos Úteis

- Parar os containers: `docker-compose -f development.yml down`
- Ver logs: `docker-compose -f development.yml logs -f`
- Executar testes: `pytest`
- Formatar código: `black .`
- Ordenar imports: `isort .`

## Tecnologias

- **FastAPI**: Framework
- **PostgreSQL**: Banco de dados
- **SQLMODEL**: ORM para Python
- **Pydentic**: Tipificação
- **Alembic**: Migrações de banco de dados
- **Docker**: Containerização
- **Pytest**: Testes unitários
