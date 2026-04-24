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

- [x] Configurar o framework de testes
- [x] Testes Unitários: Testar a lógica de cálculo da regra de 3 denúncias e transição de status (mockando o banco)
- [x] Testes Unitários: Testar a geração, expiração e validação de tokens JWT
- [x] Testes de Integração: Testar o fluxo completo de Reportar Foco usando um banco de dados de teste real com PostGIS
- [ ] Testes de Integração: Simular o upload de imagens garantindo que a API lide corretamente com falhas do S3
- [x] Testes de Integração: Testar o controle de acesso, garantindo que usuários comuns recebam erro 403 ao tentar usar rotas de firefighter
- [ ] Testes de Integração: Testar se os dados retornados do Redis condizem com o PostgreSQL após uma invalidação de cache

### Fase 6: Segurança e Autenticação

- [x] Criar rotas de Auth: Registro e Login retornando o token JWT.
- [x] Implementar o hashing seguro de senhas no cadastro.
- [x] Criar a dependência (middleware no FastAPI, ex: Depends(get_current_user)) para decodificar e validar o JWT.
- [x] Implementar controle de papéis/RBAC (USER, FIREFIGHTER, ADMIN) no token.
- [x] Proteger Rotas: Adicionar a dependência de Auth nas rotas (Exigir usuário para denunciar; Exigir papel FIREFIGHTER para a rota PATCH).
- [ ] Implementar Rate Limiting no endpoint de denúncias vinculado ao IP ou ID do usuário logado para evitar spam.
- [x] Revisar as rotas de acordo com os casos de uso da api e as regras do negócio.
- [x] Revisar os contratos da API (Refinar o Swagger/OpenAPI gerado pelo FastAPI).
- [x] Revisar os testes unitários e de integração baseado nos serviços de autenticação.

### Fase 7: Finalização e Deploy

- [x] Versionar a API
- [ ] Configurar CI/CD (ex: GitHub Actions) para rodar os testes e o linter automaticamente a cada commit/PR
- [ ] Isolar todas as credenciais e chaves secretas em variáveis de ambiente (.env) para o ambiente de produção.
- [ ] Preparar a infraestrutura em nuvem e realizar o primeiro deploy da API, Banco e Redis.

# Segurança e Autenticação

### 1. Gestão de Dependências (`pyproject.toml`)
- [x] Instalar pacote de criptografia: `passlib[bcrypt]` ou `passlib[argon2]`.
- [x] Instalar manipulador de tokens: `python-jose[cryptography]` ou `PyJWT`.
- [x] Confirmar dependência do OAuth2: `python-multipart` (incluído no `fastapi[all]`).

### 2. Módulo de Segurança (`source/api/core/security.py`)
- [x] Instanciar o `CryptContext` para o algoritmo de hash escolhido.
- [x] Implementar a função `get_password_hash(password)`.
- [x] Implementar a função `verify_password(plain_password, hashed_password)`.
- [x] Implementar a função `create_access_token(data, expires_delta)`.
- [x] Implementar a função `create_refresh_token()`.

### 3. Ajustes de Banco e Validação (`source/api/core/database/`)
- [ ] **Modelo (`models/user.py`):** Garantir que a coluna da tabela seja exclusivamente `hashed_password`.
- [x] **Schema de Entrada (`schemas/user.py`):** Criar `UserCreate` contendo a senha em texto claro.
- [ ] **Schema Interno (`schemas/user.py`):** Criar `UserInDB` contendo o `hashed_password`.
- [x] **Schema de Saída (`schemas/user.py`):** Ajustar `UserResponse` para remover qualquer menção a senhas.

### 4. Endpoints de Autenticação (`source/api/routes/auth.py`)
- [x] Criar rota `POST /login` utilizando a dependência `OAuth2PasswordRequestForm` do FastAPI.
- [x] Integrar verificação de usuário e senha na rota de login.
- [x] Retornar o JSON padronizado com `access_token`, `refresh_token` e `token_type`.
- [x] Criar rota `POST /refresh` para gerar novos tokens de acesso.

### 5. Dependências de Autorização (`source/api/core/dependencies/auth.py`)
- [x] Criar `oauth2_scheme` usando `OAuth2PasswordBearer`.
- [x] Implementar a dependência `get_current_user()` para decodificar o JWT e buscar o usuário ativo.
- [x] Implementar a dependência `require_role(role)` consumindo o `enums/roles.py` para controle de acesso (RBAC).

### 6. Defesas Ativas (`source/api/core/cache/service.py`)
- [ ] Criar função para incrementar falhas de login no Redis atreladas ao IP ou e-mail.
- [ ] Criar função para bloquear requisições de autenticação após o limite de tentativas (Rate Limiting).

### 7. Configurações Globais da API
- [x] **Variáveis de Ambiente (`deploy/variables/prod`):** Adicionar uma `SECRET_KEY` forte e criptograficamente segura.
- [ ] **CORS (`source/api/app.py`):** Configurar o `CORSMiddleware` restringindo o `allow_origins` apenas para os frontends da aplicação.
- [x] **Uploads Seguros (`source/api/routes/media.py`):** Refatorar rotas de envio de arquivos para ignorar o nome original do arquivo e gerar UUIDs seguros no salvamento via MinIO.
