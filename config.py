from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_URL: str

    ACCESS_TOKEN_SIGNATURE_SECRET: str
    ACCESS_TOKEN_EXPIRATION_TIME: int

    ADMIN_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
