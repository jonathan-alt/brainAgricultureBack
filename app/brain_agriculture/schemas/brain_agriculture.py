from __future__ import annotations


from typing import List, Optional
from uuid import UUID
import re

from pydantic import BaseModel, Field, ConfigDict, validator

# Schemas para criação (sem ID obrigatório)
class ProdutorCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
  
    cpf: str = Field(example="285.487.490-08", description="CPF do produtor")
    nomeprodutor: str = Field(example="Marcos Fernando de Souza", description="Nome do produtor")
    
    @validator('cpf')
    def validate_cpf(cls, v):
        """Valida se o CPF contém pelo menos 11 dígitos numéricos"""
        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r'[^\d]', '', v)
        
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter 11 dígitos numéricos")
        
        return v


class FazendaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    cidade: str = Field(example="Recife", description="Cidade da fazenda")
    estado: str = Field(example="Pernambuco", description="Estado da fazenda")
    areatotalfazenda: float = Field(example=8.5, description="Área total da fazenda em hectare")
    areaagricutavel: float = Field(example=8.5, description="Área agricultável em hectare")


class SafraCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    ano: int = Field(example=2025, description="Ano da safra")
    cultura: str = Field(example="Soja", description="Cultura plantada")
    idfazenda: int = Field(example=1, description="ID da fazenda (chave estrangeira)")


class SafraCreateComFazenda(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para criação de safra com especificação da fazenda por nome"""
    ano: int = Field(example=2025, description="Ano da safra")
    cultura: str = Field(example="Soja", description="Cultura plantada")
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda à qual a safra pertence")


# Schemas para resposta (com ID obrigatório)
class Produtor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
  
    id: int = Field(example=1, description="ID do produtor")
    cpf: str = Field(example="285.487.490-08", description="CPF do produtor")
    nomeprodutor: str = Field(example="Marcos Fernando de Souza", description="Nome do produtor")


class Fazenda(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(example=2, description="ID da fazenda")
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    cidade: str = Field(example="Recife", description="Cidade da fazenda")
    estado: str = Field(example="Pernambuco", description="Estado da fazenda")
    areatotalfazenda: float = Field(example=8.5, description="Área total da fazenda em hectare")
    areaagricutavel: float = Field(example=8.5, description="Área agricultável em hectare")
    idprodutor: Optional[int] = Field(default=None, example=1, description="ID do produtor (chave estrangeira)")


class Safra(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(example=1, description="ID da safra")
    ano: int = Field(example=2025, description="Ano da safra")
    cultura: str = Field(example="Soja", description="Cultura plantada")
    idfazenda: int = Field(example=1, description="ID da fazenda (chave estrangeira)")


class DadosFazenda(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para dados de fazenda"""
    id: Optional[int] = Field(example=1, description="ID da visualização")
    fazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    # Adicione outros campos conforme necessário para sua visualização analítica


class ReturnSucess(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para retorno de sucesso"""
    success: bool = Field(example=True, description="Indica se a operação foi bem-sucedida")
    message: str = Field(example="Operação realizada com sucesso", description="Mensagem de retorno")
    data: Optional[dict] = Field(example={}, description="Dados retornados")


class Brain_Agriculture(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema principal do Brain Agriculture"""
    id: Optional[int] = Field(example=1, description="ID do registro")
    fazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    # Adicione outros campos conforme necessário para sua aplicação


class ReceiveBrain_AgricultureSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para recebimento de dados do Brain Agriculture"""
    id: Optional[int] = Field(example=1, description="ID do registro")
    fazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    # Adicione outros campos conforme necessário para recebimento de dados


class FazendaPorEstado(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para estatística de fazendas por estado"""
    estado: str = Field(example="SP", description="Sigla do estado")
    quantidade: int = Field(example=5, description="Quantidade de fazendas no estado")


class EstatisticasFazendas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para estatísticas gerais de fazendas"""
    total_fazendas: int = Field(example=30, description="Total de fazendas")
    fazendas_por_estado: List[FazendaPorEstado] = Field(description="Lista de fazendas por estado")


class CulturaQuantidade(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    cultura: str = Field(example="Soja", description="Nome da cultura")
    quantidade: int = Field(example=10, description="Quantidade de safras dessa cultura")


class EstatisticasCulturas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    total_culturas: int = Field(example=30, description="Total de culturas plantadas (total de safras)")
    culturas: list[CulturaQuantidade] = Field(description="Lista de culturas e suas quantidades")


class SafraPorAno(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    ano: int = Field(example=2024, description="Ano da safra")
    quantidade: int = Field(example=15, description="Quantidade de safras nesse ano")


class EstatisticasSafrasPorAno(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    safras_por_ano: List[SafraPorAno] = Field(description="Lista de safras agrupadas por ano")


class EstatisticasAreas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    area_total: float = Field(example=1500.5, description="Área total somada de todas as fazendas em hectares")
    area_agricultavel: float = Field(example=1200.3, description="Área agricultável somada de todas as fazendas em hectares")
    area_vegetacao: float = Field(example=300.2, description="Área de vegetação (área total - área agricultável) em hectares")


class ResumoFazendas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    total_fazendas: int = Field(example=30, description="Total de fazendas cadastradas")
    total_area: float = Field(example=1500.5, description="Total de área cadastrada em hectares")


class FazendaResumida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(example=1, description="ID da fazenda")
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")


class ProdutorResumido(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(example=1, description="ID do produtor")
    cpf: str = Field(example="123.456.789-00", description="CPF do produtor")
    nomeprodutor: str = Field(example="João Silva", description="Nome do produtor")


class DadosCompletosCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """
    Schema para receber dados completos de produtor, fazendas e safras.
    - O campo 'safras' deve conter o nome da fazenda (campo 'nomefazenda') à qual a safra pertence.
    - O vínculo entre safra e fazenda é feito pelo nome da fazenda informado em cada safra.
    - O campo 'idprodutor' das fazendas é gerenciado automaticamente pelo backend.
    - Exemplo de payload:
      {
        "produtor": {"cpf": "123.456.789-00", "nomeprodutor": "João Silva"},
        "fazendas": [
          {"nomefazenda": "Fazenda A", "cidade": "São Paulo", "estado": "SP", "areatotalfazenda": 100.0, "areaagricutavel": 80.0},
          {"nomefazenda": "Fazenda B", "cidade": "Rio de Janeiro", "estado": "RJ", "areatotalfazenda": 150.0, "areaagricutavel": 120.0}
        ],
        "safras": [
          {"ano": 2025, "cultura": "Soja", "nomefazenda": "Fazenda A"},
          {"ano": 2025, "cultura": "Milho", "nomefazenda": "Fazenda B"}
        ]
      }
    """
    produtor: ProdutorCreate = Field(description="Dados do produtor (obrigatório)")
    fazendas: Optional[List[FazendaCreate]] = Field(default=None, description="Lista de fazendas (opcional). O campo idprodutor é gerenciado automaticamente pelo backend.")
    safras: Optional[List[SafraCreateComFazenda]] = Field(
        default=None,
        description="Lista de safras (opcional). Cada safra deve conter o campo 'nomefazenda' para indicar a qual fazenda pertence. O vínculo é feito pelo nome da fazenda."
    )
    
    @validator('safras')
    def validate_safras_require_fazendas(cls, v, values):
        """Valida que safras só podem vir se fazendas também vierem"""
        if v is not None and values.get('fazendas') is None:
            raise ValueError("Safras não podem ser enviadas sem fazendas. É necessário enviar fazendas junto com as safras.")
        return v


class DadosCompletosResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para resposta dos dados completos salvos"""
    success: bool = Field(example=True, description="Indica se a operação foi bem-sucedida")
    message: str = Field(example="Dados salvos com sucesso", description="Mensagem de retorno")
    data: dict = Field(example={
        "produtor_id": 1,
        "fazendas_ids": [2, 3, 4],
        "safras_ids": [5, 6, 7]
    }, description="IDs dos registros criados")


class FazendaComSafras(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para fazenda com suas safras"""
    id: int = Field(example=1, description="ID da fazenda")
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    cidade: str = Field(example="Recife", description="Cidade da fazenda")
    estado: str = Field(example="Pernambuco", description="Estado da fazenda")
    areatotalfazenda: float = Field(example=8.5, description="Área total da fazenda em hectare")
    areaagricutavel: float = Field(example=8.5, description="Área agricultável em hectare")
    idprodutor: Optional[int] = Field(default=None, example=1, description="ID do produtor (chave estrangeira)")
    safras: List[Safra] = Field(default=[], description="Lista de safras da fazenda")


class ProdutorCompleto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para produtor com suas fazendas e safras"""
    id: int = Field(example=1, description="ID do produtor")
    cpf: str = Field(example="285.487.490-08", description="CPF do produtor")
    nomeprodutor: str = Field(example="Marcos Fernando de Souza", description="Nome do produtor")
    fazendas: List[FazendaComSafras] = Field(default=[], description="Lista de fazendas do produtor com suas safras")


class FazendaCompleta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para fazenda completa com suas safras"""
    id: int = Field(example=1, description="ID da fazenda")
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    cidade: str = Field(example="Recife", description="Cidade da fazenda")
    estado: str = Field(example="Pernambuco", description="Estado da fazenda")
    areatotalfazenda: float = Field(example=8.5, description="Área total da fazenda em hectare")
    areaagricutavel: float = Field(example=8.5, description="Área agricultável em hectare")
    idprodutor: Optional[int] = Field(default=None, example=1, description="ID do produtor (chave estrangeira)")
    safras: List[Safra] = Field(default=[], description="Lista de safras da fazenda")


class VincularFazendaProdutor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para vincular uma fazenda a um produtor"""
    fazenda_id: int = Field(example=1, description="ID da fazenda")
    produtor_id: int = Field(example=1, description="ID do produtor")


class VincularProdutorFazenda(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    """Schema para vincular um produtor a uma fazenda"""
    produtor_id: int = Field(example=1, description="ID do produtor")
    fazenda_id: int = Field(example=1, description="ID da fazenda")
