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
    DOMAIN: str = 'localhost'
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_TYPE: str = 'sqlite'

    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'test'

    @property
    def database_uri(self) -> PostgresDsn:
        if self.DATABASE_TYPE == 'sqlite':
            return 'sqlite:///./test.db'
        return MultiHostUrl.build(
            scheme='postgresql+psycopg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
