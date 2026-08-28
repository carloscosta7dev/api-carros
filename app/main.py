

from fastapi import FastAPI

from app.routers import vehicles

app = FastAPI(
    title="API de Estoque de Veículos",
    description=(
        "API REST para o gerenciamento do estoque de veículos de uma loja "
        "de automóveis, com um CRUD completo: cadastro, listagem, consulta, "
        "atualização e exclusão de veículos."
    ),
    version="1.0.0",
)

app.include_router(vehicles.router)


@app.get(
    "/",
    tags=["Status"],
    summary="Verifica se a API está no ar",
    description=(
        "Endpoint simples de status, útil para checar rapidamente se a "
        "aplicação está em execução."
    ),
)
def status_da_api() -> dict[str, str]:
    return {
        "status": "online",
        "mensagem": "API de Estoque de Veículos em execução.",
        "documentacao": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)