
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Ano do primeiro automóvel da história (Benz Patent-Motorwagen, 1886).
# Usado como limite inferior plausível para o campo "ano".
ANO_MINIMO_VEICULO = 1886


class VehicleBase(BaseModel):
    """Campos comuns a todas as operações de escrita de um veículo."""

    marca: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Marca do veículo.",
        examples=["Toyota"],
    )
    modelo: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Modelo do veículo.",
        examples=["Corolla"],
    )
    ano: int = Field(
        ...,
        description="Ano de fabricação do veículo.",
        examples=[2022],
    )
    cor: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Cor predominante do veículo.",
        examples=["Prata"],
    )
    quilometragem: float = Field(
        ...,
        ge=0,
        description="Quilometragem atual do veículo, em km.",
        examples=[15000],
    )
    preco: float = Field(
        ...,
        gt=0,
        description="Preço de venda do veículo, em reais (R$).",
        examples=[98900.00],
    )
    disponivel: bool = Field(
        default=True,
        description="Indica se o veículo está disponível para venda.",
        examples=[True],
    )

    @field_validator("marca", "modelo", "cor")
    @classmethod
    def campos_texto_nao_podem_ser_vazios(cls, valor: str) -> str:
        """Remove espaços das pontas e garante que o texto não fique vazio."""
        valor = valor.strip()
        if not valor:
            raise ValueError("Este campo não pode ser vazio.")
        return valor

    @field_validator("ano")
    @classmethod
    def ano_deve_ser_valido(cls, valor: int) -> int:
        """Garante que o ano informado esteja em um intervalo plausível."""
        ano_maximo = datetime.now().year + 1
        if valor < ANO_MINIMO_VEICULO or valor > ano_maximo:
            raise ValueError(
                f"O ano deve estar entre {ANO_MINIMO_VEICULO} e {ano_maximo}."
            )
        return valor

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2022,
                "cor": "Prata",
                "quilometragem": 15000,
                "preco": 98900.00,
                "disponivel": True,
            }
        }
    )


class VehicleCreate(VehicleBase):
    """Dados necessários para cadastrar um novo veículo."""


class VehicleUpdate(VehicleBase):
    """Dados necessários para atualizar um veículo existente.

    Todos os campos são obrigatórios: a atualização substitui o registro
    por completo (semântica de PUT), evitando ambiguidade sobre quais
    campos foram ou não enviados pelo cliente.
    """


class Vehicle(VehicleBase):
    """Representação completa de um veículo, devolvida pela API."""

    id: int = Field(
        ...,
        description="Identificador único do veículo, gerado pela API.",
        examples=[1],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2022,
                "cor": "Prata",
                "quilometragem": 15000,
                "preco": 98900.00,
                "disponivel": True,
            }
        }
    )