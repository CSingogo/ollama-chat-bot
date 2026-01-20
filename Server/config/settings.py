"""Application settings using Pydantic."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # App config
    groq_api_key: str
    debug: bool = Field(False)
    project_name: str = Field("ChatTGP")
    version: str = Field("0.1.0")
    database_url: str = Field( "sqlite:///database.db")


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()


