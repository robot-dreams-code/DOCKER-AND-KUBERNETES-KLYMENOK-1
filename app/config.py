import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_PORT: int = int(os.getenv("APP_PORT", "8080"))
    EXTERNAL_API_KEY: str | None = os.getenv("EXTERNAL_API_KEY")

settings = Settings()
