# Entidades do Banco de Dados

- Usuários (USERS): Quem interage com o sistema. Usuários públicos, administrativos ou institucionais (bombeiros).
- Ocorrências (OCCURRENCES): O alerta enviado pela população. Várias denúncias na mesma região podem formar apenas 1 ocorrência.
- Denúncias (REPORTS): O incêndio validado pelos bombeiros/sistema.
- CidadesMineiras (MG_CITIES): Limites territoriais oficiais dos municípios para estatísticas estaduais.
- ZonasClimáticas (WEATHER_ZONES): A malha/grade de monitoramento contínuo.
- CondiçõesClimáticas (WEATHER_CONDITIONS): As leituras diárias/horárias que alimentam o mapa de calor de risco.

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
        geometry location "POINT(Lat, Lng)"
        string city
        enum type "FOREST_FIRE, URBAN_FIRE, OTHER"
        enum intensity "LOW, HIGH, MEDIUM"
        enum status "QUEUED, VALIDATED, EXECUTING, RESOLVED, INVALIDATED"
        enum ignition_cause "NATURAL, HUMAN, UNKNOWN"
        enum land_cover "FOREST, NATURAL, FARMING, URBAN, UNKNOW"
        decimal burned_area_ha
        datetime resolved_at
        datetime created_at
        string resolved_by
    }

    REPORTS {
        uuid id PK
        uuid user_id FK
        geometry location "POINT(Lat, Lng)"
        enum intensity_perceived "LOW, HIGH, MEDIUM"
        datetime created_at
        string photo_url
    }

    MG_CITIES {
        string ibge_code
        string name
        geometry geometry "multipolygon"
    }

    WEATHER_ZONE {
        string name
        geometry "polygon"
    }

    WEATHER_CONDITIONS {
        decimal temperature_celsius
        decimal relative_humidity
        decimal wind_speed_kmh
        decimal precipitation_mm
        decimal fire_risk_index
        datetime timestamp
        uuid zone_id FK
    }


    %% Relacionamentos
    USERS ||--o{ REPORTS : "add"
    USERS ||--o{ OCCURRENCES : "manage"
    OCCURRENCES ||--o{ REPORTS : "cluster"
    MG_CITIES ||--o{ OCCURRENCES : "host"
    WEATHER_ZONE ||--o{ WEATHER_CONDITIONS : "has a history of"

```
