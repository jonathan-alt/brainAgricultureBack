from __future__ import annotations


from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

# Schemas para criação (sem ID obrigatório)
class ProdutorCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
  
    cpf: str = Field(example="285.487.490-08", description="CPF do produtor")
    nomeprodutor: str = Field(example="Marcos Fernando de Souza", description="Nome do produtor")


class FazendaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    cidade: str = Field(example="Recife", description="Cidade da fazenda")
    estado: str = Field(example="Pernambuco", description="Estado da fazenda")
    areatotalfazenda: float = Field(example=8.5, description="Área total da fazenda em hectare")
    areaagricutavel: float = Field(example=8.5, description="Área agricultável em hectare")
    idprodutor: int = Field(example=1, description="ID do produtor (chave estrangeira)")


class SafraCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    ano: int = Field(example=2025, description="Ano da safra")
    cultura: str = Field(example="Soja", description="Cultura plantada")
    idfazenda: int = Field(example=1, description="ID da fazenda (chave estrangeira)")


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
    idprodutor: int = Field(example=1, description="ID do produtor (chave estrangeira)")


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
    nomeprodutor: str = Field(example="João Silva", description="Nome do produtor")
