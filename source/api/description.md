
Fire-Control-API is a RESTful API designed to support the management of enviromental fires. It provides endpoints for creating, retrieving, updating, and deleting fire records, as well as managing fire-fighting resources and personnel. The API is built using FastAPI and is designed to be scalable and efficient, utilizing Redis for caching and PostgreSQL for data storage. It is intended to be used by fire departments, emergency response teams, and other organizations involved in fire management and response.

Resources:
- Reports: Endpoints for creating and managing fire reports, including details such as location, severity, and status.
- Occurences: Endpoints for tracking fire occurrences, wich are validated reports that have been confirmed as actual fires.
- Users: Endpoints for managing user accounts, including fire-fighters and other personnel involved in fire management, as well the common users that can report fires.
