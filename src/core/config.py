from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunSettings(BaseModel):
    host: str = "localhost"
    port: int = 8008
    https: bool = False
    reload: bool = False
    debug: bool = False
    domain: str = "example.com"


class ApiPrefix(BaseModel):
    prefix: str = "/api/v1"


class DatabaseSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class SecuritySettings(BaseModel):
    api_key_name: str = "X-API-Key"
    api_key: str = "secret"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env.template", ".env.template", "../.env", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        populate_by_name=True,
    )
    run: RunSettings = RunSettings()
    api: ApiPrefix = ApiPrefix()
    security: SecuritySettings = SecuritySettings()
    db: DatabaseSettings


settings = Settings()
