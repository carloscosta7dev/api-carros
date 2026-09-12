# Roadmap da API de Estoque de Veículos

Este roadmap foi elaborado com base no estado real do código e da documentação do projeto, sem presumir funcionalidades que ainda não existam.

## Concluído

### API FastAPI inicial funcionando
- Objetivo: disponibilizar a aplicação web e expor endpoints para gerenciamento do estoque.
- Evidência no código: a aplicação é criada em `app/main.py` com `FastAPI`, inclui o router de veículos e expõe o endpoint raiz `/`.

### Endpoint de status da API
- Objetivo: verificar rapidamente se a aplicação está funcionando.
- Evidência: rota `GET /` retornando status online e link para `/docs`.

### CRUD completo de veículos
- Objetivo: permitir criar, consultar, listar, atualizar e excluir veículos do estoque.
- Evidência: rotas em `app/routers/vehicles.py`:
  - `GET /veiculos`
  - `GET /veiculos/{veiculo_id}`
  - `POST /veiculos`
  - `PUT /veiculos/{veiculo_id}`
  - `DELETE /veiculos/{veiculo_id}`

### Validação de dados com Pydantic
- Objetivo: garantir que os dados recebidos pela API sigam regras de negócio antes de persistirem no estoque.
- Evidência: modelos em `app/models/vehicle.py` validam campos como marca, modelo, cor, ano, quilometragem, preço e disponibilidade.

### Repositório em memória
- Objetivo: manter o estado do estoque em memória durante a execução da aplicação.
- Evidência: `VehicleRepository` em `app/repository/vehicle_repository.py` guarda os veículos em um dicionário interno e gera IDs sequenciais.

### Tratamento de erros HTTP
- Objetivo: responder com status adequado quando um recurso não é encontrado ou quando a entrada é inválida.
- Evidência: uso de `HTTPException` com 404 para veículos inexistentes e validação do Pydantic com 422 para payloads inválidos.

### Documentação automática da API
- Objetivo: facilitar inspeção e testes pela interface do FastAPI.
- Evidência: Swagger UI, ReDoc e OpenAPI são disponibilizados automaticamente pela própria estrutura do FastAPI.

### Testes automatizados de endpoints
- Objetivo: validar o comportamento principal da API em cenários de sucesso e erro.
- Evidência: arquivo `tests/test_vehicles.py` cobre criação, listagem, busca por ID, atualização e remoção, além de casos de entrada inválida.

## Em andamento

Nenhuma funcionalidade foi identificada como estando em andamento com implementação parcial confirmada no código atual.

O projeto está em um estado funcional de CRUD em memória, sem evidência de desenvolvimento paralelo em outra camada ou de features incompletas em execução.

## Próximos passos

### Melhorar a gestão do estoque com filtros e buscas
- Objetivo: permitir consultas mais úteis, como buscar por marca, modelo, disponibilidade ou faixa de preço.
- Justificativa: a API hoje lista todos os veículos e busca por ID, mas não há filtros de consulta por critérios de negócio.

### Adicionar paginação e ordenação
- Objetivo: tornar a listagem mais controlável quando o número de veículos crescer.
- Justificativa: como o armazenamento é em memória, a expansão do número de registros pode tornar a listagem pouco prática sem paginação ou ordenação.

### Expandir a cobertura de testes
- Objetivo: aumentar a confiabilidade do projeto com casos adicionais de borda.
- Justificativa: os testes atuais cobrem rotas principais, mas não há indícios de testes para cenários mais específicos de integridade de dados, regras de negócio e muitas combinações de entradas.

### Padronizar tratamento de respostas e mensagens
- Objetivo: deixar a API mais consistente para clientes e integrações.
- Justificativa: o código atual usa mensagens explícitas em alguns pontos, mas ainda não há indicação de um padrão global de resposta para erros ou de contrato formalizado para todos os endpoints.

### Documentar melhor o contrato da API
- Objetivo: facilitar uso por outros desenvolvedores e integrações externas.
- Justificativa: o FastAPI gera documentação automática, mas o projeto pode se beneficiar de exemplos e descrições mais detalhadas em documentação complementar.

## Futuro

### Persistência em banco de dados
- Objetivo: substituir o armazenamento em memória por uma solução persistente, como SQLite, PostgreSQL ou outro banco relacional.
- Justificativa: a arquitetura atual é feita para memória em execução, o que faz o estoque desaparecer ao reiniciar a aplicação.

### Autenticação e autorização
- Objetivo: proteger endpoints e controlar quem pode cadastrar, alterar ou excluir veículos.
- Justificativa: o código atual não possui qualquer mecanismo de identidade, sessão, token ou autorização.

### Containerização e ambiente de execução padronizado
- Objetivo: facilitar execução em diferentes ambientes e reduzir problemas de configuração local.
- Justificativa: não há evidência de Docker, Docker Compose, arquivos de configuração de container ou ambiente reproduzível em produção.

### Deploy e CI/CD
- Objetivo: automatizar disponibilização da API em ambientes externos e validar mudanças com pipeline de integração.
- Justificativa: o projeto ainda é um CRUD local e não apresenta evidência de deploy automatizado ou pipeline de testes em ambiente contínuo.

### Observabilidade e monitoramento
- Objetivo: acompanhar logs, métricas, erros e disponibilidade em produção.
- Justificativa: o projeto atual não indica configuração de logging estruturado, métricas, tracing ou alertas.

### Evolução do domínio do negócio
- Objetivo: ampliar o modelo para cenários mais complexos de gestão de veículos e automóveis.
- Justificativa: o domínio atual é simples e homogêneo, mas poderia evoluir para regras mais específicas de negociação, estoque, status de venda, imagens, categoria, etc.

---

## Resumo do roadmap

O projeto já entregou uma API funcional e bem estruturada para CRUD de veículos, com validação, documentação e testes. O estado corrente é sólido para uso educacional ou como base inicial de portfólio. As próximas etapas mais sensatas são melhorias de experiência e usabilidade na API, e as evoluções de futuro mais relevantes envolvem persistência, autenticação e preparação para deploy e operação real.
