import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session

from app.brain_agriculture.repositories.brain_agriculture import Brain_AgricultureRepository
from app.brain_agriculture.models.brain_agriculture import Produtor, Fazenda, Safra


class TestBrainAgricultureRepository:
    """Testes unitários para Brain_AgricultureRepository"""

    @pytest.fixture
    def repository(self, mock_db):
        return Brain_AgricultureRepository(mock_db)

    def test_get_all_produtores_success(self, repository, sample_produtor):
        """Testa busca de todos os produtores com sucesso"""
        mock_session = Mock()
        mock_session.exec.return_value.all.return_value = [sample_produtor]
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.get_all_produtores()
            
            assert result == [sample_produtor]
            mock_session.exec.assert_called_once()

    def test_get_all_produtores_no_db(self, repository):
        """Testa busca de produtores quando banco não está disponível"""
        repository.db = None
        
        result = repository.get_all_produtores()
        
        assert result == []

    def test_get_produtor_by_id_success(self, repository, sample_produtor):
        """Testa busca de produtor por ID com sucesso"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = sample_produtor
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.get_produtor_by_id(1)
            
            assert result == sample_produtor
            mock_session.exec.assert_called_once()

    def test_get_produtor_by_id_not_found(self, repository):
        """Testa busca de produtor por ID quando não encontrado"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = None
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.get_produtor_by_id(999)
            
            assert result is None

    def test_get_produtor_by_cpf_success(self, repository, sample_produtor):
        """Testa busca de produtor por CPF com sucesso"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = sample_produtor
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.get_produtor_by_cpf("123.456.789-00")
            
            assert result == sample_produtor

    def test_create_produtor_success(self, repository, sample_produtor):
        """Testa criação de produtor com sucesso"""
        mock_session = Mock()
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.create_produtor(sample_produtor)
            
            assert result == sample_produtor
            mock_session.add.assert_called_once_with(sample_produtor)
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once_with(sample_produtor)

    def test_create_produtor_no_db(self, repository, sample_produtor):
        """Testa criação de produtor quando banco não está disponível"""
        repository.db = None
        
        with pytest.raises(Exception, match="Banco de dados não disponível"):
            repository.create_produtor(sample_produtor)

    def test_update_produtor_success(self, repository, sample_produtor):
        """Testa atualização de produtor com sucesso"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = sample_produtor
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            update_data = {"nomeprodutor": "João Silva Atualizado"}
            result = repository.update_produtor(1, update_data)
            
            assert result == sample_produtor
            assert sample_produtor.nomeprodutor == "João Silva Atualizado"

    def test_update_produtor_not_found(self, repository):
        """Testa atualização de produtor quando não encontrado"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = None
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.update_produtor(999, {"nomeprodutor": "Teste"})
            
            assert result is None

    def test_delete_produtor_success(self, repository, sample_produtor):
        """Testa exclusão de produtor com sucesso"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = sample_produtor
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.delete_produtor(1)
            
            assert result is True
            mock_session.delete.assert_called_once_with(sample_produtor)
            mock_session.commit.assert_called_once()

    def test_delete_produtor_not_found(self, repository):
        """Testa exclusão de produtor quando não encontrado"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = None
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.delete_produtor(999)
            
            assert result is False

    def test_get_total_fazendas_success(self, repository):
        """Testa busca do total de fazendas com sucesso"""
        mock_session = Mock()
        mock_session.exec.return_value.first.return_value = 10
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.get_total_fazendas()
            
            assert result == 10

    def test_get_total_fazendas_no_db(self, repository):
        """Testa busca do total de fazendas quando banco não está disponível"""
        repository.db = None
        
        result = repository.get_total_fazendas()
        
        assert result == 0

    def test_get_estatisticas_areas_success(self, repository):
        """Testa busca de estatísticas de áreas com sucesso"""
        mock_session = Mock()
        mock_result = Mock()
        mock_result.area_total = 1000.0
        mock_result.area_agricultavel = 800.0
        mock_session.exec.return_value.first.return_value = mock_result
        
        with patch.object(Session, '__enter__', return_value=mock_session):
            repository.db = Mock()
            
            result = repository.get_estatisticas_areas()
            
            expected = {
                "area_total": 1000.0,
                "area_agricultavel": 800.0,
                "area_vegetacao": 200.0
            }
            assert result == expected

    def test_get_estatisticas_areas_no_db(self, repository):
        """Testa busca de estatísticas de áreas quando banco não está disponível"""
        repository.db = None
        
        result = repository.get_estatisticas_areas()
        
        expected = {
            "area_total": 0,
            "area_agricultavel": 0,
            "area_vegetacao": 0
        }
        assert result == expected 