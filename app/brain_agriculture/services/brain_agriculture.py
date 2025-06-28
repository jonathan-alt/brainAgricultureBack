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

    async def create_produtor(self, produtor_data: Produtor) -> ReturnSucess:
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

    async def create_fazenda(self, fazenda_data: Fazenda) -> ReturnSucess:
        """Cria uma nova fazenda"""
        try:
            # Verificar se o produtor existe
            produtor = self.brain_agriculture_repository.get_produtor_by_id(fazenda_data.idprodutor)
            if not produtor:
                return ReturnSucess(
                    success=False,
                    message="Produtor não encontrado",
                    data={}
                )
            
            # Criar a fazenda no banco
            fazenda_model = FazendaModel(
                nomefazenda=fazenda_data.nomefazenda,
                cidade=fazenda_data.cidade,
                estado=fazenda_data.estado,
                areatotalfazenda=fazenda_data.areatotalfazenda,
                areaagricutavel=fazenda_data.areaagricutavel,
                idprodutor=fazenda_data.idprodutor
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
            if 'idprodutor' in fazenda_data:
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

    async def create_safra(self, safra_data: Safra) -> ReturnSucess:
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
        """Busca lista resumida de produtores (ID e nome)"""
        try:
            produtores = self.brain_agriculture_repository.get_all_produtores()
            return [
                ProdutorResumido(id=produtor.id, nomeprodutor=produtor.nomeprodutor)
                for produtor in produtores
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar produtores resumidos: {e}")
            raise e

    
