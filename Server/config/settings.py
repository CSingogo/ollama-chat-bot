"""Application settings using Pydantic."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # App config
    google_api_key: str
    debug: bool = Field(False)
    project_name: str = Field("ChatTGP")
    version: str = Field("0.1.0")
    database_url: str = Field( "sqlite:///database.db")
    secret_key: str = Field("f3A9dG4s8b2Hj9kL0qYzT1uVwXcR5mN6")
    algorithm: str = Field("HS256")
    access_token_expire_minutes: int = Field(30)


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()


