

alembic init migrations

alembic revision --autogenerate -m "initdb"

alembic upgrade head

uvicorn app.main:app --reload

clean_cache:
    pyclean --verbose .