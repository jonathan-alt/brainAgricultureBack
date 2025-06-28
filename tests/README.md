# Testes do Brain Agriculture Backend

Este diretório contém todos os testes automatizados para o projeto Brain Agriculture Backend.

## 📁 Estrutura

```
tests/
├── conftest.py              # Configurações e fixtures compartilhadas
├── unit/                    # Testes unitários
│   ├── test_repository.py   # Testes do repositório
│   └── test_service.py      # Testes do service
├── integration/             # Testes de integração
│   └── test_routes.py       # Testes das rotas da API
└── README.md               # Esta documentação
```

## 🧪 Tipos de Testes

### Testes Unitários (`tests/unit/`)

- **Objetivo**: Testar componentes isoladamente
- **Cobertura**: Repositório, Service, Schemas
- **Características**: Rápidos, com mocks, sem dependências externas

### Testes de Integração (`tests/integration/`)

- **Objetivo**: Testar a integração entre componentes
- **Cobertura**: Rotas da API, fluxos completos
- **Características**: Mais lentos, testam comportamento real

## 🚀 Como Executar:

```bash
# Executa automaticamente via Docker se disponível, senão localmente
./run_tests.sh

# Forçar execução via Docker
./run_tests.sh -d

# Forçar execução local
./run_tests.sh -l

# Apenas testes unitários via Docker
./run_tests.sh -d -u

# Com cobertura via Docker
./run_tests.sh -d -c
```

#### Script Específico para Docker

```bash
# Executar todos os testes via Docker
./run_tests_docker.sh

# Apenas testes unitários
./run_tests_docker.sh -u

# Apenas testes de integração
./run_tests_docker.sh -i

# Com cobertura e rebuild da imagem
./run_tests_docker.sh -c -b

# Manter containers para inspeção
./run_tests_docker.sh -k
```

#### Docker Compose Direto

```bash
# Todos os testes
docker-compose -f docker-compose.test.yml --profile test up test-app

# Apenas testes unitários
docker-compose -f docker-compose.test.yml --profile test up test-app-unit

# Apenas testes de integração
docker-compose -f docker-compose.test.yml --profile test up test-app-integration

# Com rebuild
docker-compose -f docker-compose.test.yml --profile test up --build test-app
```

### 💻 Execução Local

```bash
# Todos os testes
pytest

# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/

# Com cobertura
pytest --cov=app --cov-report=html

# Verboso
pytest -v

# Parar no primeiro erro
pytest -x
```

## 🐳 Configuração Docker

### Arquivos Docker

- **`Dockerfile.test`**: Imagem específica para testes
- **`docker-compose.test.yml`**: Configuração de serviços para testes
- **`run_tests_docker.sh`**: Script específico para Docker

### Serviços Disponíveis

- **`test-app`**: Todos os testes (com banco de dados)
- **`test-app-unit`**: Apenas testes unitários (sem banco)
- **`test-app-integration`**: Apenas testes de integração (com banco)
- **`test-db`**: Banco de dados PostgreSQL para testes

### Variáveis de Ambiente

```bash
ENVIRONMENT=test
DATABASE_URL=postgresql://test_user:test_password@test-db:5432/brain_agriculture_test
PYTHONPATH=/app
```

## 📊 Cobertura de Código

### Via Docker

```bash
# Com relatório HTML
./run_tests_docker.sh -c

# Para acessar o relatório HTML do container
docker cp $(docker ps -q --filter "ancestor=brain-agriculture-back-test-app"):/app/htmlcov ./htmlcov
```

### Via Local

```bash
pytest --cov=app --cov-report=html
```

O relatório será gerado em:

- **Terminal**: Mostra linhas não cobertas
- **HTML**: `htmlcov/index.html` (abrir no navegador)

## 🔧 Configuração

### Dependências

As dependências de teste estão em `requirements/development.txt`:

- `pytest`: Framework de testes
- `pytest-asyncio`: Suporte a testes assíncronos
- `httpx`: Cliente HTTP para testes de API
- `pytest-cov`: Cobertura de código

### Configuração do pytest

O arquivo `pytest.ini` contém as configurações:

- Diretório de testes: `tests/`
- Padrão de arquivos: `test_*.py`
- Modo assíncrono: `auto`
- Marcadores: `unit`, `integration`, `slow`

## 📝 Escrevendo Novos Testes

### Teste Unitário

```python
import pytest
from unittest.mock import Mock

def test_meu_metodo_success():
    """Testa meu método com sucesso"""
    # Arrange
    mock_dependency = Mock()
    mock_dependency.method.return_value = "resultado"

    # Act
    result = minha_funcao(mock_dependency)

    # Assert
    assert result == "resultado esperado"
    mock_dependency.method.assert_called_once()
```

### Teste de Integração

```python
import pytest
from fastapi.testclient import TestClient

def test_minha_rota_success(client):
    """Testa minha rota com sucesso"""
    response = client.get("/api/v1/minha-rota")

    assert response.status_code == 200
    data = response.json()
    assert "campo" in data
```

### Fixtures Disponíveis

Veja `conftest.py` para todas as fixtures:

- `sample_produtor`: Dados de exemplo de produtor
- `sample_fazenda`: Dados de exemplo de fazenda
- `sample_safra`: Dados de exemplo de safra
- `mock_repository_methods`: Mock dos métodos do repositório
- `client`: Cliente de teste FastAPI

## 🏷️ Marcadores

Use marcadores para organizar e filtrar testes:

```python
@pytest.mark.unit
def test_unitario():
    pass

@pytest.mark.integration
def test_integracao():
    pass

@pytest.mark.slow
def test_lento():
    pass
```

Executar por marcador:

```bash
pytest -m unit          # Apenas testes unitários
pytest -m integration   # Apenas testes de integração
pytest -m "not slow"    # Excluir testes lentos
```

## 🔍 Debugging

### Via Docker

```bash
# Manter containers para inspeção
./run_tests_docker.sh -k

# Ver logs do container
docker-compose -f docker-compose.test.yml logs test-app

# Entrar no container
docker-compose -f docker-compose.test.yml exec test-app bash
```

### Via Local

```bash
# Parar no primeiro erro
pytest -x

# Mostrar output mesmo em sucesso
pytest -s

# Executar teste específico
pytest tests/unit/test_service.py::test_meu_metodo

# Com breakpoint
pytest --pdb
```

## 📈 Boas Práticas

1. **Nomes descritivos**: Use nomes que descrevam o que está sendo testado
2. **Arrange-Act-Assert**: Organize testes em 3 seções
3. **Um assert por teste**: Teste uma coisa por vez
4. **Mocks apropriados**: Use mocks para dependências externas
5. **Fixtures reutilizáveis**: Crie fixtures para dados comuns
6. **Cobertura mínima**: Mantenha pelo menos 80% de cobertura
7. **Ambiente isolado**: Use Docker para garantir consistência

## 🐛 Troubleshooting

### Erro de importação

```bash
# Adicionar diretório ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Erro de dependências

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements/development.txt
```

### Erro de Docker

```bash
# Verificar se Docker está rodando
docker --version
docker-compose --version

# Limpar containers e volumes
docker-compose -f docker-compose.test.yml down -v
docker system prune -f
```

### Testes lentos

```bash
# Executar em paralelo (se disponível)
pytest -n auto

# Executar apenas testes rápidos
pytest -m "not slow"
```

### Banco de dados de teste

```bash
# Verificar se o banco está rodando
docker-compose -f docker-compose.test.yml ps

# Reiniciar apenas o banco
docker-compose -f docker-compose.test.yml restart test-db
```

## 🚀 CI/CD

Para integração contínua, use:

```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: ./run_tests_docker.sh -c -b
```

Ou para execução local em CI:

```yaml
- name: Run Tests
  run: |
    pip install -r requirements/development.txt
    pytest --cov=app --cov-report=xml
```

## ✅ Status Atual dos Testes

- **Testes Unitários**: ✅ Funcionando
- **Testes de Integração**: ✅ Funcionando
- **Cobertura de Código**: ✅ Configurada
- **Ambiente Docker**: ✅ Configurado
- **Scripts de Automação**: ✅ Funcionando

Todos os testes estão passando com sucesso! 🎉
