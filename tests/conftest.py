import pytest
from typing import Generator, Dict, Any
from unittest.mock import Mock, AsyncMock
from sqlmodel import Session, create_engine
from sqlalchemy.pool import StaticPool

from app.core.container import Container
from app.brain_agriculture.models.brain_agriculture import Produtor, Fazenda, Safra
from app.brain_agriculture.repositories.brain_agriculture import Brain_AgricultureRepository
from app.brain_agriculture.services.brain_agriculture import Brain_AgricultureService


@pytest.fixture(scope="session")
def test_engine():
    """Engine de teste usando SQLite em memória"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine


@pytest.fixture
def test_session(test_engine):
    """Sessão de teste"""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def mock_db():
    """Mock do banco de dados"""
    return Mock()


@pytest.fixture
def brain_agriculture_repository(mock_db):
    """Repositório com banco mockado"""
    return Brain_AgricultureRepository(mock_db)


@pytest.fixture
def brain_agriculture_service(brain_agriculture_repository):
    """Service com repositório mockado"""
    return Brain_AgricultureService(brain_agriculture_repository)


@pytest.fixture
def container():
    """Container de dependências para testes"""
    container = Container()
    return container


@pytest.fixture
def sample_produtor_data() -> Dict[str, Any]:
    """Dados de exemplo para um produtor"""
    return {
        "id": 1,
        "cpf": "123.456.789-00",
        "nomeprodutor": "João Silva"
    }


@pytest.fixture
def sample_fazenda_data() -> Dict[str, Any]:
    """Dados de exemplo para uma fazenda"""
    return {
        "id": 1,
        "nomefazenda": "Fazenda Nova",
        "cidade": "São Paulo",
        "estado": "SP",
        "areatotalfazenda": 100.0,
        "areaagricutavel": 80.0,
        "idprodutor": 1
    }


@pytest.fixture
def sample_safra_data() -> Dict[str, Any]:
    """Dados de exemplo para uma safra"""
    return {
        "id": 1,
        "ano": 2024,
        "cultura": "Soja",
        "idfazenda": 1
    }


@pytest.fixture
def sample_produtor(sample_produtor_data) -> Produtor:
    """Instância de exemplo de Produtor"""
    return Produtor(**sample_produtor_data)


@pytest.fixture
def sample_fazenda(sample_fazenda_data) -> Fazenda:
    """Instância de exemplo de Fazenda"""
    return Fazenda(**sample_fazenda_data)


@pytest.fixture
def sample_safra(sample_safra_data) -> Safra:
    """Instância de exemplo de Safra"""
    return Safra(**sample_safra_data)


@pytest.fixture
def mock_repository_methods(brain_agriculture_repository):
    """Mock dos métodos do repositório"""
    brain_agriculture_repository.get_all_produtores = Mock(return_value=[])
    brain_agriculture_repository.get_produtor_by_id = Mock(return_value=None)
    brain_agriculture_repository.get_produtor_by_cpf = Mock(return_value=None)
    brain_agriculture_repository.create_produtor = Mock()
    brain_agriculture_repository.update_produtor = Mock()
    brain_agriculture_repository.delete_produtor = Mock(return_value=True)
    
    brain_agriculture_repository.get_all_fazendas = Mock(return_value=[])
    brain_agriculture_repository.get_fazenda_by_id = Mock(return_value=None)
    brain_agriculture_repository.get_fazendas_by_produtor = Mock(return_value=[])
    brain_agriculture_repository.create_fazenda = Mock()
    brain_agriculture_repository.update_fazenda = Mock()
    brain_agriculture_repository.delete_fazenda = Mock(return_value=True)
    
    brain_agriculture_repository.get_all_safras = Mock(return_value=[])
    brain_agriculture_repository.get_safra_by_id = Mock(return_value=None)
    brain_agriculture_repository.get_safras_by_fazenda = Mock(return_value=[])
    brain_agriculture_repository.get_safras_by_ano = Mock(return_value=[])
    brain_agriculture_repository.create_safra = Mock()
    brain_agriculture_repository.update_safra = Mock()
    brain_agriculture_repository.delete_safra = Mock(return_value=True)
    
    brain_agriculture_repository.get_total_fazendas = Mock(return_value=0)
    brain_agriculture_repository.get_fazendas_por_estado = Mock(return_value=[])
    brain_agriculture_repository.get_estatisticas_areas = Mock(return_value={
        "area_total": 0.0,
        "area_agricultavel": 0.0,
        "area_vegetacao": 0.0
    })
    brain_agriculture_repository.get_total_culturas = Mock(return_value=0)
    brain_agriculture_repository.get_culturas_agrupadas = Mock(return_value=[])
    
    return brain_agriculture_repository 