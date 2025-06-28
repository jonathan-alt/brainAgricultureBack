from __future__ import annotations


from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

class Produtor(BaseModel):
    id: Optional[int] = Field(example=1, description="ID do produtor")
    cpf: str = Field(example="285.487.490-08", description="CPF do produtor")
    nomeprodutor: str = Field(example="Marcos Fernando de Souza", description="Nome do produtor")


class Fazenda(BaseModel):
    id: Optional[int] = Field(example=2, description="ID da fazenda")
    nomefazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    cidade: str = Field(example="Recife", description="Cidade da fazenda")
    estado: str = Field(example="Pernambuco", description="Estado da fazenda")
    areatotalfazenda: float = Field(example=8.5  , description="Área total a fazenda em hectare")
    areaagricutav: float = Field(example=8.5, description="Área agricultável em hectare")
    idprodutor: int = Field(example=1, description="ID do produtor (chave estrangeira)")


class Safra(BaseModel):
    id: Optional[int] = Field(example=1, description="ID da safra")
    ano: int = Field(example=2025, description="Ano da safra")
    cultura: str = Field(example="Soja", description="Cultura plantada")
    idfazenda: int = Field(example=1, description="ID da fazenda (chave estrangeira)")


class DadosFazenda(BaseModel):
    """Schema para dados de fazenda"""
    id: Optional[int] = Field(example=1, description="ID da visualização")
    fazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    # Adicione outros campos conforme necessário para sua visualização analítica


class ReturnSucess(BaseModel):
    """Schema para retorno de sucesso"""
    success: bool = Field(example=True, description="Indica se a operação foi bem-sucedida")
    message: str = Field(example="Operação realizada com sucesso", description="Mensagem de retorno")
    data: Optional[dict] = Field(example={}, description="Dados retornados")


class Brain_Agriculture(BaseModel):
    """Schema principal do Brain Agriculture"""
    id: Optional[int] = Field(example=1, description="ID do registro")
    fazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    # Adicione outros campos conforme necessário para sua aplicação


class ReceiveBrain_AgricultureSchema(BaseModel):
    """Schema para recebimento de dados do Brain Agriculture"""
    id: Optional[int] = Field(example=1, description="ID do registro")
    fazenda: str = Field(example="Fazenda Nova", description="Nome da fazenda")
    # Adicione outros campos conforme necessário para recebimento de dados
