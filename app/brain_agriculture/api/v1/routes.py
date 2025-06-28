import logging
import time
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, HTTPException

from app.core.container import Container

from app.brain_agriculture.schemas.brain_agriculture import Brain_Agriculture, DadosFazenda, Produtor, Fazenda, Safra, ReturnSucess, EstatisticasFazendas
from app.brain_agriculture.schemas.brain_agriculture import EstatisticasCulturas
from app.brain_agriculture.schemas.brain_agriculture import EstatisticasAreas
from app.brain_agriculture.schemas.brain_agriculture import ResumoFazendas
from app.brain_agriculture.schemas.brain_agriculture import FazendaResumida, ProdutorResumido
from app.brain_agriculture.schemas.brain_agriculture import ProdutorCreate, FazendaCreate, SafraCreate
from app.brain_agriculture.services.brain_agriculture import Brain_AgricultureService

logger = logging.getLogger(__name__)

brain_agriculture_router = r = APIRouter()


@r.get("/fazendas/{fazenda}/dados", response_model=DadosFazenda)
@inject
async def get_dados_fazenda(
    fazenda: str,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca dados de uma fazenda específica"""
    try:
        response = await brain_agriculture_service.get_teste(fazenda)
        return response
    except Exception as e:
        logger.error(f"Erro ao buscar dados da fazenda {fazenda}: {e}")
        raise e


# Rotas CRUD para Produtores
@r.get("/produtores", response_model=List[Produtor])
@inject
async def get_all_produtores(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista todos os produtores"""
    try:
        produtores = await brain_agriculture_service.get_all_produtores()
        return produtores
    except Exception as e:
        logger.error(f"Erro ao buscar produtores: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


# Rota específica para lista de produtores (deve vir antes da rota com parâmetro)
@r.get("/produtores/lista", response_model=List[ProdutorResumido])
@inject
async def get_lista_produtores(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista resumida de produtores (ID e nome)"""
    try:
        produtores = await brain_agriculture_service.get_produtores_resumidos()
        return produtores
    except Exception as e:
        logger.error(f"Erro ao buscar lista de produtores: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/produtores/{produtor_id}", response_model=Produtor)
@inject
async def get_produtor_by_id(
    produtor_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca um produtor específico pelo ID"""
    try:
        produtor = await brain_agriculture_service.get_produtor_by_id(produtor_id)
        if not produtor:
            raise HTTPException(status_code=404, detail="Produtor não encontrado")
        return produtor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar produtor {produtor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.post("/produtores", response_model=ReturnSucess)
@inject
async def create_produtor(
    produtor: ProdutorCreate,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Cria um novo produtor"""
    try:
        result = await brain_agriculture_service.create_produtor(produtor)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar produtor: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.put("/produtores/{produtor_id}", response_model=ReturnSucess)
@inject
async def update_produtor(
    produtor_id: int,
    produtor_data: ProdutorCreate,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Atualiza um produtor existente"""
    try:
        # Converter o schema para dict, excluindo campos None
        update_data = {}
        if produtor_data.cpf is not None:
            update_data['cpf'] = produtor_data.cpf
        if produtor_data.nomeprodutor is not None:
            update_data['nomeprodutor'] = produtor_data.nomeprodutor
        
        result = await brain_agriculture_service.update_produtor(produtor_id, update_data)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar produtor {produtor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.delete("/produtores/{produtor_id}", response_model=ReturnSucess)
@inject
async def delete_produtor(
    produtor_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Exclui um produtor"""
    try:
        result = await brain_agriculture_service.delete_produtor(produtor_id)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir produtor {produtor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


# Rotas CRUD para Fazendas
@r.get("/fazendas", response_model=List[Fazenda])
@inject
async def get_all_fazendas(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista todas as fazendas"""
    try:
        fazendas = await brain_agriculture_service.get_all_fazendas()
        return fazendas
    except Exception as e:
        logger.error(f"Erro ao buscar fazendas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


# Rotas específicas para fazendas (devem vir antes das rotas com parâmetros)
@r.get("/fazendas/estatisticas", response_model=EstatisticasFazendas)
@inject
async def get_estatisticas_fazendas(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca estatísticas de fazendas por estado e total"""
    try:
        estatisticas = await brain_agriculture_service.get_estatisticas_fazendas()
        return estatisticas
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas de fazendas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/fazendas/estatisticas-areas", response_model=EstatisticasAreas)
@inject
async def get_estatisticas_areas(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca estatísticas de áreas das fazendas (total, agricultável e vegetação)"""
    try:
        estatisticas = await brain_agriculture_service.get_estatisticas_areas()
        return estatisticas
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas de áreas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/fazendas/resumo", response_model=ResumoFazendas)
@inject
async def get_resumo_fazendas(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca resumo simplificado: total de fazendas e área total cadastrada"""
    try:
        resumo = await brain_agriculture_service.get_resumo_fazendas()
        return resumo
    except Exception as e:
        logger.error(f"Erro ao buscar resumo de fazendas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/fazendas/lista", response_model=List[FazendaResumida])
@inject
async def get_lista_fazendas(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista resumida de fazendas (ID e nome)"""
    try:
        fazendas = await brain_agriculture_service.get_fazendas_resumidas()
        return fazendas
    except Exception as e:
        logger.error(f"Erro ao buscar lista de fazendas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/fazendas/{fazenda_id}", response_model=Fazenda)
@inject
async def get_fazenda_by_id(
    fazenda_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca uma fazenda específica pelo ID"""
    try:
        fazenda = await brain_agriculture_service.get_fazenda_by_id(fazenda_id)
        if not fazenda:
            raise HTTPException(status_code=404, detail="Fazenda não encontrada")
        return fazenda
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar fazenda {fazenda_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/produtores/{produtor_id}/fazendas", response_model=List[Fazenda])
@inject
async def get_fazendas_by_produtor(
    produtor_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista fazendas de um produtor específico"""
    try:
        fazendas = await brain_agriculture_service.get_fazendas_by_produtor(produtor_id)
        return fazendas
    except Exception as e:
        logger.error(f"Erro ao buscar fazendas do produtor {produtor_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.post("/fazendas", response_model=ReturnSucess)
@inject
async def create_fazenda(
    fazenda: FazendaCreate,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Cria uma nova fazenda"""
    try:
        result = await brain_agriculture_service.create_fazenda(fazenda)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar fazenda: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.put("/fazendas/{fazenda_id}", response_model=ReturnSucess)
@inject
async def update_fazenda(
    fazenda_id: int,
    fazenda_data: FazendaCreate,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Atualiza uma fazenda existente"""
    try:
        # Converter o schema para dict, excluindo campos None
        update_data = {}
        if fazenda_data.nomefazenda is not None:
            update_data['nomefazenda'] = fazenda_data.nomefazenda
        if fazenda_data.cidade is not None:
            update_data['cidade'] = fazenda_data.cidade
        if fazenda_data.estado is not None:
            update_data['estado'] = fazenda_data.estado
        if fazenda_data.areatotalfazenda is not None:
            update_data['areatotalfazenda'] = fazenda_data.areatotalfazenda
        if fazenda_data.areaagricutavel is not None:
            update_data['areaagricutavel'] = fazenda_data.areaagricutavel
        if fazenda_data.idprodutor is not None:
            update_data['idprodutor'] = fazenda_data.idprodutor
        
        result = await brain_agriculture_service.update_fazenda(fazenda_id, update_data)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar fazenda {fazenda_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.delete("/fazendas/{fazenda_id}", response_model=ReturnSucess)
@inject
async def delete_fazenda(
    fazenda_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Exclui uma fazenda"""
    try:
        result = await brain_agriculture_service.delete_fazenda(fazenda_id)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir fazenda {fazenda_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


# Rotas CRUD para Safras
@r.get("/safras", response_model=List[Safra])
@inject
async def get_all_safras(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista todas as safras"""
    try:
        safras = await brain_agriculture_service.get_all_safras()
        return safras
    except Exception as e:
        logger.error(f"Erro ao buscar safras: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


# Rota específica para estatísticas de culturas (deve vir antes da rota com parâmetro)
@r.get("/safras/estatisticas-culturas", response_model=EstatisticasCulturas)
@inject
async def get_estatisticas_culturas(
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca estatísticas de culturas plantadas (total e por cultura)"""
    try:
        estatisticas = await brain_agriculture_service.get_estatisticas_culturas()
        return estatisticas
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas de culturas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/safras/{safra_id}", response_model=Safra)
@inject
async def get_safra_by_id(
    safra_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Busca uma safra específica pelo ID"""
    try:
        safra = await brain_agriculture_service.get_safra_by_id(safra_id)
        if not safra:
            raise HTTPException(status_code=404, detail="Safra não encontrada")
        return safra
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar safra {safra_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/fazendas/{fazenda_id}/safras", response_model=List[Safra])
@inject
async def get_safras_by_fazenda(
    fazenda_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista safras de uma fazenda específica"""
    try:
        safras = await brain_agriculture_service.get_safras_by_fazenda(fazenda_id)
        return safras
    except Exception as e:
        logger.error(f"Erro ao buscar safras da fazenda {fazenda_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.get("/safras/ano/{ano}", response_model=List[Safra])
@inject
async def get_safras_by_ano(
    ano: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Lista safras por ano específico"""
    try:
        safras = await brain_agriculture_service.get_safras_by_ano(ano)
        return safras
    except Exception as e:
        logger.error(f"Erro ao buscar safras do ano {ano}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.post("/safras", response_model=ReturnSucess)
@inject
async def create_safra(
    safra: SafraCreate,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Cria uma nova safra"""
    try:
        result = await brain_agriculture_service.create_safra(safra)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar safra: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.put("/safras/{safra_id}", response_model=ReturnSucess)
@inject
async def update_safra(
    safra_id: int,
    safra_data: SafraCreate,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Atualiza uma safra existente"""
    try:
        # Converter o schema para dict, excluindo campos None
        update_data = {}
        if safra_data.ano is not None:
            update_data['ano'] = safra_data.ano
        if safra_data.cultura is not None:
            update_data['cultura'] = safra_data.cultura
        if safra_data.idfazenda is not None:
            update_data['idfazenda'] = safra_data.idfazenda
        
        result = await brain_agriculture_service.update_safra(safra_id, update_data)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar safra {safra_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@r.delete("/safras/{safra_id}", response_model=ReturnSucess)
@inject
async def delete_safra(
    safra_id: int,
    brain_agriculture_service: Brain_AgricultureService = Depends(Provide[Container.brain_agriculture_service]),
):
    """Exclui uma safra"""
    try:
        result = await brain_agriculture_service.delete_safra(safra_id)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao excluir safra {safra_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")




