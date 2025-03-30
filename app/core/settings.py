from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TOKEN: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
