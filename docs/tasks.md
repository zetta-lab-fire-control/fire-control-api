# Desenvolvimento

### Fase 1: Planejamento e Design

- [x] Inicializar o repositório Git e definir a estrutura de pastas (arquitetura do código)
- [x] Definir requisitos funcionais e não funcionais
- [x] Desenhar a arquitetura geral e fluxo de dados
- [x] Modelar o schema do banco de dados (Relacional + Geoespacial)


### Fase 2: Configuração do Projeto e Infraestrutura

- [x] Configurar o ambiente de desenvolvimento local (uv, docker, makefile)
- [x] Configurar ferramentas de qualidade de código (Linter, Formatter)


### Fase 3: Desenvolvimento - Serviços Core

- [x] Configurar a conexão do ORM (ex: SQLAlchemy + GeoAlchemy2) com o PostgreSQL.
- [x] Criar os Modelos (Tabelas do banco) para Usuários, Ocorrências e Denúncias.
- [x] Criar os Schemas (Pydantic) para validação de entrada e saída de dados.
- [x] Configurar o Alembic e executar as migrations iniciais do schema.
- [x] Integrar o serviço de Cloud Storage (MinIO configurado) para upload de fotos.
- [x] Criar a query geoespacial (PostGIS ST_DWithin) para calcular o raio de 400m.
- [x] Criar as rotas de acordo com os casos de uso da api e as regras do negócio.
- [x] Documentar os contratos da API (Refinar o Swagger/OpenAPI gerado pelo FastAPI).


### Fase 4: Otimização e Performance

- [x] Cache: Configurar a conexão da API com o Redis
- [x] Cache: Implementar rotinas de armazenamento/limpeza e atualização de dados em cache.


### Fase 5: Testes (Unitários e de Integração)

- [ ] Configurar o framework de testes
- [ ] Testes Unitários: Testar a lógica de cálculo da regra de 3 denúncias e transição de status (mockando o banco)
- [ ] Testes Unitários: Testar a geração, expiração e validação de tokens JWT
- [ ] Testes de Integração: Testar o fluxo completo de Reportar Foco usando um banco de dados de teste real com PostGIS
- [ ] Testes de Integração: Simular o upload de imagens garantindo que a API lide corretamente com falhas do S3
- [ ] Testes de Integração: Testar o controle de acesso, garantindo que usuários comuns recebam erro 403 ao tentar usar rotas de bombeiros
- [ ] Testes de Integração: Testar se os dados retornados do Redis condizem com o PostgreSQL após uma invalidação de cache

### Fase 6: Segurança e Autenticação

- [ ] Criar rotas de Auth: Registro e Login retornando o token JWT.
- [ ] Implementar o hashing seguro de senhas no cadastro.
- [ ] Criar a dependência (middleware no FastAPI, ex: Depends(get_current_user)) para decodificar e validar o JWT.
- [ ] Implementar controle de papéis/RBAC (USER, FIREFIGHTER, ADMIN) no token.
- [ ] Proteger Rotas: Adicionar a dependência de Auth nas rotas (Exigir usuário para denunciar; Exigir papel FIREFIGHTER para a rota PATCH).
- [ ] Implementar Rate Limiting no endpoint de denúncias vinculado ao IP ou ID do usuário logado para evitar spam.
- [ ] Revisar as rotas de acordo com os casos de uso da api e as regras do negócio.
- [ ] Revisar os contratos da API (Refinar o Swagger/OpenAPI gerado pelo FastAPI).
- [ ] Revisar os testes unitários e de integração baseado nos serviços de autenticação.

### Fase 6: Finalização e Deploy

- [ ] Versionar a API
- [ ] Configurar CI/CD (ex: GitHub Actions) para rodar os testes e o linter automaticamente a cada commit/PR
- [ ] Isolar todas as credenciais e chaves secretas em variáveis de ambiente (.env) para o ambiente de produção.
- [ ] Preparar a infraestrutura em nuvem e realizar o primeiro deploy da API, Banco e Redis.
