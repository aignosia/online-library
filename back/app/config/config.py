from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Online Library API"
    DATABASE_URI: str = ""
    JWT_SECRET_KEY: str = ""
    PASSWORD_HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RECOMMENDATION_MODEL_FILE: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
