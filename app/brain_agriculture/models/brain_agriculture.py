from typing import Optional
from sqlmodel import SQLModel, Field


class Produtor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, description="ID do produtor")
    cpf: str = Field(index=True, description="CPF do produtor", max_length=20)
    nomeprodutor: str = Field(description="Nome do produtor", max_length=100)


class Fazenda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, description="ID da fazenda")
    nomefazenda: str = Field(description="Nome da fazenda", max_length=100)
    cidade: str = Field(description="Cidade da fazenda", max_length=100)
    estado: str = Field(description="Estado da fazenda", max_length=100)
    areatotalfazenda: float = Field(description="Área total da fazenda em hectare")
    areaagricutav: float = Field(description="Área agricultável em hectare")
    idprodutor: int = Field(foreign_key="produtor.id", description="ID do produtor (chave estrangeira)")


class Safra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, description="ID da safra")
    ano: int = Field(description="Ano da safra")
    cultura: str = Field(description="Cultura plantada", max_length=100)
    idfazenda: int = Field(foreign_key="fazenda.id", description="ID da fazenda (chave estrangeira)")
