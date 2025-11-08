import os

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class APIConfig(BaseSettings):
    host: str
    port: str
    log_level: str
    cors_origins: str
    debug: bool
    workers: int = os.cpu_count()

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="API_", extra="ignore"
    )


class PostgresConfig(BaseSettings):
    db: str
    host: str
    user: str
    password: str
    port: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="POSTGRES_", extra="ignore"
    )

    def connection_string(self) -> str:
        url = "%s://%s:%s@%s:%s/%s" % (
            "postgresql+asyncpg",
            self.user,
            self.password,
            self.host,
            self.port,
            self.db,
        )

        return url


class RedisDatabase(BaseSettings):
    url: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="REDIS_", extra="ignore"
    )


class TokenConfig(BaseSettings):
    algorithm: str
    issuer: str
    expiration_time: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="TOKEN_", extra="ignore"
    )


class Settings(BaseSettings):
    postgres: PostgresConfig = PostgresConfig()
    redis: RedisDatabase = RedisDatabase()
    api_config: APIConfig = APIConfig()
    token_config: TokenConfig = TokenConfig()


settings = Settings()
