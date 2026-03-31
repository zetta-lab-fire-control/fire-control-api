# Casos de Uso

### Usuários

Rotas responsáveis pela gestão de acesso, autenticação e recuperação de credenciais, garantindo a segurança estipulada nas regras de negócio (senhas criptografadas e expiração de sessão).

* **`POST /api/auth/login` (Autenticação)**
    * **Descrição:** Valida as credenciais (email e senha) do usuário (seja perfil `PUBLIC`, `FIREFIGHTER` ou `ADMIN`).
    * **Regras:** Retorna erro caso credenciais sejam inválidas (sem expor dados sensíveis). Em caso de sucesso, gera um token ou sessão com tempo de expiração rigoroso de 30 minutos de inatividade. Redireciona usuários públicos para o formulário de denúncia e administradores para o painel operacional.
* **`POST /api/auth/forgot-password` (Recuperação de Senha)**
    * **Descrição:** Recebe o email do usuário e envia as instruções para redefinição de senha.
    * **Regras:** Valida o formato do e-mail no backend.
* **`POST /api/auth/logout` (Encerramento de Sessão)**
    * **Descrição:** Invalida o token/sessão atual do usuário, forçando a desconexão.

---

### Denúncias

Rotas voltadas para a interação do público (usuários logados) para reportar focos de incêndio.

* **`POST /api/reports` (Registrar Denúncia)**
    * **Descrição:** Rota protegida (apenas usuários autenticados). Recebe os dados do formulário: `location` (coordenadas ou cidade) e `intensity_perceived` (LOW, MEDIUM, HIGH), além de opcionalmente a `photo_url`.
    * **Regras de Negócio:**
        * Valida se todos os campos obrigatórios foram preenchidos e se a localização é válida.
        * Salva a denúncia na tabela `REPORTS`.
        * **Gatilho de Ocorrência:** O sistema deve verificar se já existe uma ocorrência ativa na mesma área. Se não houver, cria uma nova em `OCCURRENCES` com status `QUEUED` ("Em análise"). Se houver, vincula a denúncia à ocorrência existente.
        * **Validação Automática:** Se o sistema detectar 3 denúncias na mesma localização, o status da ocorrência vinculada avança automaticamente para `VALIDATED` (Alerta validado).
        * Retorna mensagem de sucesso com o código da ocorrência gerada/vinculada.

---

### Ocorrências

Rotas consumidas principalmente pelos painéis de visualização (Home pública) e pelo painel operacional (Administradores/Bombeiros).

* **`GET /api/occurrences/indicators` (Indicadores da Home)**
    * **Descrição:** Rota pública (ou acessível na Home) que processa e retorna os dados resumidos do sistema.
    * **Regras:**
        * **Total de Focos Ativos:** Contagem de ocorrências onde o status NÃO é `RESOLVED` ou `INVALIDATED`.
        * **Municípios Afetados:** Contagem distinta (sem duplicidade) das localizações (cidades) atreladas às ocorrências ativas.
        * **Nível de Risco:** Calculado via backend baseado na quantidade e intensidade média (`intensity_avg`) dos focos ativos (Baixo, Médio, Alto).
        * Se não houver dados, retorna todos os valores como `0`.
* **`GET /api/occurrences` (Listar Ocorrências)**
    * **Descrição:** Rota protegida (`ADMIN` ou `FIREFIGHTER`). Retorna a lista de ocorrências consolidadas para o painel operacional.
    * **Regras:** Inclui informações de localização, contagem de denúncias associadas (`REPORTS`), intensidade média e status atual. Permite ordenação por data de criação (mais recentes) ou por volume de denúncias associadas. Retorna array vazio caso não haja registros.
* **`GET /api/occurrences/{id}` (Detalhes da Ocorrência)**
    * **Descrição:** Rota protegida. Retorna o detalhamento completo de uma ocorrência específica.
    * **Regras:** Traz os dados da tabela `OCCURRENCES` cruzados com a tabela `REPORTS` vinculadas para exibir: status atual, horários (`created_at`), intensidade e um array de imagens (`photo_url`) extraídas das denúncias que compõem aquela ocorrência.
* **`PATCH /api/occurrences/{id}/status` (Atualizar Status da Ocorrência)**
    * **Descrição:** Rota protegida para uso exclusivo do painel operacional. Atualiza a coluna `status` de uma ocorrência.
    * **Regras:** O status deve ser restrito ao *enum* do banco (`QUEUED` = Em análise, `EXECUTING` = Em atendimento, `RESOLVED` = Solucionado, `INVALIDATED` = Alerta falso). Salva imediatamente e garante que a mudança reflita nos indicadores globais. Caso o status seja `RESOLVED` ou `INVALIDATED`, deve preencher automaticamente o campo `resolved_at`.
