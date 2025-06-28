import pytest
from unittest.mock import Mock, patch
from app.brain_agriculture.services.brain_agriculture import Brain_AgricultureService
from app.brain_agriculture.schemas.brain_agriculture import Produtor, Fazenda, Safra, ReturnSucess, ProdutorCreate


class TestBrainAgricultureService:
    """Testes unitários para Brain_AgricultureService"""

    @pytest.fixture
    def service(self, brain_agriculture_repository):
        return Brain_AgricultureService(brain_agriculture_repository)

    @pytest.mark.asyncio
    async def test_get_all_produtores_success(self, service, mock_repository_methods, sample_produtor):
        """Testa busca de todos os produtores com sucesso"""
        mock_repository_methods.get_all_produtores.return_value = [sample_produtor]
        
        result = await service.get_all_produtores()
        
        assert len(result) == 1
        assert result[0].id == sample_produtor.id
        assert result[0].nomeprodutor == sample_produtor.nomeprodutor

    @pytest.mark.asyncio
    async def test_get_produtor_by_id_success(self, service, mock_repository_methods, sample_produtor):
        """Testa busca de produtor por ID com sucesso"""
        mock_repository_methods.get_produtor_by_id.return_value = sample_produtor
        
        result = await service.get_produtor_by_id(1)
        
        assert result is not None
        assert result.id == sample_produtor.id
        assert result.nomeprodutor == sample_produtor.nomeprodutor

    @pytest.mark.asyncio
    async def test_get_produtor_by_id_not_found(self, service, mock_repository_methods):
        """Testa busca de produtor por ID quando não encontrado"""
        mock_repository_methods.get_produtor_by_id.return_value = None
        
        result = await service.get_produtor_by_id(999)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_create_produtor_success(self, service, mock_repository_methods, sample_produtor):
        """Testa criação de produtor com sucesso"""
        mock_repository_methods.get_produtor_by_cpf.return_value = None
        mock_repository_methods.create_produtor.return_value = sample_produtor
        
        produtor_data = ProdutorCreate(
            cpf="123.456.789-00",
            nomeprodutor="João Silva"
        )
        
        result = await service.create_produtor(produtor_data)
        
        assert result.success is True
        assert "Produtor criado com sucesso" in result.message
        assert result.data["id"] == sample_produtor.id

    @pytest.mark.asyncio
    async def test_create_produtor_duplicate_cpf(self, service, mock_repository_methods, sample_produtor):
        """Testa criação de produtor com CPF duplicado"""
        mock_repository_methods.get_produtor_by_cpf.return_value = sample_produtor
        
        produtor_data = ProdutorCreate(
            cpf="123.456.789-00",
            nomeprodutor="João Silva"
        )
        
        result = await service.create_produtor(produtor_data)
        
        assert result.success is False
        assert "Já existe um produtor cadastrado com este CPF" in result.message

    @pytest.mark.asyncio
    async def test_update_produtor_success(self, service, mock_repository_methods, sample_produtor):
        """Testa atualização de produtor com sucesso"""
        mock_repository_methods.get_produtor_by_id.return_value = sample_produtor
        mock_repository_methods.update_produtor.return_value = sample_produtor
        
        update_data = {"nomeprodutor": "João Silva Atualizado"}
        
        result = await service.update_produtor(1, update_data)
        
        assert result.success is True
        assert "Produtor atualizado com sucesso" in result.message

    @pytest.mark.asyncio
    async def test_update_produtor_not_found(self, service, mock_repository_methods):
        """Testa atualização de produtor quando não encontrado"""
        mock_repository_methods.get_produtor_by_id.return_value = None
        
        update_data = {"nomeprodutor": "João Silva Atualizado"}
        
        result = await service.update_produtor(999, update_data)
        
        assert result.success is False
        assert "Produtor não encontrado" in result.message

    @pytest.mark.asyncio
    async def test_delete_produtor_success(self, service, mock_repository_methods, sample_produtor):
        """Testa exclusão de produtor com sucesso"""
        mock_repository_methods.get_produtor_by_id.return_value = sample_produtor
        mock_repository_methods.delete_produtor.return_value = True
        
        result = await service.delete_produtor(1)
        
        assert result.success is True
        assert "Produtor excluído com sucesso" in result.message

    @pytest.mark.asyncio
    async def test_delete_produtor_not_found(self, service, mock_repository_methods):
        """Testa exclusão de produtor quando não encontrado"""
        mock_repository_methods.get_produtor_by_id.return_value = None
        
        result = await service.delete_produtor(999)
        
        assert result.success is False
        assert "Produtor não encontrado" in result.message

    @pytest.mark.asyncio
    async def test_get_estatisticas_fazendas_success(self, service, mock_repository_methods):
        """Testa busca de estatísticas de fazendas com sucesso"""
        mock_repository_methods.get_fazendas_por_estado.return_value = [
            {"estado": "SP", "quantidade": 5},
            {"estado": "MG", "quantidade": 3}
        ]
        mock_repository_methods.get_total_fazendas.return_value = 8
        
        result = await service.get_estatisticas_fazendas()
        
        assert result.total_fazendas == 8
        assert len(result.fazendas_por_estado) == 2
        assert result.fazendas_por_estado[0].estado == "SP"
        assert result.fazendas_por_estado[0].quantidade == 5

    @pytest.mark.asyncio
    async def test_get_estatisticas_culturas_success(self, service, mock_repository_methods):
        """Testa busca de estatísticas de culturas com sucesso"""
        mock_repository_methods.get_total_culturas.return_value = 10
        mock_repository_methods.get_culturas_agrupadas.return_value = [
            {"cultura": "Soja", "quantidade": 5},
            {"cultura": "Milho", "quantidade": 3}
        ]
        
        result = await service.get_estatisticas_culturas()
        
        assert result.total_culturas == 10
        assert len(result.culturas) == 2
        assert result.culturas[0].cultura == "Soja"
        assert result.culturas[0].quantidade == 5

    @pytest.mark.asyncio
    async def test_get_estatisticas_areas_success(self, service, mock_repository_methods):
        """Testa busca de estatísticas de áreas com sucesso"""
        mock_repository_methods.get_estatisticas_areas.return_value = {
            "area_total": 1000.0,
            "area_agricultavel": 800.0,
            "area_vegetacao": 200.0
        }
        
        result = await service.get_estatisticas_areas()
        
        assert result.area_total == 1000.0
        assert result.area_agricultavel == 800.0
        assert result.area_vegetacao == 200.0

    @pytest.mark.asyncio
    async def test_get_resumo_fazendas_success(self, service, mock_repository_methods):
        """Testa busca de resumo de fazendas com sucesso"""
        mock_repository_methods.get_total_fazendas.return_value = 10
        mock_repository_methods.get_estatisticas_areas.return_value = {
            "area_total": 1000.0,
            "area_agricultavel": 800.0,
            "area_vegetacao": 200.0
        }
        
        result = await service.get_resumo_fazendas()
        
        assert result.total_fazendas == 10
        assert result.total_area == 1000.0

    @pytest.mark.asyncio
    async def test_get_fazendas_resumidas_success(self, service, mock_repository_methods, sample_fazenda):
        """Testa busca de fazendas resumidas com sucesso"""
        mock_repository_methods.get_all_fazendas.return_value = [sample_fazenda]
        
        result = await service.get_fazendas_resumidas()
        
        assert len(result) == 1
        assert result[0].id == sample_fazenda.id
        assert result[0].nomefazenda == sample_fazenda.nomefazenda

    @pytest.mark.asyncio
    async def test_get_produtores_resumidos_success(self, service, mock_repository_methods, sample_produtor):
        """Testa busca de produtores resumidos com sucesso"""
        mock_repository_methods.get_all_produtores.return_value = [sample_produtor]
        
        result = await service.get_produtores_resumidos()
        
        assert len(result) == 1
        assert result[0].id == sample_produtor.id
        assert result[0].nomeprodutor == sample_produtor.nomeprodutor 