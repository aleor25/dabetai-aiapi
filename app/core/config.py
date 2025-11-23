from pydantic import ConfigDict
from pydantic_settings import BaseSettings

import os


class Settings(BaseSettings):
    project_name: str = "DABETAI-AIAPI"
    ml_models_dir: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml_models")
    database_url: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dabetai.db')}"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7
    fcm_server_key: str = ""
    google_client_id: str = ""
    
    model_config = ConfigDict(env_file=".env")


settings = Settings()
