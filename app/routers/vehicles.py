

from fastapi import APIRouter, HTTPException, Path, status

from app.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from app.repository.vehicle_repository import vehicle_repository

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

VEICULO_NAO_ENCONTRADO = "Veículo com ID {} não encontrado."


@router.get(
    "",
    response_model=list[Vehicle],
    summary="Listar todos os veículos",
    description="Retorna todos os veículos atualmente cadastrados no estoque.",
)
def listar_veiculos() -> list[Vehicle]:
    return vehicle_repository.listar_todos()


@router.get(
    "/{veiculo_id}",
    response_model=Vehicle,
    summary="Consultar veículo por ID",
    description="Retorna os dados de um único veículo, a partir do seu ID.",
    responses={404: {"description": "Veículo não encontrado."}},
)
def obter_veiculo(
    veiculo_id: int = Path(..., gt=0, description="ID do veículo desejado."),
) -> Vehicle:
    veiculo = vehicle_repository.buscar_por_id(veiculo_id)
    if veiculo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=VEICULO_NAO_ENCONTRADO.format(veiculo_id),
        )
    return veiculo


@router.post(
    "",
    response_model=Vehicle,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo veículo",
    description=(
        "Cadastra um novo veículo no estoque e retorna o registro criado, "
        "já com o ID gerado pela API."
    ),
)
def criar_veiculo(veiculo: VehicleCreate) -> Vehicle:
    return vehicle_repository.criar(veiculo)


@router.put(
    "/{veiculo_id}",
    response_model=Vehicle,
    summary="Atualizar veículo por ID",
    description=(
        "Atualiza todos os dados de um veículo existente. O corpo da "
        "requisição deve conter todos os campos, como em um novo cadastro."
    ),
    responses={404: {"description": "Veículo não encontrado."}},
)
def atualizar_veiculo(
    veiculo: VehicleUpdate,
    veiculo_id: int = Path(..., gt=0, description="ID do veículo a ser atualizado."),
) -> Vehicle:
    veiculo_atualizado = vehicle_repository.atualizar(veiculo_id, veiculo)
    if veiculo_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=VEICULO_NAO_ENCONTRADO.format(veiculo_id),
        )
    return veiculo_atualizado


@router.delete(
    "/{veiculo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir veículo por ID",
    description="Remove definitivamente um veículo do estoque.",
    responses={404: {"description": "Veículo não encontrado."}},
)
def excluir_veiculo(
    veiculo_id: int = Path(..., gt=0, description="ID do veículo a ser removido."),
) -> None:
    removido = vehicle_repository.remover(veiculo_id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=VEICULO_NAO_ENCONTRADO.format(veiculo_id),
        )