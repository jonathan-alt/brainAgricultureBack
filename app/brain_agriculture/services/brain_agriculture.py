import datetime as dt
import logging
import time
import uuid
import re
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
    EstatisticasSafrasPorAno,
    SafraPorAno,
)
from app.brain_agriculture.models.brain_agriculture import Produtor as ProdutorModel, Fazenda as FazendaModel, Safra as SafraModel

logger = logging.getLogger(__name__)


class Brain_AgricultureService(BaseService):
    def __init__(self, brain_agriculture_repository: Brain_AgricultureRepository):
        self.brain_agriculture_repository = brain_agriculture_repository
        super().__init__(brain_agriculture_repository)

    def _padronizar_cpf(self, cpf: str) -> str:
        """
        Padroniza o CPF removendo caracteres especiais e formatando como XXX.XXX.XXX-XX
        """
        # Remove todos os caracteres não numéricos
        cpf_limpo = re.sub(r'[^\d]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter 11 dígitos")
        
        # Formata como XXX.XXX.XXX-XX
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        
        return cpf_formatado

    def _verificar_cpf_existente(self, cpf: str, excluir_id: Optional[int] = None) -> Optional[Produtor]:
        """
        Verifica se já existe um produtor com o CPF fornecido
        Se excluir_id for fornecido, ignora esse ID na verificação (para updates)
        """
        try:
            cpf_padronizado = self._padronizar_cpf(cpf)
            existing_produtor = self.brain_agriculture_repository.get_produtor_by_cpf(cpf_padronizado)
            
            if existing_produtor and (excluir_id is None or existing_produtor.id != excluir_id):
                return existing_produtor
            
            return None
        except ValueError as e:
            logger.error(f"Erro ao padronizar CPF '{cpf}': {e}")
            raise e

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
            # Padronizar CPF
            cpf_padronizado = self._padronizar_cpf(produtor_data.cpf)
            
            # Verificar se já existe um produtor com o mesmo CPF
            existing_produtor = self._verificar_cpf_existente(cpf_padronizado)
            if existing_produtor:
                return ReturnSucess(
                    success=False,
                    message="Já existe um produtor cadastrado com este CPF",
                    data={}
                )
            
            # Criar o produtor no banco com CPF padronizado
            produtor_model = ProdutorModel(
                cpf=cpf_padronizado,
                nomeprodutor=produtor_data.nomeprodutor
            )
            
            created_produtor = self.brain_agriculture_repository.create_produtor(produtor_model)
            
            return ReturnSucess(
                success=True,
                message="Produtor criado com sucesso",
                data={"id": created_produtor.id, "cpf": created_produtor.cpf, "nome": created_produtor.nomeprodutor}
            )
        except ValueError as e:
            logger.error(f"Erro de validação do CPF: {e}")
            return ReturnSucess(
                success=False,
                message=f"CPF inválido: {str(e)}",
                data={}
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
            
            # Se estiver atualizando o CPF, padronizar e verificar duplicatas
            if 'cpf' in produtor_data:
                try:
                    cpf_padronizado = self._padronizar_cpf(produtor_data['cpf'])
                    # Verificar se existe outro produtor com o mesmo CPF (excluindo o atual)
                    duplicate_produtor = self._verificar_cpf_existente(cpf_padronizado, excluir_id=produtor_id)
                    if duplicate_produtor:
                        return ReturnSucess(
                            success=False,
                            message="Já existe outro produtor cadastrado com este CPF",
                            data={}
                        )
                    # Atualizar o CPF com a versão padronizada
                    produtor_data['cpf'] = cpf_padronizado
                except ValueError as e:
                    return ReturnSucess(
                        success=False,
                        message=f"CPF inválido: {str(e)}",
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
        """Exclui um produtor e todas as suas fazendas e safras em cascata"""
        try:
            # Verificar se o produtor existe
            existing_produtor = self.brain_agriculture_repository.get_produtor_by_id(produtor_id)
            if not existing_produtor:
                return ReturnSucess(
                    success=False,
                    message="Produtor não encontrado",
                    data={}
                )
            
            # 1. Buscar todas as fazendas do produtor
            fazendas = self.brain_agriculture_repository.get_fazendas_by_produtor(produtor_id)
            
            # 2. Para cada fazenda, excluir todas as safras
            safras_excluidas = 0
            for fazenda in fazendas:
                safras = self.brain_agriculture_repository.get_safras_by_fazenda(fazenda.id)
                for safra in safras:
                    self.brain_agriculture_repository.delete_safra(safra.id)
                    safras_excluidas += 1
                logger.info(f"Excluídas {len(safras)} safras da fazenda {fazenda.id}")
            
            # 3. Excluir todas as fazendas do produtor
            fazendas_excluidas = 0
            for fazenda in fazendas:
                self.brain_agriculture_repository.delete_fazenda(fazenda.id)
                fazendas_excluidas += 1
                logger.info(f"Excluída fazenda {fazenda.id}")
            
            # 4. Excluir o produtor
            success = self.brain_agriculture_repository.delete_produtor(produtor_id)
            
            if success:
                return ReturnSucess(
                    success=True,
                    message=f"Produtor excluído com sucesso. Foram excluídas {fazendas_excluidas} fazendas e {safras_excluidas} safras",
                    data={
                        "id": produtor_id,
                        "fazendas_excluidas": fazendas_excluidas,
                        "safras_excluidas": safras_excluidas
                    }
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
            # O idprodutor agora é gerenciado automaticamente pelo backend
            # Esta validação foi removida pois o campo não existe mais no schema
            
            # Criar a fazenda no banco
            fazenda_model = FazendaModel(
                nomefazenda=fazenda_data.nomefazenda,
                cidade=fazenda_data.cidade,
                estado=fazenda_data.estado,
                areatotalfazenda=fazenda_data.areatotalfazenda,
                areaagricutavel=fazenda_data.areaagricutavel,
                idprodutor=None  # Será definido quando a fazenda for vinculada a um produtor
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
        """Exclui uma fazenda e todas as suas safras em cascata"""
        try:
            # Verificar se a fazenda existe
            existing_fazenda = self.brain_agriculture_repository.get_fazenda_by_id(fazenda_id)
            if not existing_fazenda:
                return ReturnSucess(
                    success=False,
                    message="Fazenda não encontrada",
                    data={}
                )
            
            # 1. Buscar todas as safras da fazenda
            safras = self.brain_agriculture_repository.get_safras_by_fazenda(fazenda_id)
            
            # 2. Excluir todas as safras da fazenda
            safras_excluidas = 0
            for safra in safras:
                self.brain_agriculture_repository.delete_safra(safra.id)
                safras_excluidas += 1
                logger.info(f"Excluída safra {safra.id} da fazenda {fazenda_id}")
            
            # 3. Excluir a fazenda
            success = self.brain_agriculture_repository.delete_fazenda(fazenda_id)
            
            if success:
                return ReturnSucess(
                    success=True,
                    message=f"Fazenda excluída com sucesso. Foram excluídas {safras_excluidas} safras",
                    data={
                        "id": fazenda_id,
                        "safras_excluidas": safras_excluidas
                    }
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

    async def get_estatisticas_safras_por_ano(self) -> EstatisticasSafrasPorAno:
        """Busca estatísticas de safras agrupadas por ano"""
        try:
            safras_por_ano_data = self.brain_agriculture_repository.get_safras_por_ano()
            safras_por_ano = [SafraPorAno(**item) for item in safras_por_ano_data]
            return EstatisticasSafrasPorAno(safras_por_ano=safras_por_ano)
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas de safras por ano: {e}")
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
        """Processa dados completos de produtor, fazendas e safras de forma hierárquica com rollback"""
        created_produtor = None
        created_fazendas = []
        created_safras = []
        
        try:
            # O produtor é obrigatório, então sempre processamos primeiro
            produtor_id = None
            
            # 1. Salvar produtor (obrigatório)
            logger.info("Processando dados do produtor")
            
            # Padronizar CPF
            cpf_padronizado = self._padronizar_cpf(dados.produtor.cpf)
            
            # Verificar se já existe um produtor com o mesmo CPF
            existing_produtor = self.brain_agriculture_repository.get_produtor_by_cpf(cpf_padronizado)
            if existing_produtor:
                return DadosCompletosResponse(
                    success=False,
                    message="Já existe um produtor cadastrado com este CPF",
                    data={}
                )
            
            # Criar novo produtor com CPF padronizado
            produtor_model = ProdutorModel(
                cpf=cpf_padronizado,
                nomeprodutor=dados.produtor.nomeprodutor
            )
            created_produtor = self.brain_agriculture_repository.create_produtor(produtor_model)
            produtor_id = created_produtor.id
            logger.info(f"Produtor criado com ID: {produtor_id}")
            
            fazendas_ids = []
            safras_ids = []
            
            # 2. Processar fazendas (se fornecidas)
            if dados.fazendas:
                logger.info(f"Processando {len(dados.fazendas)} fazendas")
                
                for fazenda_data in dados.fazendas:
                    try:
                        # Verificar se a fazenda já existe para este produtor
                        existing_fazenda = self.brain_agriculture_repository.get_fazenda_by_nome_and_produtor(
                            fazenda_data.nomefazenda, produtor_id
                        )
                        
                        if existing_fazenda:
                            fazendas_ids.append(existing_fazenda.id)
                            logger.info(f"Fazenda '{fazenda_data.nomefazenda}' já existe com ID: {existing_fazenda.id}")
                        else:
                            # Criar nova fazenda vinculada ao produtor
                            fazenda_model = FazendaModel(
                                nomefazenda=fazenda_data.nomefazenda,
                                cidade=fazenda_data.cidade,
                                estado=fazenda_data.estado,
                                areatotalfazenda=fazenda_data.areatotalfazenda,
                                areaagricutavel=fazenda_data.areaagricutavel,
                                idprodutor=produtor_id
                            )
                            created_fazenda = self.brain_agriculture_repository.create_fazenda(fazenda_model)
                            created_fazendas.append(created_fazenda)
                            fazendas_ids.append(created_fazenda.id)
                            logger.info(f"Fazenda '{fazenda_data.nomefazenda}' criada com ID: {created_fazenda.id}")
                    except Exception as e:
                        logger.error(f"Erro ao criar fazenda '{fazenda_data.nomefazenda}': {e}")
                        # Fazer rollback de todas as fazendas criadas
                        await self._rollback_fazendas(created_fazendas)
                        if created_produtor:
                            await self._rollback_produtor(created_produtor)
                        return DadosCompletosResponse(
                            success=False,
                            message=f"Erro ao criar fazenda '{fazenda_data.nomefazenda}': {str(e)}",
                            data={}
                        )
            
            # 3. Processar safras (se fornecidas)
            if dados.safras:
                logger.info(f"Processando {len(dados.safras)} safras")
                
                # A validação já garante que fazendas existem, mas vamos verificar por segurança
                if not fazendas_ids:
                    await self._rollback_fazendas(created_fazendas)
                    if created_produtor:
                        await self._rollback_produtor(created_produtor)
                    return DadosCompletosResponse(
                        success=False,
                        message="Erro interno: safras fornecidas mas nenhuma fazenda foi encontrada/criada",
                        data={}
                    )
                
                # Criar um mapeamento de nome da fazenda para ID
                fazenda_nome_to_id = {}
                for fazenda_data in dados.fazendas:
                    # Verificar se a fazenda já existe para este produtor
                    existing_fazenda = self.brain_agriculture_repository.get_fazenda_by_nome_and_produtor(
                        fazenda_data.nomefazenda, produtor_id
                    )
                    if existing_fazenda:
                        fazenda_nome_to_id[fazenda_data.nomefazenda] = existing_fazenda.id
                    else:
                        # Buscar a fazenda criada na lista de fazendas criadas
                        for created_fazenda in created_fazendas:
                            if created_fazenda.nomefazenda == fazenda_data.nomefazenda:
                                fazenda_nome_to_id[fazenda_data.nomefazenda] = created_fazenda.id
                                break
                
                for safra_data in dados.safras:
                    try:
                        # Buscar o ID da fazenda pelo nome
                        if safra_data.nomefazenda not in fazenda_nome_to_id:
                            await self._rollback_safras(created_safras)
                            await self._rollback_fazendas(created_fazendas)
                            if created_produtor:
                                await self._rollback_produtor(created_produtor)
                            return DadosCompletosResponse(
                                success=False,
                                message=f"Fazenda '{safra_data.nomefazenda}' não encontrada para a safra {safra_data.ano}-{safra_data.cultura}",
                                data={}
                            )
                        
                        fazenda_id = fazenda_nome_to_id[safra_data.nomefazenda]
                        
                        # Criar safra vinculada à fazenda
                        safra_model = SafraModel(
                            ano=safra_data.ano,
                            cultura=safra_data.cultura,
                            idfazenda=fazenda_id
                        )
                        created_safra = self.brain_agriculture_repository.create_safra(safra_model)
                        created_safras.append(created_safra)
                        safras_ids.append(created_safra.id)
                        logger.info(f"Safra {safra_data.ano}-{safra_data.cultura} criada com ID: {created_safra.id} para fazenda '{safra_data.nomefazenda}' (ID: {fazenda_id})")
                    except Exception as e:
                        logger.error(f"Erro ao criar safra {safra_data.ano}-{safra_data.cultura}: {e}")
                        # Fazer rollback de todas as safras criadas
                        await self._rollback_safras(created_safras)
                        await self._rollback_fazendas(created_fazendas)
                        if created_produtor:
                            await self._rollback_produtor(created_produtor)
                        return DadosCompletosResponse(
                            success=False,
                            message=f"Erro ao criar safra {safra_data.ano}-{safra_data.cultura}: {str(e)}",
                            data={}
                        )
            
            # Preparar resposta
            response_data = {"produtor_id": produtor_id}
            if fazendas_ids:
                response_data["fazendas_ids"] = fazendas_ids
            if safras_ids:
                response_data["safras_ids"] = safras_ids
            
            return DadosCompletosResponse(
                success=True,
                message="Dados processados e salvos com sucesso",
                data=response_data
            )
            
        except ValueError as e:
            logger.error(f"Erro de validação do CPF: {e}")
            # Fazer rollback de tudo que foi criado
            await self._rollback_safras(created_safras)
            await self._rollback_fazendas(created_fazendas)
            if created_produtor:
                await self._rollback_produtor(created_produtor)
            return DadosCompletosResponse(
                success=False,
                message=f"CPF inválido: {str(e)}",
                data={}
            )
        except Exception as e:
            logger.error(f"Erro inesperado ao processar dados completos: {e}")
            # Fazer rollback de tudo que foi criado
            await self._rollback_safras(created_safras)
            await self._rollback_fazendas(created_fazendas)
            if created_produtor:
                await self._rollback_produtor(created_produtor)
            return DadosCompletosResponse(
                success=False,
                message=f"Erro interno ao processar dados: {str(e)}",
                data={}
            )

    async def _rollback_produtor(self, produtor):
        """Faz rollback de um produtor criado"""
        try:
            if produtor and produtor.id:
                logger.info(f"Fazendo rollback do produtor {produtor.id}")
                self.brain_agriculture_repository.delete_produtor(produtor.id)
        except Exception as e:
            logger.error(f"Erro ao fazer rollback do produtor {produtor.id if produtor else 'None'}: {e}")

    async def _rollback_fazendas(self, fazendas):
        """Faz rollback das fazendas criadas"""
        try:
            for fazenda in fazendas:
                if fazenda and fazenda.id:
                    logger.info(f"Fazendo rollback da fazenda {fazenda.id}")
                    self.brain_agriculture_repository.delete_fazenda(fazenda.id)
        except Exception as e:
            logger.error(f"Erro ao fazer rollback das fazendas: {e}")

    async def _rollback_safras(self, safras):
        """Faz rollback das safras criadas"""
        try:
            for safra in safras:
                if safra and safra.id:
                    logger.info(f"Fazendo rollback da safra {safra.id}")
                    self.brain_agriculture_repository.delete_safra(safra.id)
        except Exception as e:
            logger.error(f"Erro ao fazer rollback das safras: {e}")

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

    
