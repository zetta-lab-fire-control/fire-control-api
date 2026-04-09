# Entidades do Banco de Dados

- Usuários (USERS)
- Ocorrências (OCCURRENCES)
- Denúncias (REPORTS)

### Schema

```mermaid
erDiagram

    USERS {
        uuid id PK
        string firstname
        string lastname
        string email UK
        string telephone
        string password
        datetime created_at
        enum role "PUBLIC, FIREFIGHTER, ADMIN"

    }

    OCCURRENCES {
        uuid id PK
        uuid report_id FK
        geometry location "(Lat, Lng)"
        string city
        enum type "FOREST_FIRE, URBAN_FIRE, OTHER"
        enum intensity "LOW, HIGH, MEDIUM"
        enum status "QUEUED, VALIDATED, EXECUTING, RESOLVED, INVALIDATED"
        datetime resolved_at
        datetime created_at
        string resolved_by
    }

    REPORTS {
        uuid id PK
        uuid user_id FK
        geometry location "(Lat, Lng)"
        enum intensity_perceived "LOW, HIGH, MEDIUM"
        datetime created_at
        string photo_url
    }

    %% Relacionamentos
    USERS ||--o{ REPORTS : "add"
    USERS ||--o{ OCCURRENCES : "manage"
    OCCURRENCES ||--o{ REPORTS : "contain"
```
