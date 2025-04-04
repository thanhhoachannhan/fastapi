
init_migrations:
    alembic init migrations

revision:
    alembic revision --autogenerate -m "initdb"

upgrade:
    alembic upgrade head

run:
    uvicorn app.main:app --reload

clean_cache:
    pyclean --verbose .