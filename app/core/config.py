from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_TIME: int = 30
    REFRESH_TOKEN_TIME: int = 7
    GROQ_API_KEY: str

settings = Settings()