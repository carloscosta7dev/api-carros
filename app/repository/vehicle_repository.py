

from app.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate


class VehicleRepository:
    """Gerencia o armazenamento em memória dos veículos do estoque."""

    def __init__(self) -> None:
        self._veiculos: dict[int, Vehicle] = {}
        self._proximo_id: int = 1

    def listar_todos(self) -> list[Vehicle]:
        """Retorna todos os veículos cadastrados, na ordem de cadastro."""
        return list(self._veiculos.values())

    def buscar_por_id(self, veiculo_id: int) -> Vehicle | None:
        """Retorna um veículo pelo ID, ou None se ele não existir."""
        return self._veiculos.get(veiculo_id)

    def criar(self, dados: VehicleCreate) -> Vehicle:
        """Cria um novo veículo, atribuindo automaticamente um ID único."""
        novo_veiculo = Vehicle(id=self._proximo_id, **dados.model_dump())
        self._veiculos[self._proximo_id] = novo_veiculo
        self._proximo_id += 1
        return novo_veiculo

    def atualizar(self, veiculo_id: int, dados: VehicleUpdate) -> Vehicle | None:
        """Substitui os dados de um veículo existente.

        Retorna None caso o veículo não exista, para que o router decida
        como responder (normalmente com um erro 404).
        """
        if veiculo_id not in self._veiculos:
            return None

        veiculo_atualizado = Vehicle(id=veiculo_id, **dados.model_dump())
        self._veiculos[veiculo_id] = veiculo_atualizado
        return veiculo_atualizado

    def remover(self, veiculo_id: int) -> bool:
        """Remove um veículo do estoque. Retorna True se algo foi removido."""
        if veiculo_id not in self._veiculos:
            return False

        del self._veiculos[veiculo_id]
        return True


# Instância única, compartilhada por toda a aplicação (padrão singleton
# simples). Como não há banco de dados nesta versão, este objeto é quem
# guarda o "estado" do estoque enquanto a aplicação estiver em execução.
vehicle_repository = VehicleRepository()