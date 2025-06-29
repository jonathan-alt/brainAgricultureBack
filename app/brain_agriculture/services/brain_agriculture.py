import datetime as dt
import logging
import time
import uuid
from typing import Dict, Optional, List

from app.core.services import BaseService
from app.brain_agriculture.repositories.brain_agriculture import Brain_AgricultureRepository
from app.brain_agriculture.schemas.brain_agriculture import (
    DadosFazenda,
    ReceiveBrain_AgricultureSchema,
    Produtor,
    Fazenda,
    Safra,
    ReturnSucess,
    EstatisticasFazendas,
    FazendaPorEstado,
    EstatisticasCulturas,
    CulturaQuantidade,
    EstatisticasAreas,
    ResumoFazendas,
    FazendaResumida,
    ProdutorResumido,
    ProdutorCreate,
    FazendaCreate,
    SafraCreate,
    DadosCompletosCreate,
    DadosCompletosResponse,
    ProdutorCompleto,
    FazendaCompleta,
    FazendaComSafras,
    VincularFazendaProdutor,
    VincularProdutorFazenda,
)
from app.brain_agriculture.models.brain_agriculture import Produtor as ProdutorModel, Fazenda as FazendaModel, Safra as SafraModel

logger = logging.getLogger(__name__)


class Brain_AgricultureService(BaseService):
    def __init__(self, brain_agriculture_repository: Brain_AgricultureRepository):
        self.brain_agriculture_repository = brain_agriculture_repository
        super().__init__(brain_agriculture_repository)

    async def get_teste(self, fazenda: str) -> DadosFazenda:
        return await self.brain_agriculture_repository.get_teste(fazenda)

    async def insert_brain_agriculture(self, brain_agriculture: ReceiveBrain_AgricultureSchema, client_id: int) -> None:
        """Insere dados do Brain Agriculture"""
        try:
            logger.info(f"Inserindo dados do Brain Agriculture para fazenda: {brain_agriculture.fazenda}, client_id: {client_id}")
            # Aqui você implementaria a lógica real de inserção no banco de dados
            # Por exemplo: await self.brain_agriculture_repository.insert(brain_agriculture, client_id)
        except Exception as e:
            logger.error(f"Erro ao inserir dados do Brain Agriculture: {e}")
            raise e

    # Métodos CRUD para Produtores
    async def get_all_produtores(self) -> List[Produtor]:
        """Busca todos os produtores"""
        try:
            produtores = self.brain_agriculture_repository.get_all_produtores()
            return [Produtor.from_orm(produtor) for produtor in produtores]
        except Exception as e:
            logger.error(f"Erro ao buscar produtores: {e}")
            raise e

    async def get_produtor_by_id(self, produtor_id: int) -> Optional[Produtor]:
        """Busca um produtor pelo ID"""
        try:
            produtor = self.brain_agriculture_repository.get_produtor_by_id(produtor_id)
            if produtor:
                return Produtor.from_orm(produtor)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar produtor {produtor_id}: {e}")
            raise e

    async def create_produtor(self, produtor_data: ProdutorCreate) -> ReturnSucess:
        """Cria um novo produtor"""
        try:
            # Verificar se já existe um produtor com o mesmo CPF
            existing_produtor = self.brain_agriculture_repository.get_produtor_by_cpf(produtor_data.cpf)
            if existing_produtor:
                return ReturnSucess(
                    success=False,
                    message="Já existe um produtor cadastrado com este CPF",
                    data={}
                )
            
            # Criar o produtor no banco
            produtor_model = ProdutorModel(
                cpf=produtor_data.cpf,
                nomeprodutor=produtor_data.nomeprodutor
            )
            
            created_produtor = self.brain_agriculture_repository.create_produtor(produtor_model)
            
            return ReturnSucess(
                success=True,
                message="Produtor criado com sucesso",
                data={"id": created_produtor.id, "cpf": created_produtor.cpf, "nome": created_produtor.nomeprodutor}
            )
        except Exception as e:
            logger.error(f"Erro ao criar produtor: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao criar produtor: {str(e)}",
                data={}
            )

    async def update_produtor(self, produtor_id: int, produtor_data: dict) -> ReturnSucess:
        """Atualiza um produtor existente"""
        try:
            # Verificar se o produtor existe
            existing_produtor = self.brain_agriculture_repository.get_produtor_by_id(produtor_id)
            if not existing_produtor:
                return ReturnSucess(
                    success=False,
                    message="Produtor não encontrado",
                    data={}
                )
            
            # Se estiver atualizando o CPF, verificar se não existe outro com o mesmo CPF
            if 'cpf' in produtor_data:
                cpf_produtor = self.brain_agriculture_repository.get_produtor_by_cpf(produtor_data['cpf'])
                if cpf_produtor and cpf_produtor.id != produtor_id:
                    return ReturnSucess(
                        success=False,
                        message="Já existe outro produtor cadastrado com este CPF",
                        data={}
                    )
            
            updated_produtor = self.brain_agriculture_repository.update_produtor(produtor_id, produtor_data)
            
            if updated_produtor:
                return ReturnSucess(
                    success=True,
                    message="Produtor atualizado com sucesso",
                    data={"id": updated_produtor.id, "cpf": updated_produtor.cpf, "nome": updated_produtor.nomeprodutor}
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao atualizar produtor",
                    data={}
                )
        except Exception as e:
            logger.error(f"Erro ao atualizar produtor {produtor_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao atualizar produtor: {str(e)}",
                data={}
            )

    async def delete_produtor(self, produtor_id: int) -> ReturnSucess:
        """Exclui um produtor"""
        try:
            # Verificar se o produtor existe
            existing_produtor = self.brain_agriculture_repository.get_produtor_by_id(produtor_id)
            if not existing_produtor:
                return ReturnSucess(
                    success=False,
                    message="Produtor não encontrado",
                    data={}
                )
            
            success = self.brain_agriculture_repository.delete_produtor(produtor_id)
            
            if success:
                return ReturnSucess(
                    success=True,
                    message="Produtor excluído com sucesso",
                    data={"id": produtor_id}
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao excluir produtor",
                    data={}
                )
        except Exception as e:
            logger.error(f"Erro ao excluir produtor {produtor_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao excluir produtor: {str(e)}",
                data={}
            )

    # Métodos CRUD para Fazendas
    async def get_all_fazendas(self) -> List[Fazenda]:
        """Busca todas as fazendas"""
        try:
            fazendas = self.brain_agriculture_repository.get_all_fazendas()
            return [Fazenda.from_orm(fazenda) for fazenda in fazendas]
        except Exception as e:
            logger.error(f"Erro ao buscar fazendas: {e}")
            raise e

    async def get_fazenda_by_id(self, fazenda_id: int) -> Optional[Fazenda]:
        """Busca uma fazenda pelo ID"""
        try:
            fazenda = self.brain_agriculture_repository.get_fazenda_by_id(fazenda_id)
            if fazenda:
                return Fazenda.from_orm(fazenda)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar fazenda {fazenda_id}: {e}")
            raise e

    async def get_fazendas_by_produtor(self, produtor_id: int) -> List[Fazenda]:
        """Busca fazendas de um produtor específico"""
        try:
            fazendas = self.brain_agriculture_repository.get_fazendas_by_produtor(produtor_id)
            return [Fazenda.from_orm(fazenda) for fazenda in fazendas]
        except Exception as e:
            logger.error(f"Erro ao buscar fazendas do produtor {produtor_id}: {e}")
            raise e

    async def create_fazenda(self, fazenda_data: FazendaCreate) -> ReturnSucess:
        """Cria uma nova fazenda"""
        try:
            # Verificar se o produtor existe (se idprodutor foi fornecido)
            if fazenda_data.idprodutor is not None:
                produtor = self.brain_agriculture_repository.get_produtor_by_id(fazenda_data.idprodutor)
                if not produtor:
                    return ReturnSucess(
                        success=False,
                        message="Produtor não encontrado",
                        data={}
                    )
                produtor_id = fazenda_data.idprodutor
            else:
                return ReturnSucess(
                    success=False,
                    message="ID do produtor é obrigatório para criar uma fazenda",
                    data={}
                )
            
            # Criar a fazenda no banco
            fazenda_model = FazendaModel(
                nomefazenda=fazenda_data.nomefazenda,
                cidade=fazenda_data.cidade,
                estado=fazenda_data.estado,
                areatotalfazenda=fazenda_data.areatotalfazenda,
                areaagricutavel=fazenda_data.areaagricutavel,
                idprodutor=produtor_id
            )
            
            created_fazenda = self.brain_agriculture_repository.create_fazenda(fazenda_model)
            
            return ReturnSucess(
                success=True,
                message="Fazenda criada com sucesso",
                data={"id": created_fazenda.id, "nome": created_fazenda.nomefazenda, "cidade": created_fazenda.cidade}
            )
        except Exception as e:
            logger.error(f"Erro ao criar fazenda: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao criar fazenda: {str(e)}",
                data={}
            )

    async def update_fazenda(self, fazenda_id: int, fazenda_data: dict) -> ReturnSucess:
        """Atualiza uma fazenda existente"""
        try:
            # Verificar se a fazenda existe
            existing_fazenda = self.brain_agriculture_repository.get_fazenda_by_id(fazenda_id)
            if not existing_fazenda:
                return ReturnSucess(
                    success=False,
                    message="Fazenda não encontrada",
                    data={}
                )
            
            # Se estiver atualizando o produtor, verificar se existe
            if 'idprodutor' in fazenda_data and fazenda_data['idprodutor'] is not None:
                produtor = self.brain_agriculture_repository.get_produtor_by_id(fazenda_data['idprodutor'])
                if not produtor:
                    return ReturnSucess(
                        success=False,
                        message="Produtor não encontrado",
                        data={}
                    )
            
            updated_fazenda = self.brain_agriculture_repository.update_fazenda(fazenda_id, fazenda_data)
            
            if updated_fazenda:
                return ReturnSucess(
                    success=True,
                    message="Fazenda atualizada com sucesso",
                    data={"id": updated_fazenda.id, "nome": updated_fazenda.nomefazenda, "cidade": updated_fazenda.cidade}
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao atualizar fazenda",
                    data={}
                )
        except Exception as e:
            logger.error(f"Erro ao atualizar fazenda {fazenda_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao atualizar fazenda: {str(e)}",
                data={}
            )

    async def delete_fazenda(self, fazenda_id: int) -> ReturnSucess:
        """Exclui uma fazenda"""
        try:
            # Verificar se a fazenda existe
            existing_fazenda = self.brain_agriculture_repository.get_fazenda_by_id(fazenda_id)
            if not existing_fazenda:
                return ReturnSucess(
                    success=False,
                    message="Fazenda não encontrada",
                    data={}
                )
            
            success = self.brain_agriculture_repository.delete_fazenda(fazenda_id)
            
            if success:
                return ReturnSucess(
                    success=True,
                    message="Fazenda excluída com sucesso",
                    data={"id": fazenda_id}
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao excluir fazenda",
                    data={}
                )
        except Exception as e:
            logger.error(f"Erro ao excluir fazenda {fazenda_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao excluir fazenda: {str(e)}",
                data={}
            )

    # Métodos CRUD para Safras
    async def get_all_safras(self) -> List[Safra]:
        """Busca todas as safras"""
        try:
            safras = self.brain_agriculture_repository.get_all_safras()
            return [Safra.from_orm(safra) for safra in safras]
        except Exception as e:
            logger.error(f"Erro ao buscar safras: {e}")
            raise e

    async def get_safra_by_id(self, safra_id: int) -> Optional[Safra]:
        """Busca uma safra pelo ID"""
        try:
            safra = self.brain_agriculture_repository.get_safra_by_id(safra_id)
            if safra:
                return Safra.from_orm(safra)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar safra {safra_id}: {e}")
            raise e

    async def get_safras_by_fazenda(self, fazenda_id: int) -> List[Safra]:
        """Busca safras de uma fazenda específica"""
        try:
            safras = self.brain_agriculture_repository.get_safras_by_fazenda(fazenda_id)
            return [Safra.from_orm(safra) for safra in safras]
        except Exception as e:
            logger.error(f"Erro ao buscar safras da fazenda {fazenda_id}: {e}")
            raise e

    async def get_safras_by_ano(self, ano: int) -> List[Safra]:
        """Busca safras por ano"""
        try:
            safras = self.brain_agriculture_repository.get_safras_by_ano(ano)
            return [Safra.from_orm(safra) for safra in safras]
        except Exception as e:
            logger.error(f"Erro ao buscar safras do ano {ano}: {e}")
            raise e

    async def create_safra(self, safra_data: SafraCreate) -> ReturnSucess:
        """Cria uma nova safra"""
        try:
            # Verificar se a fazenda existe
            fazenda = self.brain_agriculture_repository.get_fazenda_by_id(safra_data.idfazenda)
            if not fazenda:
                return ReturnSucess(
                    success=False,
                    message="Fazenda não encontrada",
                    data={}
                )
            
            # Criar a safra no banco
            safra_model = SafraModel(
                ano=safra_data.ano,
                cultura=safra_data.cultura,
                idfazenda=safra_data.idfazenda
            )
            
            created_safra = self.brain_agriculture_repository.create_safra(safra_model)
            
            return ReturnSucess(
                success=True,
                message="Safra criada com sucesso",
                data={"id": created_safra.id, "ano": created_safra.ano, "cultura": created_safra.cultura}
            )
        except Exception as e:
            logger.error(f"Erro ao criar safra: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao criar safra: {str(e)}",
                data={}
            )

    async def update_safra(self, safra_id: int, safra_data: dict) -> ReturnSucess:
        """Atualiza uma safra existente"""
        try:
            # Verificar se a safra existe
            existing_safra = self.brain_agriculture_repository.get_safra_by_id(safra_id)
            if not existing_safra:
                return ReturnSucess(
                    success=False,
                    message="Safra não encontrada",
                    data={}
                )
            
            # Se estiver atualizando a fazenda, verificar se existe
            if 'idfazenda' in safra_data:
                fazenda = self.brain_agriculture_repository.get_fazenda_by_id(safra_data['idfazenda'])
                if not fazenda:
                    return ReturnSucess(
                        success=False,
                        message="Fazenda não encontrada",
                        data={}
                    )
            
            updated_safra = self.brain_agriculture_repository.update_safra(safra_id, safra_data)
            
            if updated_safra:
                return ReturnSucess(
                    success=True,
                    message="Safra atualizada com sucesso",
                    data={"id": updated_safra.id, "ano": updated_safra.ano, "cultura": updated_safra.cultura}
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao atualizar safra",
                    data={}
                )
        except Exception as e:
            logger.error(f"Erro ao atualizar safra {safra_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao atualizar safra: {str(e)}",
                data={}
            )

    async def delete_safra(self, safra_id: int) -> ReturnSucess:
        """Exclui uma safra"""
        try:
            # Verificar se a safra existe
            existing_safra = self.brain_agriculture_repository.get_safra_by_id(safra_id)
            if not existing_safra:
                return ReturnSucess(
                    success=False,
                    message="Safra não encontrada",
                    data={}
                )
            
            success = self.brain_agriculture_repository.delete_safra(safra_id)
            
            if success:
                return ReturnSucess(
                    success=True,
                    message="Safra excluída com sucesso",
                    data={"id": safra_id}
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao excluir safra",
                    data={}
                )
        except Exception as e:
            logger.error(f"Erro ao excluir safra {safra_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro ao excluir safra: {str(e)}",
                data={}
            )

    async def get_estatisticas_fazendas(self) -> EstatisticasFazendas:
        """Busca estatísticas de fazendas por estado e total"""
        try:
            # Buscar fazendas por estado
            fazendas_por_estado_data = self.brain_agriculture_repository.get_fazendas_por_estado()
            
            # Buscar total de fazendas
            total_fazendas = self.brain_agriculture_repository.get_total_fazendas()
            
            # Converter para schemas
            fazendas_por_estado = [
                FazendaPorEstado(estado=item["estado"], quantidade=item["quantidade"])
                for item in fazendas_por_estado_data
            ]
            
            return EstatisticasFazendas(
                total_fazendas=total_fazendas,
                fazendas_por_estado=fazendas_por_estado
            )
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas de fazendas: {e}")
            raise e

    async def get_estatisticas_culturas(self) -> EstatisticasCulturas:
        """Busca estatísticas de culturas plantadas (total e por cultura)"""
        try:
            total_culturas = self.brain_agriculture_repository.get_total_culturas()
            culturas_agrupadas = self.brain_agriculture_repository.get_culturas_agrupadas()
            culturas = [CulturaQuantidade(**item) for item in culturas_agrupadas]
            return EstatisticasCulturas(
                total_culturas=total_culturas,
                culturas=culturas
            )
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas de culturas: {e}")
            raise e

    async def get_estatisticas_areas(self) -> EstatisticasAreas:
        """Busca estatísticas de áreas das fazendas (total, agricultável e vegetação)"""
        try:
            areas_data = self.brain_agriculture_repository.get_estatisticas_areas()
            return EstatisticasAreas(**areas_data)
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas de áreas: {e}")
            raise e

    async def get_resumo_fazendas(self) -> ResumoFazendas:
        """Busca resumo simplificado: total de fazendas e área total cadastrada"""
        try:
            total_fazendas = self.brain_agriculture_repository.get_total_fazendas()
            areas_data = self.brain_agriculture_repository.get_estatisticas_areas()
            total_area = areas_data["area_total"]
            
            return ResumoFazendas(
                total_fazendas=total_fazendas,
                total_area=total_area
            )
        except Exception as e:
            logger.error(f"Erro ao buscar resumo de fazendas: {e}")
            raise e

    async def get_fazendas_resumidas(self) -> List[FazendaResumida]:
        """Busca lista resumida de fazendas (ID e nome)"""
        try:
            fazendas = self.brain_agriculture_repository.get_all_fazendas()
            return [
                FazendaResumida(id=fazenda.id, nomefazenda=fazenda.nomefazenda)
                for fazenda in fazendas
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar fazendas resumidas: {e}")
            raise e

    async def get_produtores_resumidos(self) -> List[ProdutorResumido]:
        """Busca lista resumida de produtores (ID, CPF e nome)"""
        try:
            produtores = self.brain_agriculture_repository.get_all_produtores()
            return [
                ProdutorResumido(id=produtor.id, cpf=produtor.cpf, nomeprodutor=produtor.nomeprodutor)
                for produtor in produtores
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar produtores resumidos: {e}")
            raise e

    async def processar_dados_completos(self, dados: DadosCompletosCreate) -> DadosCompletosResponse:
        """Processa dados completos de produtor, fazenda e safra de forma hierárquica"""
        try:
            # A validação já é feita automaticamente pelo Pydantic
            produtor_id = None
            fazenda_id = None
            safra_id = None
            
            # 1. Salvar produtor primeiro (se fornecido)
            if dados.produtor:
                logger.info("Processando dados do produtor")
                
                # Verificar se já existe um produtor com o mesmo CPF
                existing_produtor = self.brain_agriculture_repository.get_produtor_by_cpf(dados.produtor.cpf)
                if existing_produtor:
                    produtor_id = existing_produtor.id
                    logger.info(f"Produtor já existe com ID: {produtor_id}")
                else:
                    # Criar novo produtor
                    produtor_model = ProdutorModel(
                        cpf=dados.produtor.cpf,
                        nomeprodutor=dados.produtor.nomeprodutor
                    )
                    created_produtor = self.brain_agriculture_repository.create_produtor(produtor_model)
                    produtor_id = created_produtor.id
                    logger.info(f"Produtor criado com ID: {produtor_id}")
            
            # 2. Salvar fazenda (se fornecida)
            if dados.fazenda:
                logger.info("Processando dados da fazenda")
                
                # Se não temos produtor_id ainda, usar o idprodutor fornecido
                if produtor_id is None:
                    if dados.fazenda.idprodutor is None:
                        return DadosCompletosResponse(
                            success=False,
                            message="É necessário fornecer um produtor ou o ID do produtor na fazenda",
                            data={}
                        )
                    produtor_id = dados.fazenda.idprodutor
                    # Verificar se o produtor existe
                    produtor = self.brain_agriculture_repository.get_produtor_by_id(produtor_id)
                    if not produtor:
                        return DadosCompletosResponse(
                            success=False,
                            message=f"Produtor com ID {produtor_id} não encontrado",
                            data={}
                        )
                else:
                    # Usar o produtor_id que acabamos de criar/obter
                    produtor_id = produtor_id
                
                # Criar fazenda
                fazenda_model = FazendaModel(
                    nomefazenda=dados.fazenda.nomefazenda,
                    cidade=dados.fazenda.cidade,
                    estado=dados.fazenda.estado,
                    areatotalfazenda=dados.fazenda.areatotalfazenda,
                    areaagricutavel=dados.fazenda.areaagricutavel,
                    idprodutor=produtor_id
                )
                created_fazenda = self.brain_agriculture_repository.create_fazenda(fazenda_model)
                fazenda_id = created_fazenda.id
                logger.info(f"Fazenda criada com ID: {fazenda_id}")
            
            # 3. Salvar safra (se fornecida)
            if dados.safra:
                logger.info("Processando dados da safra")
                
                # Se não temos fazenda_id ainda, usar o idfazenda fornecido
                if fazenda_id is None:
                    fazenda_id = dados.safra.idfazenda
                    # Verificar se a fazenda existe
                    fazenda = self.brain_agriculture_repository.get_fazenda_by_id(fazenda_id)
                    if not fazenda:
                        return DadosCompletosResponse(
                            success=False,
                            message=f"Fazenda com ID {fazenda_id} não encontrada",
                            data={}
                        )
                else:
                    # Usar o fazenda_id que acabamos de criar
                    fazenda_id = fazenda_id
                
                # Criar safra
                safra_model = SafraModel(
                    ano=dados.safra.ano,
                    cultura=dados.safra.cultura,
                    idfazenda=fazenda_id
                )
                created_safra = self.brain_agriculture_repository.create_safra(safra_model)
                safra_id = created_safra.id
                logger.info(f"Safra criada com ID: {safra_id}")
            
            # Preparar resposta
            response_data = {}
            if produtor_id:
                response_data["produtor_id"] = produtor_id
            if fazenda_id:
                response_data["fazenda_id"] = fazenda_id
            if safra_id:
                response_data["safra_id"] = safra_id
            
            return DadosCompletosResponse(
                success=True,
                message="Dados processados e salvos com sucesso",
                data=response_data
            )
            
        except Exception as e:
            logger.error(f"Erro ao processar dados completos: {e}")
            return DadosCompletosResponse(
                success=False,
                message=f"Erro interno ao processar dados: {str(e)}",
                data={}
            )

    async def get_produtor_completo(self, produtor_id: int) -> Optional[ProdutorCompleto]:
        """Busca um produtor completo com suas fazendas e safras"""
        try:
            # Buscar o produtor
            produtor = self.brain_agriculture_repository.get_produtor_by_id(produtor_id)
            if not produtor:
                return None
            
            # Buscar fazendas do produtor
            fazendas = self.brain_agriculture_repository.get_fazendas_by_produtor(produtor_id)
            
            # Para cada fazenda, buscar suas safras
            fazendas_com_safras = []
            for fazenda in fazendas:
                safras = self.brain_agriculture_repository.get_safras_by_fazenda(fazenda.id)
                
                # Converter safras para schema
                safras_schema = [Safra.from_orm(safra) for safra in safras]
                
                # Criar fazenda com safras
                fazenda_com_safras = FazendaComSafras(
                    id=fazenda.id,
                    nomefazenda=fazenda.nomefazenda,
                    cidade=fazenda.cidade,
                    estado=fazenda.estado,
                    areatotalfazenda=fazenda.areatotalfazenda,
                    areaagricutavel=fazenda.areaagricutavel,
                    idprodutor=fazenda.idprodutor,
                    safras=safras_schema
                )
                fazendas_com_safras.append(fazenda_com_safras)
            
            # Criar produtor completo
            produtor_completo = ProdutorCompleto(
                id=produtor.id,
                cpf=produtor.cpf,
                nomeprodutor=produtor.nomeprodutor,
                fazendas=fazendas_com_safras
            )
            
            return produtor_completo
            
        except Exception as e:
            logger.error(f"Erro ao buscar produtor completo {produtor_id}: {e}")
            raise e

    async def get_fazenda_completa(self, fazenda_id: int) -> Optional[FazendaCompleta]:
        """Busca uma fazenda completa com suas safras"""
        try:
            # Buscar a fazenda
            fazenda = self.brain_agriculture_repository.get_fazenda_by_id(fazenda_id)
            if not fazenda:
                return None
            
            # Buscar safras da fazenda
            safras = self.brain_agriculture_repository.get_safras_by_fazenda(fazenda_id)
            
            # Converter safras para schema
            safras_schema = [Safra.from_orm(safra) for safra in safras]
            
            # Criar fazenda completa
            fazenda_completa = FazendaCompleta(
                id=fazenda.id,
                nomefazenda=fazenda.nomefazenda,
                cidade=fazenda.cidade,
                estado=fazenda.estado,
                areatotalfazenda=fazenda.areatotalfazenda,
                areaagricutavel=fazenda.areaagricutavel,
                idprodutor=fazenda.idprodutor,
                safras=safras_schema
            )
            
            return fazenda_completa
            
        except Exception as e:
            logger.error(f"Erro ao buscar fazenda completa {fazenda_id}: {e}")
            raise e

    async def vincular_fazenda_produtor(self, dados: VincularFazendaProdutor) -> ReturnSucess:
        """Vincula uma fazenda a um produtor"""
        try:
            # Verificar se a fazenda existe
            fazenda = self.brain_agriculture_repository.get_fazenda_by_id(dados.fazenda_id)
            if not fazenda:
                return ReturnSucess(
                    success=False,
                    message=f"Fazenda com ID {dados.fazenda_id} não encontrada",
                    data={}
                )
            
            # Verificar se o produtor existe
            produtor = self.brain_agriculture_repository.get_produtor_by_id(dados.produtor_id)
            if not produtor:
                return ReturnSucess(
                    success=False,
                    message=f"Produtor com ID {dados.produtor_id} não encontrado",
                    data={}
                )
            
            # Atualizar a fazenda com o novo produtor
            update_data = {"idprodutor": dados.produtor_id}
            updated_fazenda = self.brain_agriculture_repository.update_fazenda(dados.fazenda_id, update_data)
            
            if updated_fazenda:
                return ReturnSucess(
                    success=True,
                    message=f"Fazenda '{updated_fazenda.nomefazenda}' vinculada com sucesso ao produtor '{produtor.nomeprodutor}'",
                    data={
                        "fazenda_id": updated_fazenda.id,
                        "fazenda_nome": updated_fazenda.nomefazenda,
                        "produtor_id": produtor.id,
                        "produtor_nome": produtor.nomeprodutor
                    }
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao vincular fazenda ao produtor",
                    data={}
                )
                
        except Exception as e:
            logger.error(f"Erro ao vincular fazenda {dados.fazenda_id} ao produtor {dados.produtor_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro interno ao vincular fazenda ao produtor: {str(e)}",
                data={}
            )

    async def vincular_produtor_fazenda(self, dados: VincularProdutorFazenda) -> ReturnSucess:
        """Vincula um produtor a uma fazenda (mesma funcionalidade da anterior, mas com ordem diferente)"""
        try:
            # Verificar se o produtor existe
            produtor = self.brain_agriculture_repository.get_produtor_by_id(dados.produtor_id)
            if not produtor:
                return ReturnSucess(
                    success=False,
                    message=f"Produtor com ID {dados.produtor_id} não encontrado",
                    data={}
                )
            
            # Verificar se a fazenda existe
            fazenda = self.brain_agriculture_repository.get_fazenda_by_id(dados.fazenda_id)
            if not fazenda:
                return ReturnSucess(
                    success=False,
                    message=f"Fazenda com ID {dados.fazenda_id} não encontrada",
                    data={}
                )
            
            # Atualizar a fazenda com o novo produtor
            update_data = {"idprodutor": dados.produtor_id}
            updated_fazenda = self.brain_agriculture_repository.update_fazenda(dados.fazenda_id, update_data)
            
            if updated_fazenda:
                return ReturnSucess(
                    success=True,
                    message=f"Produtor '{produtor.nomeprodutor}' vinculado com sucesso à fazenda '{updated_fazenda.nomefazenda}'",
                    data={
                        "produtor_id": produtor.id,
                        "produtor_nome": produtor.nomeprodutor,
                        "fazenda_id": updated_fazenda.id,
                        "fazenda_nome": updated_fazenda.nomefazenda
                    }
                )
            else:
                return ReturnSucess(
                    success=False,
                    message="Erro ao vincular produtor à fazenda",
                    data={}
                )
                
        except Exception as e:
            logger.error(f"Erro ao vincular produtor {dados.produtor_id} à fazenda {dados.fazenda_id}: {e}")
            return ReturnSucess(
                success=False,
                message=f"Erro interno ao vincular produtor à fazenda: {str(e)}",
                data={}
            )

    
