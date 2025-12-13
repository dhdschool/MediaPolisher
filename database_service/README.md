# Database Service

This service handles crud operations, schemas/migrations, and database session management.

## Running

This service runs via docker compose.
For production, it requires the MP_DB_SERVICE_URL env var, pointing to the postgres database URL.

## Alembic migrations
To run alembic migrations that resolve files correctly, use the alembic_op.sh in /scripts as you would with alembic. Example:
./scripts/alembic_op.sh revision --autogenerate -m "message"

## Schemas
All json inputs/outputs are found in shared_libs/database_service.py

## API Endpoints
POST /feeds/ - Takes a FeedsCreateRequest json and returns a FeedDTO
GET /feeds/{feed_id} - Takes a feed's UUID and returns a FeedDTO
GET /feeds/ - Gets all FeedDTOs in the database
PATCH /feeds/{feed_id} - Updates a feed's state with relevant data
