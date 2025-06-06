# Working with environment variables, creating a class to validate the environment variables

# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Add this new field; it will be read if present in the environment
    DATABASE_URL: str | None = None


     # 2) Make these optional so Pydantic won’t complain if they’re missing
    DATABASE_HOSTNAME: str | None = None
    DATABASE_PORT: str | None     = None
    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_NAME: str | None     = None

    # DATABASE_HOSTNAME: str
    # DATABASE_PORT: int
    # DATABASE_PASSWORD: str
    # DATABASE_NAME: str
    # DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()           # type: ignore

