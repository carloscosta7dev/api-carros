# Memória técnica da API de Estoque de Veículos

Este documento registra o estado real do projeto no momento atual, com base na leitura do código-fonte, na estrutura da aplicação e no README do repositório. Ele não deve ser interpretado como uma proposta de reestruturação, e sim como um registro técnico do que realmente existe hoje.

## 1. Objetivo do projeto

A API foi desenvolvida para gerenciar o estoque de veículos de uma loja de automóveis, com foco em operações CRUD. O projeto está organizado como uma API REST em FastAPI, com objetivo principal de permitir:

- cadastro de veículos;
- listagem do estoque;
- consulta de um veículo por ID;
- atualização dos dados de um veículo;
- exclusão de um veículo.

O README deixa explícito que esta é uma primeira versão intencionalmente construída sem banco de dados, autenticação, Docker ou deploy, mantendo o foco em um CRUD sólido e bem organizado.

## 2. Tecnologias utilizadas

As tecnologias confirmadas no projeto são:

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- httpx

O arquivo `requirements.txt` confirma as dependências principais:

- `fastapi`
- `uvicorn[standard]`
- `pydantic`
- `pytest`
- `httpx`

## 3. Estrutura da aplicação

A estrutura atual do projeto é:

- `app/`
  - `__init__.py`
  - `main.py`
  - `models/`
    - `vehicle.py`
  - `repository/`
    - `vehicle_repository.py`
  - `routers/`
    - `vehicles.py`
- `tests/`
  - `test_vehicles.py`
- `README.md`
- `requirements.txt`
- `.gitignore`

A organização indica divisão funcional em camadas:

- `main.py`: ponto de entrada da aplicação e configuração do FastAPI;
- `routers/`: endpoints HTTP e lógica de exposição da API;
- `models/`: modelos de dados e validações com Pydantic;
- `repository/`: armazenamento e lógica de acesso ao estado do estoque;
- `tests/`: validação automatizada dos comportamentos esperados.

## 4. Arquitetura utilizada

A arquitetura identificada é uma estrutura simples em camadas, sem camada de serviços explícita:

1. `app.main` instancia o FastAPI e inclui o router principal.
2. `app.routers.vehicles` define as rotas da API.
3. `app.repository.vehicle_repository` encapsula o estado do estoque e implementa as operações de CRUD.
4. `app.models.vehicle` define os modelos e as regras de validação.
5. Os testes usam `TestClient` para exercitar a API por HTTP.

Não há evidência de:

- camada de serviço (`services/`);
- banco de dados;
- autenticação;
- filas ou mensageria;
- containerização;
- deploy automatizado.

## 5. Principais componentes

### `app/main.py`
- Cria a instância da aplicação FastAPI.
- Configura título, descrição e versão da API.
- Inclui o router de veículos.
- Expõe o endpoint raiz `/` com status da aplicação.

### `app/routers/vehicles.py`
- Define o prefixo `/veiculos`.
- Expõe endpoints para:
  - listar todos os veículos;
  - obter veículo por ID;
  - criar veículo;
  - atualizar veículo;
  - excluir veículo.
- Usa `HTTPException` para responder com erro 404 quando o veículo não existe.

### `app/models/vehicle.py`
- Define `VehicleBase`, `VehicleCreate`, `VehicleUpdate` e `Vehicle`.
- Cria os contratos de entrada e saída da API.
- Valida:
  - texto obrigatório e sem espaços vazios;
  - preço positivo;
  - quilometragem maior ou igual a zero;
  - ano válido dentro de um intervalo plausível;
  - campos obrigatórios em criação e atualização.
- Gera exemplos de payloads para documentação OpenAPI.

### `app/repository/vehicle_repository.py`
- Mantém o estado em memória em um dicionário (`dict[int, Vehicle]`).
- Acumula ids em `self._proximo_id`.
- Implementa CRUD básico:
  - `listar_todos()`
  - `buscar_por_id()`
  - `criar()`
  - `atualizar()`
  - `remover()`
- A instância `vehicle_repository` é compartilhada pela aplicação.

### `tests/test_vehicles.py`
- Reinicia o estado em memória antes de cada teste usando `setup_function()`.
- Valida o comportamento principal dos endpoints.
- Garante que a API rejeite entradas inválidas com status 422.

## 6. Endpoints existentes

Os endpoints confirmados no código são:

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verifica se a API está em execução |
| GET | `/veiculos` | Lista todos os veículos |
| GET | `/veiculos/{veiculo_id}` | Busca um veículo por ID |
| POST | `/veiculos` | Cria um novo veículo |
| PUT | `/veiculos/{veiculo_id}` | Atualiza um veículo por ID |
| DELETE | `/veiculos/{veiculo_id}` | Remove um veículo por ID |

## 7. Modelos e schemas

Os modelos existentes são:

- `VehicleBase`
  - `marca: str`
  - `modelo: str`
  - `ano: int`
  - `cor: str`
  - `quilometragem: float`
  - `preco: float`
  - `disponivel: bool = True`

- `VehicleCreate`: herda a base e representa criação.
- `VehicleUpdate`: herda a base e representa atualização completa do recurso.
- `Vehicle`: estende a base com `id: int`.

Validações confirmadas:

- `marca`, `modelo` e `cor`: não podem ser vazios após trim;
- `ano`: deve estar entre 1886 e `ano_atual + 1`;
- `quilometragem`: maior ou igual a zero;
- `preco`: maior que zero;
- `disponivel`: booleano com valor padrão `True`.

## 8. Estratégia de armazenamento dos dados

A estratégia confirmada é armazenamento em memória.

- Não existe banco de dados configurado.
- Os veículos são mantidos em um dicionário Python dentro do repositório.
- O estado do estoque é perdido quando a aplicação é encerrada.
- Os IDs são gerados sequencialmente, começando em 1.

A documentação do README confirma esta intenção, explicitando que a primeira versão foi feita sem banco de dados para manter foco no CRUD.

## 9. Estratégia de testes

Os testes usam pytest e `fastapi.testclient.TestClient`.

Pontos observados:

- o estoque em memória é limpo antes de cada teste;
- os testes validam sucesso e falha de endpoints;
- os testes cobrem casos de payload inválido e da ausência de veículos.

Não há evidência de testes de integração com banco, testes assíncronos, testes de performance ou cobertura de UI.

## 10. Dependências importantes

Dependências confirmadas no `requirements.txt`:

- `fastapi` — framework da API;
- `uvicorn[standard]` — servidor ASGI;
- `pydantic` — validação e serialização de modelos;
- `pytest` — execução dos testes;
- `httpx` — cliente HTTP para testes e integração.

## 11. Decisões arquiteturais já tomadas

As decisões que podem ser confirmadas a partir do código são:

- uso de FastAPI como framework principal;
- organização em módulos (`main`, `routers`, `models`, `repository`);
- utilização de Pydantic para serialização e validação;
- abordagem de CRUD direta em um repositório em memória;
- uso de `PUT` como atualização completa do recurso;
- geração automática do ID no repositório;
- tratamento de 404 para recurso inexistente;
- documentação OpenAPI gerada automaticamente.

## 12. Regras e padrões existentes no código

Padrões observados:

- nomes em português para rotas e mensagens de erro (ex.: `veiculo_id`, `Veículo com ID ... não encontrado.`);
- uso de `APIRouter` com prefixo `/veiculos`;
- uso de `response_model` para tipagem da resposta;
- uso de `Field` para documentação e validação de campos;
- uso de `field_validator` para regras específicas de texto e ano;
- uso de `status_code` explícito em rotas;
- instância única de repositório compartilhada.

## 13. Limitações atuais

As limitações que podem ser concluídas pelo código e pela documentação são:

- ausência de persistência real;
- ausência de autenticação/autorização;
- ausência de banco de dados;
- ausência de camada de serviço;
- ausência de paginação e filtros de listagem;
- ausência de suporte a múltiplos usuários ou contexto de sessão;
- ausência de containerização e deploy automatizado;
- estado compartilhado somente em memória enquanto a aplicação está em execução.

## 14. Problemas conhecidos ou riscos identificados

Não há um arquivo de issues ou documentação de bugs detalhada no projeto. Contudo, com base no código, os seguintes pontos devem ser considerados:

- reinicialização da aplicação resulta em perda de dados;
- qualquer alteração de estado é perdida ao fechar o processo;
- o projeto não possui proteção de acesso para dados sensíveis ou operações administrativas;
- não existem mecanismos de observabilidade, logs de auditoria ou monitoramento.

## 15. Funcionalidades já implementadas

A lista abaixo resume as funcionalidades atualmente confirmadas:

- [x] API em execução com FastAPI
- [x] Endpoint de status
- [x] Cadastro de veículos
- [x] Listagem de veículos
- [x] Consulta por ID
- [x] Atualização de veículos
- [x] Exclusão de veículos
- [x] Validação de campos
- [x] Tratamento de erros 404 e 422
- [x] Documentação automática Swagger/ReDoc
- [x] Testes automatizados com pytest
- [x] Armazenamento em memória do estoque

## 16. Pontos que devem ser considerados antes de alterar o projeto

Antes de qualquer modificação no código, é importante considerar:

- o projeto foi desenhado para manter dados em memória; qualquer mudança de persistência precisa ser planejada com cuidado;
- a API usa uma arquitetura simples e direta; alterar esta estrutura sem precisar pode aumentar a complexidade desnecessariamente;
- os modelos Pydantic definem contratos fortes; mudanças neles afetam a API e os testes;
- a lógica de negócio e o armazenamento estão fortemente acoplados no repositório atual;
- não há autenticação nem autorização; qualquer funcionalidade nova deve considerar esse contexto;
- qualquer mudança na estrutura dos endpoints deve ser acompanhada de ajuste em testes e documentação;
- o projeto não possui infraestrutura de deploy, banco ou observabilidade, então mudanças futuras nessa área exigem decisão explícita de arquitetura.

## 17. Observações finais

Este projeto está em um estado funcional e coerente para uma API de CRUD de veículos. Ele é especialmente útil como base para aprender FastAPI, Pydantic, organização em módulos e boas práticas de API REST. O seu principal limite atual é a ausência de persistência e de camada de infraestrutura mais robusta, o que deve ser encarado como uma decisão explícita do escopo atual e não como uma lacuna acidental.
