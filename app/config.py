import secrets
from typing import Annotated, Any

from pydantic import PostgresDsn, BeforeValidator, AnyUrl
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',')]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_ignore_empty=True, extra='ignore'
    )

    API_PREFIX: str = '/api/v1'

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'
    DOMAIN: str = 'https://fastapi-dyjd.onrender.com'
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    POSTGRES_SERVER: str = 'dpg-cqq2dgqj1k6c73d9qjq0-a'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'test'
    POSTGRES_PASSWORD: str = '2RMatcepeyaldJqhijMV2jXM0Wm6mnhn'
    POSTGRES_DB: str = 'test_nwvk'

    @property
    def database_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql+psycopg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
