
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RepoPilot"
    environment: str = "development"
    secret_key: str = "development-only-change-me"
    access_token_minutes: int = 30
    refresh_token_days: int = 7
    database_url: str = "sqlite:///./repopilot.db"
    cors_origins: str = "http://localhost:5173"
    github_token: str = ""

    # Local Ollama configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:7b"
    ollama_timeout_seconds: int = 240

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self):
        return [
            x.strip()
            for x in self.cors_origins.split(",")
            if x.strip()
        ]


settings = Settings()
