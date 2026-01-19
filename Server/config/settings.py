"""Application settings using Pydantic."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # App config
    api_key: str = Field(..., env="GROQ_API_KEY")
    debug: bool = Field(False)
    project_name: str = Field("ChatTGP")
    version: str = Field("0.1.0")
    database_url = Field( "sqlite:///database.db")




settings = Settings()