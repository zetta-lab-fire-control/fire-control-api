# Desenvolvimento 

### Fase 1: Planejamento e Design

- [x] Inicializar o repositório Git e definir a estrutura de pastas (arquitetura do código)
  
- [x] Definir requisitos funcionais e não funcionais

- [x] Desenhar a arquitetura geral e fluxo de dados

- [x] Modelar o schema do banco de dados (Relacional + Geoespacial)


### Fase 2: Configuração do Projeto e Infraestrutura

- [ ] Configurar o ambiente de desenvolvimento local (uv, docker, makefile)
  
- [ ] Configurar ferramentas de qualidade de código (Linter, Formatter)
  

### Fase 3: Desenvolvimento - Serviços Core

- [ ] Documentar os contratos da API (Criar o Swagger/OpenAPI spec das rotas)
  
- [ ] Configurar o ORM/Query Builder e executar as migrations iniciais do schema

- [ ] Auth: Implementar registro e login gerando token JWT (com hash de senhas)

- [ ] Auth: Criar middlewares de proteção de rotas e controle de papéis (USER, FIREFIGHTER, ADMIN)

- [ ] Upload: Integrar o serviço de Cloud Storage (ex: AWS S3) para receber fotos e retornar a URL

- [ ] Geoespacial: Escrever a query do PostGIS (ST_DWithin) para calcular o raio de 400m

- [ ] Ocorrências: Criar o endpoint de Reportar Foco (POST) recebendo dados, validando o raio de 400m e vinculando/criando a ocorrência

- [ ] Regra de Negócio: Implementar a lógica que altera o status automaticamente ao atingir 3 denúncias

- [ ] Bombeiros: Criar o endpoint (PATCH) para bombeiros atualizarem o status do foco (preenchendo a data de resolução)

- [ ] Leitura/Filtros: Criar o endpoint do Mapa (GET) filtrando apenas focos ativos ou solucionados há menos de 24h

- [ ] Estatísticas: Criar os endpoints de dados agregados (histórico, contagens diárias, cidades afetadas)

### Fase 4: Otimização e Segurança

- [ ] Cache: Configurar a conexão da API com o Redis

- [ ] Cache: Implementar o armazenamento em cache para a rota de leitura do Mapa e Dashboards

- [ ] Cache: Criar a rotina de invalidação/atualização do cache quando uma nova denúncia é feita ou um status é alterado

- [ ] Segurança: Implementar Rate Limiting no endpoint de denúncias para evitar ataques de bots/spam

### Fase 5: Testes (Unitários e de Integração)

- [ ] Configurar o framework de testes (ex: Jest se for Node, Pytest se for Python)

- [ ] Testes Unitários: Testar a lógica de cálculo da regra de 3 denúncias e transição de status (mockando o banco)

- [ ] Testes Unitários: Testar a geração, expiração e validação de tokens JWT

- [ ] Testes de Integração: Testar o fluxo completo de Reportar Foco usando um banco de dados de teste real com PostGIS

- [ ] Testes de Integração: Simular o upload de imagens garantindo que a API lide corretamente com falhas do S3

- [ ] Testes de Integração: Testar o controle de acesso, garantindo que usuários comuns recebam erro 403 ao tentar usar rotas de bombeiros

- [ ] Testes de Integração: Testar se os dados retornados do Redis condizem com o PostgreSQL após uma invalidação de cache

### Fase 6: Finalização e Deploy

- [ ] Configurar CI/CD (ex: GitHub Actions) para rodar os testes e o linter automaticamente a cada commit/PR

- [ ] Isolar todas as credenciais e chaves secretas em variáveis de ambiente (.env)

- [ ] Preparar a infraestrutura em nuvem e realizar o primeiro deploy da API, Banco e Redis