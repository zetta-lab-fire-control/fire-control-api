# Arquitetura e Serviços

A arquitetura proposta é baseada em microsserviços lógicos (ou um Monolito Modular) com separação clara de responsabilidades. Utilizaremos um serviço de cache para otimizar a leitura do mapa.

```mermaid

sequenceDiagram
    participant Client as Web/Mobile App
    participant API as API (Python + FastAPI)
    participant Redis as Cache (Redis)
    participant DB as  RDBMS (PostgreSQL + PostGIS)
    participant Storage as Cloud Storage (Minio)

    Note over Client, Storage: Carregar Mapa de Ocorrências
    Client->>API: GET /api/v1/occurrences (Filtros: Hoje, Norte de Minas)
    API->>Redis: Busca dados do mapa em cache

    alt Cache HIT
        Redis-->>API: Retorna JSON otimizado
    else Cache MISS
        API->>DB: Consulta focos ativos e histórico
        DB-->>API: Retorna registros
        API->>Redis: Salva resultado no cache (TTL: 5 min)
    end
    API-->>Client: Response

    Note over Client, Storage: Registrar Denúncia

    Client->>API: POST /api/v1/reports (Foto, Lat, Lng, Intensidade)
    API->>Storage: Faz upload da imagem enviada
    Storage-->>API: Retorna URL da imagem

    API->>DB: Query Espacial (Raio 400m)
    DB-->>API: Resultado

    API->>DB: POST/PUT ocorrence
    DB-->>API: Confirmação da transação

    API->>Redis: Invalida/Atualiza cache do mapa afetado
    API-->>Client: Response

    Note over Client, Storage: Gerir denúncias
    Client->>API: PATCH /api/v1/occurrences/{id} (status: SOLUCIONADO)
    API   ->>DB: Atualiza status e preenche 'resolved_at'
    DB-->>API: Confirmação
    API->>Redis: Invalida cache do mapa (Foco some após 24h)
    API-->>Client: Response


```
