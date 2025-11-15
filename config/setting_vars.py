import logging
# Standard Libraries
from typing import Optional

# Third-party Libraries
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv


# --- Load environment early (optional but useful for local/dev) ---
load_dotenv()

# --- Logger setup ---
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application environment settings.

    Defines strongly-typed environment variables for the application.
    Automatically loads from `.env`, Docker, or system environment.
    """

    # --- Core settings ---
    DEBUG: int = Field(default=1, description="Enable/disable debug mode.")
    DATABASE_URL: Optional[str] = Field(
        default=None, description="Database connection string."
    )
    SECRET_KEY: SecretStr = Field(default="*")

    # --- Configuration metadata ---
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # json_loads=json.loads,
        extra="ignore",  # ignores unknown vars gracefully
    )


# --- Instantiate settings ---
settings = Settings()

# --- Log settings at startup (safe) ---
logger.debug("Loaded settings", settings=settings.model_dump())
