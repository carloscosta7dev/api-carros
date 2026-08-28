

from fastapi.testclient import TestClient

from app.main import app
from app.repository.vehicle_repository import vehicle_repository

client = TestClient(app)


def setup_function() -> None:
    """Reinicia o estoque em memória antes de cada teste, para isolá-los."""
    vehicle_repository._veiculos.clear()
    vehicle_repository._proximo_id = 1


def _veiculo_valido(**sobrescreve) -> dict:
    """Monta um payload válido de veículo, permitindo sobrescrever campos."""
    payload = {
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2022,
        "cor": "Prata",
        "quilometragem": 15000,
        "preco": 98900.00,
        "disponivel": True,
    }
    payload.update(sobrescreve)
    return payload


def test_criar_veiculo_com_sucesso():
    resposta = client.post("/veiculos", json=_veiculo_valido())

    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["id"] == 1
    assert dados["marca"] == "Toyota"
    assert dados["disponivel"] is True


def test_criar_veiculo_com_ano_invalido_retorna_422():
    resposta = client.post("/veiculos", json=_veiculo_valido(ano=1800))
    assert resposta.status_code == 422


def test_criar_veiculo_com_preco_negativo_retorna_422():
    resposta = client.post("/veiculos", json=_veiculo_valido(preco=-100))
    assert resposta.status_code == 422


def test_criar_veiculo_com_marca_vazia_retorna_422():
    resposta = client.post("/veiculos", json=_veiculo_valido(marca="   "))
    assert resposta.status_code == 422


def test_listar_veiculos_quando_estoque_vazio():
    resposta = client.get("/veiculos")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listar_veiculos_apos_cadastro():
    client.post("/veiculos", json=_veiculo_valido())
    client.post("/veiculos", json=_veiculo_valido(modelo="Civic"))

    resposta = client.get("/veiculos")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_obter_veiculo_existente():
    criado = client.post("/veiculos", json=_veiculo_valido()).json()

    resposta = client.get(f"/veiculos/{criado['id']}")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == criado["id"]


def test_obter_veiculo_inexistente_retorna_404():
    resposta = client.get("/veiculos/999")
    assert resposta.status_code == 404


def test_atualizar_veiculo_existente():
    criado = client.post("/veiculos", json=_veiculo_valido()).json()

    novos_dados = _veiculo_valido(cor="Branco", disponivel=False)
    resposta = client.put(f"/veiculos/{criado['id']}", json=novos_dados)

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["cor"] == "Branco"
    assert dados["disponivel"] is False


def test_atualizar_veiculo_inexistente_retorna_404():
    resposta = client.put("/veiculos/999", json=_veiculo_valido())
    assert resposta.status_code == 404


def test_excluir_veiculo_existente():
    criado = client.post("/veiculos", json=_veiculo_valido()).json()

    resposta = client.delete(f"/veiculos/{criado['id']}")
    assert resposta.status_code == 204

    resposta_get = client.get(f"/veiculos/{criado['id']}")
    assert resposta_get.status_code == 404


def test_excluir_veiculo_inexistente_retorna_404():
    resposta = client.delete("/veiculos/999")
    assert resposta.status_code == 404