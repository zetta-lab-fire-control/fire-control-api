Todo List de Autenticação por Rota


1. Rotas de Users (/users)

    POST /users (Criar Usuário):

        - Autenticação: NÃO.


    GET /users (Listar Usuários):

        - Autenticação: SIM

        - Função: ADMIN/BOMBEIROS


    GET /users/{user_id} (Visualizar Usuário):

        - Autenticação: SIM

        - Função: ADMIN/BOMBEIROS, INSTANCE_OWNER


    PUT /users/{user_id} e DELETE /users/{user_id} (Editar/Deletar Usuário):

        - Autenticação: SIM

        - Função: ADMIN/BOMBEIROS, INSTANCE_OWNER


2. Rotas de Reports (/reports - Denúncias)

    POST /reports (Criar Denúncia):

        - Autenticação: SIM

        - Função: LOGGED_USER


    GET /reports (Listar Denúncias):

        - Autenticação: SIM.

        - Função: ADMIN/BOMBEIROS


    GET /reports/{report_id} (Visualizar Denúncia):

        - Autenticação: SIM.

        - Função: ADMIN/BOMBEIROS, INSTANCE_OWNER


    PUT /reports/{report_id} e DELETE /reports/{report_id} (Editar/Deletar Denúncia):

        - Autenticação: SIM.

        - Função: ADMIN/BOMBEIROS


3. Rotas de Occurrences (/occurrences - Focos de Incêndio Validados)

    GET /occurrences (Listar Ocorrências Base):

        - Autenticação: NÃO


    GET /occurrences/indicators/public e /occurrences/indicators/history (Indicadores Públicos e Histórico):

        - Autenticação: NÃO


    GET /occurrences/indicators/operational (Indicadores Operacionais):

        - Autenticação: SIM

        - Função: ADMIN/BOMBEIROS


    PUT /occurrences/{occurrence_id} e DELETE /occurrences/{occurrence_id} (Atualizar/Deletar Ocorrência):

        - Autenticação: SIM

        - Função: ADMIN/BOMBEIROS


    POST /occurrences (Criar Ocorrência Validada):

        - Autenticação: SIM

        - Função: ADMIN/BOMBEIROS


4. Rotas de Media (/media)

    POST /media (Upload de Mídia):

        - Autenticação: SIM

        - Função: LOGGED_USER


    GET /media/{media_id} (Visualizar Mídia):

        - Autenticação: NÃO
