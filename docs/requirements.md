# Requisitos da API

### Requisitos Funcionais (RF)

- RF01 - Autenticação e Autorização: A API deve permitir login via e-mail e senha, gerando um token JWT. Deve haver controle de papéis (Roles: USER, FIREFIGHTER, ADMIN).

- RF02 - Registro de Denúncias: A API deve receber dados de uma nova denúncia (latitude, longitude, intensidade, imagem).

- RF03 - Upload de Imagens: A API deve receber o arquivo da foto, enviá-lo para um serviço de Cloud Storage (ex: AWS S3) e salvar apenas a URL no banco de dados.

- RF04 - Agrupamento Espacial (Clustering): Ao receber uma denúncia, a API deve verificar se existe uma Ocorrência ativa num raio de 400 metros.

    - Se SIM: Vincula a denúncia à ocorrência existente.

    - Se NÃO: Cria uma nova ocorrência com status "Em análise".

- RF05 - Motor de Validação Automática: Sempre que uma ocorrência atingir 3 denúncias vinculadas, a API deve alterar seu status automaticamente para "Alerta validado automaticamente".

- RF06 - Gestão de Status: A API deve permitir que usuários com perfil FIREFIGHTER alterem o status da ocorrência (Ex: para Em atendimento, Solucionado ou Alerta falso).

- RF07 - Filtro de Exibição (Regra de 24h): A API de listagem do mapa não deve retornar ocorrências com status Solucionado ou Alerta Falso cuja data de alteração seja superior a 24 horas.

- RF08 - Dashboards e Histórico: A API deve fornecer endpoints que retornem dados agregados (count, group by) para alimentar os gráficos, cards de resumo diário e painéis de indicadores, filtráveis por data e região.

- RF09 - Feedback ao Usuário: O endpoint de criação de denúncia deve retornar uma resposta formatada contendo o ID gerado, status e a mensagem de orientação sobre a regra das 3 denúncias.

### Requisitos Não Funcionais (RNF)

- RNF01 - Performance Geoespacial: O banco de dados deve utilizar índices espaciais (ex: GIST no PostGIS) para garantir que a busca do raio de 400m responda em milissegundos.

- RNF02 - Segurança: Todas as rotas (exceto Home, Histórico e Reportar Foco anônimo) devem ser protegidas por JWT. Senhas devem ser armazenadas com hash (ex: bcrypt).

- RNF03 - Rate Limiting: O endpoint de Reportar Foco deve ter limite de requisições por IP para evitar ataques de spam/bots que possam gerar falsos alertas.

- RNF04 - Escalabilidade: A arquitetura deve ser stateless (sem guardar estado na memória do servidor) para permitir o escalonamento horizontal em épocas de seca (alta demanda).