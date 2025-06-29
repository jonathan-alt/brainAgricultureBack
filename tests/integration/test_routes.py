import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock

from app.main import app
from app.core.container import Container
from app.brain_agriculture.models.brain_agriculture import Produtor, Fazenda, Safra
from app.brain_agriculture.schemas.brain_agriculture import ReturnSucess, EstatisticasFazendas, FazendaPorEstado, EstatisticasCulturas, CulturaQuantidade, EstatisticasAreas, ResumoFazendas, FazendaResumida, ProdutorResumido, ProdutorCompleto, FazendaComSafras, FazendaCompleta, VincularFazendaProdutor, VincularProdutorFazenda
import app.brain_agriculture.api.v1.routes as routes_module

@pytest.fixture
def mock_service():
    mock_service = Mock()
    mock_service.get_all_produtores = AsyncMock()
    mock_service.get_produtor_by_id = AsyncMock()
    mock_service.create_produtor = AsyncMock()
    mock_service.update_produtor = AsyncMock()
    mock_service.delete_produtor = AsyncMock()
    mock_service.get_all_fazendas = AsyncMock()
    mock_service.get_fazenda_by_id = AsyncMock()
    mock_service.create_fazenda = AsyncMock()
    mock_service.update_fazenda = AsyncMock()
    mock_service.delete_fazenda = AsyncMock()
    mock_service.get_all_safras = AsyncMock()
    mock_service.get_safra_by_id = AsyncMock()
    mock_service.create_safra = AsyncMock()
    mock_service.update_safra = AsyncMock()
    mock_service.delete_safra = AsyncMock()
    mock_service.get_estatisticas_fazendas = AsyncMock()
    mock_service.get_estatisticas_culturas = AsyncMock()
    mock_service.get_estatisticas_areas = AsyncMock()
    mock_service.get_resumo_fazendas = AsyncMock()
    mock_service.get_fazendas_resumidas = AsyncMock()
    mock_service.get_produtores_resumidos = AsyncMock()
    mock_service.get_teste = AsyncMock()
    mock_service.get_produtor_completo = AsyncMock()
    mock_service.get_fazenda_completa = AsyncMock()
    mock_service.vincular_fazenda_produtor = AsyncMock()
    mock_service.vincular_produtor_fazenda = AsyncMock()
    return mock_service

class TestBrainAgricultureRoutes:
    def test_get_all_produtores_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                sample_produtor = Produtor(
                    id=1,
                    cpf="123.456.789-00",
                    nomeprodutor="João Silva"
                )
                mock_service.get_all_produtores.return_value = [sample_produtor]
                response = client.get("/api/v1/produtores")
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 1
                assert data[0]["id"] == 1
                assert data[0]["nomeprodutor"] == "João Silva"

    def test_get_produtor_by_id_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                sample_produtor = Produtor(
                    id=1,
                    cpf="123.456.789-00",
                    nomeprodutor="João Silva"
                )
                mock_service.get_produtor_by_id.return_value = sample_produtor
                response = client.get("/api/v1/produtores/1")
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == 1
                assert data["nomeprodutor"] == "João Silva"

    def test_get_produtor_by_id_not_found(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_produtor_by_id.return_value = None
                response = client.get("/api/v1/produtores/999")
                assert response.status_code == 404
                assert "Produtor não encontrado" in response.json()["detail"]

    def test_create_produtor_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.create_produtor.return_value = ReturnSucess(
                    success=True,
                    message="Produtor criado com sucesso",
                    data={"id": 1, "cpf": "123.456.789-00", "nome": "João Silva"}
                )
                produtor_data = {
                    "cpf": "123.456.789-00",
                    "nomeprodutor": "João Silva"
                }
                response = client.post("/api/v1/produtores", json=produtor_data)
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "Produtor criado com sucesso" in data["message"]

    def test_create_produtor_duplicate_cpf(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.create_produtor.return_value = ReturnSucess(
                    success=False,
                    message="Já existe um produtor cadastrado com este CPF",
                    data={}
                )
                produtor_data = {
                    "cpf": "123.456.789-00",
                    "nomeprodutor": "João Silva"
                }
                response = client.post("/api/v1/produtores", json=produtor_data)
                assert response.status_code == 400
                assert "Já existe um produtor cadastrado com este CPF" in response.json()["detail"]

    def test_get_estatisticas_fazendas_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_estatisticas_fazendas.return_value = EstatisticasFazendas(
                    total_fazendas=10,
                    fazendas_por_estado=[
                        FazendaPorEstado(estado="SP", quantidade=5),
                        FazendaPorEstado(estado="MG", quantidade=3)
                    ]
                )
                response = client.get("/api/v1/fazendas/estatisticas")
                assert response.status_code == 200
                data = response.json()
                assert data["total_fazendas"] == 10
                assert len(data["fazendas_por_estado"]) == 2

    def test_get_estatisticas_culturas_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_estatisticas_culturas.return_value = EstatisticasCulturas(
                    total_culturas=15,
                    culturas=[
                        CulturaQuantidade(cultura="Soja", quantidade=8),
                        CulturaQuantidade(cultura="Milho", quantidade=5)
                    ]
                )
                response = client.get("/api/v1/safras/estatisticas-culturas")
                assert response.status_code == 200
                data = response.json()
                assert data["total_culturas"] == 15
                assert len(data["culturas"]) == 2

    def test_get_estatisticas_areas_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_estatisticas_areas.return_value = EstatisticasAreas(
                    area_total=1000.0,
                    area_agricultavel=800.0,
                    area_vegetacao=200.0
                )
                response = client.get("/api/v1/fazendas/estatisticas-areas")
                assert response.status_code == 200
                data = response.json()
                assert data["area_total"] == 1000.0
                assert data["area_agricultavel"] == 800.0
                assert data["area_vegetacao"] == 200.0

    def test_get_resumo_fazendas_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_resumo_fazendas.return_value = ResumoFazendas(
                    total_fazendas=10,
                    total_area=1000.0
                )
                response = client.get("/api/v1/fazendas/resumo")
                assert response.status_code == 200
                data = response.json()
                assert data["total_fazendas"] == 10
                assert data["total_area"] == 1000.0

    def test_get_lista_fazendas_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_fazendas_resumidas.return_value = [
                    FazendaResumida(id=1, nomefazenda="Fazenda Nova"),
                    FazendaResumida(id=2, nomefazenda="Fazenda São João")
                ]
                response = client.get("/api/v1/fazendas/lista")
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2
                assert data[0]["id"] == 1
                assert data[0]["nomefazenda"] == "Fazenda Nova"

    def test_get_lista_produtores_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_produtores_resumidos.return_value = [
                    ProdutorResumido(id=1, cpf="123.456.789-00", nomeprodutor="João Silva"),
                    ProdutorResumido(id=2, cpf="987.654.321-00", nomeprodutor="Maria Santos")
                ]
                response = client.get("/api/v1/produtores/lista")
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2
                assert data[0]["id"] == 1
                assert data[0]["cpf"] == "123.456.789-00"
                assert data[0]["nomeprodutor"] == "João Silva"

    def test_internal_server_error(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_all_produtores.side_effect = Exception("Erro interno")
                response = client.get("/api/v1/produtores")
                assert response.status_code == 500
                assert "Erro interno do servidor" in response.json()["detail"]

    def test_get_produtor_completo_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                from app.brain_agriculture.schemas.brain_agriculture import ProdutorCompleto, FazendaComSafras
                
                # Criar dados de teste
                sample_safra = Safra(id=1, ano=2024, cultura="Soja", idfazenda=1)
                sample_fazenda_com_safras = FazendaComSafras(
                    id=1,
                    nomefazenda="Fazenda São João",
                    cidade="São Paulo",
                    estado="SP",
                    areatotalfazenda=100.5,
                    areaagricutavel=80.0,
                    idprodutor=1,
                    safras=[sample_safra]
                )
                sample_produtor_completo = ProdutorCompleto(
                    id=1,
                    cpf="123.456.789-00",
                    nomeprodutor="João Silva",
                    fazendas=[sample_fazenda_com_safras]
                )
                
                mock_service.get_produtor_completo.return_value = sample_produtor_completo
                response = client.get("/api/v1/produtores/1/completo")
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == 1
                assert data["nomeprodutor"] == "João Silva"
                assert len(data["fazendas"]) == 1
                assert data["fazendas"][0]["nomefazenda"] == "Fazenda São João"
                assert len(data["fazendas"][0]["safras"]) == 1
                assert data["fazendas"][0]["safras"][0]["cultura"] == "Soja"

    def test_get_produtor_completo_not_found(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_produtor_completo.return_value = None
                response = client.get("/api/v1/produtores/999/completo")
                assert response.status_code == 404
                assert "Produtor não encontrado" in response.json()["detail"]

    def test_get_fazenda_completa_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                from app.brain_agriculture.schemas.brain_agriculture import FazendaCompleta
                
                # Criar dados de teste
                sample_safra1 = Safra(id=1, ano=2024, cultura="Soja", idfazenda=1)
                sample_safra2 = Safra(id=2, ano=2024, cultura="Milho", idfazenda=1)
                sample_fazenda_completa = FazendaCompleta(
                    id=1,
                    nomefazenda="Fazenda São João",
                    cidade="São Paulo",
                    estado="SP",
                    areatotalfazenda=100.5,
                    areaagricutavel=80.0,
                    idprodutor=1,
                    safras=[sample_safra1, sample_safra2]
                )
                
                mock_service.get_fazenda_completa.return_value = sample_fazenda_completa
                response = client.get("/api/v1/fazendas/1/completa")
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == 1
                assert data["nomefazenda"] == "Fazenda São João"
                assert len(data["safras"]) == 2
                assert data["safras"][0]["cultura"] == "Soja"
                assert data["safras"][1]["cultura"] == "Milho"

    def test_get_fazenda_completa_not_found(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.get_fazenda_completa.return_value = None
                response = client.get("/api/v1/fazendas/999/completa")
                assert response.status_code == 404
                assert "Fazenda não encontrada" in response.json()["detail"]

    def test_vincular_fazenda_produtor_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.vincular_fazenda_produtor.return_value = ReturnSucess(
                    success=True,
                    message="Fazenda 'Fazenda São João' vinculada com sucesso ao produtor 'João Silva'",
                    data={
                        "fazenda_id": 1,
                        "fazenda_nome": "Fazenda São João",
                        "produtor_id": 2,
                        "produtor_nome": "João Silva"
                    }
                )
                
                dados = {"fazenda_id": 1, "produtor_id": 2}
                response = client.post("/api/v1/vincular-fazenda-produtor", json=dados)
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "vinculada com sucesso" in data["message"]
                assert data["data"]["fazenda_id"] == 1
                assert data["data"]["produtor_id"] == 2

    def test_vincular_fazenda_produtor_error(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.vincular_fazenda_produtor.return_value = ReturnSucess(
                    success=False,
                    message="Fazenda com ID 999 não encontrada",
                    data={}
                )
                
                dados = {"fazenda_id": 999, "produtor_id": 1}
                response = client.post("/api/v1/vincular-fazenda-produtor", json=dados)
                
                assert response.status_code == 400
                assert "Fazenda com ID 999 não encontrada" in response.json()["detail"]

    def test_vincular_produtor_fazenda_success(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.vincular_produtor_fazenda.return_value = ReturnSucess(
                    success=True,
                    message="Produtor 'João Silva' vinculado com sucesso à fazenda 'Fazenda São João'",
                    data={
                        "produtor_id": 2,
                        "produtor_nome": "João Silva",
                        "fazenda_id": 1,
                        "fazenda_nome": "Fazenda São João"
                    }
                )
                
                dados = {"produtor_id": 2, "fazenda_id": 1}
                response = client.post("/api/v1/vincular-produtor-fazenda", json=dados)
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "vinculado com sucesso" in data["message"]
                assert data["data"]["produtor_id"] == 2
                assert data["data"]["fazenda_id"] == 1

    def test_vincular_produtor_fazenda_error(self, mock_service):
        with TestClient(app) as client:
            container = app.container
            with container.brain_agriculture_service.override(mock_service):
                mock_service.vincular_produtor_fazenda.return_value = ReturnSucess(
                    success=False,
                    message="Produtor com ID 999 não encontrado",
                    data={}
                )
                
                dados = {"produtor_id": 999, "fazenda_id": 1}
                response = client.post("/api/v1/vincular-produtor-fazenda", json=dados)
                
                assert response.status_code == 400
                assert "Produtor com ID 999 não encontrado" in response.json()["detail"] 