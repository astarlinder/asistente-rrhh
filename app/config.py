from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Base de datos
    db_user: str
    db_password: SecretStr
    db_name: str
    db_host: str = "localhost"
    db_port: int = 5432

    # Proveedores de IA
    llm_provider: str = "groq"
    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-3.7-flash"
    groq_api_key: SecretStr | None = None
    groq_model: str = "openai/gpt-oss-120b"

    # RAG
    umbral_similitud: float = 0.80
    reformular: bool = True

    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
