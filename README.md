#  api-carros 

API REST desenvolvida em **Python** com **FastAPI** para o gerenciamento do estoque de veículos de uma loja de automóveis. Projeto construído como peça de portfólio, com foco em código limpo, organização de pastas profissional e boas práticas de desenvolvimento com FastAPI e Pydantic.

Este projeto implementa uma **API REST com operações CRUD completas para o gerenciamento de estoque de veículos** de uma loja de automóveis, permitindo cadastrar, listar, consultar, atualizar e excluir veículos.

Esta primeira versão foi construída propositalmente **sem banco de dados, autenticação, Docker ou deploy**, para manter o foco no que importa nesta etapa: um CRUD sólido, bem validado e bem organizado, usando FastAPI e Pydantic. Os dados ficam armazenados em memória durante a execução da aplicação.

## ✅ Funcionalidades

- [x] Cadastrar um novo veículo
- [x] Listar todos os veículos do estoque
- [x] Consultar um veículo específico por ID
- [x] Atualizar os dados de um veículo por ID
- [x] Excluir um veículo por ID
- [x] Validação completa dos dados de entrada com Pydantic
- [x] Tratamento de erros HTTP (404, 422)
- [x] Documentação interativa gerada automaticamente (Swagger UI e ReDoc)
- [x] Testes automatizados com pytest

##  Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| [Python 3.10+](https://www.python.org/) | Linguagem de programação |
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web para criação da API |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI utilizado para executar a aplicação |
| [Pydantic](https://docs.pydantic.dev/) | Validação e serialização dos dados |
| [Pytest](https://docs.pytest.org/) | Testes automatizados |
| Git & GitHub | Controle de versão e hospedagem do código |

##  Estrutura do projeto

```
estoque-veiculos-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Ponto de entrada (instância do FastAPI)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── vehicle.py              # Schemas Pydantic (VehicleCreate, VehicleUpdate, Vehicle)
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── vehicles.py             # Endpoints do CRUD de veículos
│   │
│   └── repository/
│       ├── __init__.py
│       └── vehicle_repository.py   # Camada de acesso a dados (armazenamento em memória)
│
├── tests/
│   ├── __init__.py
│   └── test_vehicles.py            # Testes automatizados dos endpoints
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

Essa organização separa claramente as responsabilidades do projeto:

- **`models/`** define *o quê* é um veículo e *quais dados são válidos*;
- **`routers/`** define *como* o cliente HTTP interage com os veículos;
- **`repository/`** define *onde e como* os veículos são armazenados;
- **`main.py`** conecta todas as peças e sobe a aplicação.

Essa separação facilita a manutenção e permite, por exemplo, trocar futuramente o armazenamento em memória por um banco de dados real sem alterar as rotas.

##  Modelo de dados

Cada veículo é representado pelos seguintes campos:

| Campo | Tipo | Obrigatório | Regras de validação |
|---|---|---|---|
| `id` | `int` | Gerado automaticamente | Não deve ser enviado pelo cliente |
| `marca` | `string` | Sim | 1 a 50 caracteres, não pode ser vazio |
| `modelo` | `string` | Sim | 1 a 50 caracteres, não pode ser vazio |
| `ano` | `int` | Sim | Entre 1886 e o ano atual + 1 |
| `cor` | `string` | Sim | 1 a 30 caracteres, não pode ser vazio |
| `quilometragem` | `float` | Sim | Maior ou igual a 0 |
| `preco` | `float` | Sim | Maior que 0 |
| `disponivel` | `bool` | Não (padrão: `true`) | — |

##  Pré-requisitos

- [Python 3.10 ou superior](https://www.python.org/downloads/) instalado
- [pip](https://pip.pypa.io/) (geralmente já vem com o Python)
- [Git](https://git-scm.com/) instalado

Verifique a sua versão do Python:

```bash
python --version
```

##  Instalação e execução

### 1. Clone o repositório

```bash
git clone https://github.com/carloscosta7dev/api-carros.git
cd api-carros```

### 2. Crie e ative um ambiente virtual

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
uvicorn app.main:app --reload
```

A flag `--reload` reinicia o servidor automaticamente a cada alteração no código (ótima para desenvolvimento; remova-a se não precisar desse comportamento).

A API estará disponível em:

```
http://localhost:8000
```

>  Alternativa: também é possível executar com `python -m app.main`, a partir da raiz do projeto, graças ao bloco `if __name__ == "__main__"` presente em `app/main.py`.

##  Documentação interativa

Assim que a aplicação estiver rodando, o FastAPI disponibiliza documentação interativa gerada automaticamente:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Esquema OpenAPI (JSON):** http://localhost:8000/openapi.json

Pelo Swagger UI é possível testar todos os endpoints diretamente pelo navegador, sem precisar de nenhuma ferramenta externa.

##  Endpoints da API

| Método | Rota | Descrição | Resposta de sucesso |
|---|---|---|---|
| `GET` | `/` | Verifica se a API está no ar | `200 OK` |
| `GET` | `/veiculos` | Lista todos os veículos | `200 OK` |
| `GET` | `/veiculos/{id}` | Consulta um veículo por ID | `200 OK` |
| `POST` | `/veiculos` | Cadastra um novo veículo | `201 Created` |
| `PUT` | `/veiculos/{id}` | Atualiza um veículo por ID | `200 OK` |
| `DELETE` | `/veiculos/{id}` | Exclui um veículo por ID | `204 No Content` |

##  Exemplos de requisições e respostas

### Cadastrar um veículo — `POST /veiculos`

**Requisição:**
```bash
curl -X POST "http://localhost:8000/veiculos" \
  -H "Content-Type: application/json" \
  -d '{
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2022,
        "cor": "Prata",
        "quilometragem": 15000,
        "preco": 98900.00,
        "disponivel": true
      }'
```

**Resposta `201 Created`:**
```json
{
  "marca": "Toyota",
  "modelo": "Corolla",
  "ano": 2022,
  "cor": "Prata",
  "quilometragem": 15000,
  "preco": 98900.0,
  "disponivel": true,
  "id": 1
}
```

### Listar todos os veículos — `GET /veiculos`

**Requisição:**
```bash
curl "http://localhost:8000/veiculos"
```

**Resposta `200 OK`:**
```json
[
  {
    "marca": "Toyota",
    "modelo": "Corolla",
    "ano": 2022,
    "cor": "Prata",
    "quilometragem": 15000,
    "preco": 98900.0,
    "disponivel": true,
    "id": 1
  }
]
```

### Consultar veículo por ID — `GET /veiculos/{id}`

**Requisição:**
```bash
curl "http://localhost:8000/veiculos/1"
```

**Resposta `200 OK`:** igual ao objeto retornado no cadastro.

**Se o ID não existir, resposta `404 Not Found`:**
```json
{
  "detail": "Veículo com ID 99 não encontrado."
}
```

### Atualizar veículo por ID — `PUT /veiculos/{id}`

> A atualização substitui o veículo por completo — envie todos os campos, mesmo os que não mudaram.

**Requisição:**
```bash
curl -X PUT "http://localhost:8000/veiculos/1" \
  -H "Content-Type: application/json" \
  -d '{
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2022,
        "cor": "Branco",
        "quilometragem": 20000,
        "preco": 95000.00,
        "disponivel": false
      }'
```

**Resposta `200 OK`:**
```json
{
  "marca": "Toyota",
  "modelo": "Corolla",
  "ano": 2022,
  "cor": "Branco",
  "quilometragem": 20000,
  "preco": 95000.0,
  "disponivel": false,
  "id": 1
}
```

### Excluir veículo por ID — `DELETE /veiculos/{id}`

**Requisição:**
```bash
curl -X DELETE "http://localhost:8000/veiculos/1"
```

**Resposta:** `204 No Content` (sem corpo na resposta)

##  Tratamento de erros

A API responde com códigos HTTP apropriados para cada situação:

| Situação | Código | Quando ocorre |
|---|---|---|
| Veículo não encontrado | `404 Not Found` | GET, PUT ou DELETE com um ID que não existe no estoque |
| Dados de entrada inválidos | `422 Unprocessable Entity` | POST ou PUT com campos ausentes, em branco ou fora das regras de validação |

**Exemplo — tentativa de cadastro com dados inválidos:**

```bash
curl -X POST "http://localhost:8000/veiculos" \
  -H "Content-Type: application/json" \
  -d '{
        "marca": "",
        "modelo": "Civic",
        "ano": 1500,
        "cor": "Preto",
        "quilometragem": -10,
        "preco": -5000,
        "disponivel": true
      }'
```

**Resposta `422 Unprocessable Entity` (formato simplificado; o FastAPI pode incluir campos adicionais, como `input` e `url`):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "marca"],
      "msg": "Value error, Este campo não pode ser vazio."
    },
    {
      "type": "value_error",
      "loc": ["body", "ano"],
      "msg": "Value error, O ano deve estar entre 1886 e 2027."
    },
    {
      "type": "greater_than_equal",
      "loc": ["body", "quilometragem"],
      "msg": "Input should be greater than or equal to 0"
    },
    {
      "type": "greater_than",
      "loc": ["body", "preco"],
      "msg": "Input should be greater than 0"
    }
  ]
}
```

Esse comportamento é gerado automaticamente pelo FastAPI a partir das validações declaradas nos schemas Pydantic (`app/models/vehicle.py`) — nenhum código adicional de tratamento é necessário para esses casos. Já os erros `404` são tratados explicitamente nas rotas (`app/routers/vehicles.py`), usando `HTTPException`.

##  Executando os testes

O projeto inclui testes automatizados cobrindo os principais fluxos do CRUD (casos de sucesso e de erro), usando `pytest` e o `TestClient` do FastAPI.

Com o ambiente virtual ativado e as dependências instaladas, execute a partir da raiz do projeto:

```bash
pytest
```

Para uma saída mais detalhada:

```bash
pytest -v
```

##  Limitações da versão atual

Esta é a primeira versão do projeto, com escopo intencionalmente reduzido:

- Os dados são armazenados **em memória** — todo o estoque é perdido quando a aplicação é reiniciada.
- Não há **autenticação** ou controle de acesso — todos os endpoints são públicos.
- Não há **banco de dados**, **Docker** ou **deploy** configurados.
- O armazenamento em memória não é seguro para múltiplos processos/workers simultâneos.

Essas limitações são propositais, para manter o foco em um CRUD bem construído nesta etapa do projeto.

##  Autor

Desenvolvido por carloscosta7dev.
- GitHub: https://github.com/carloscosta7dev/api-carros
- LinkedIn: www.linkedin.com/in/carlos-henrique-souza-costa-2b1aa23b6



