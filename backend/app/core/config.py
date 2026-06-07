from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "EAIOS Orchestration Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # We will add OpenAI, Qdrant, and Redis keys here later
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()