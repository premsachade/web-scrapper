import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    __BASE_DIRECTORY = os.getcwd()

    DATA_DIRECTORY: str = f"{__BASE_DIRECTORY}/data"

    IMAGES_DIRECTORY: str = f"{DATA_DIRECTORY}/images"

    REDIS_URL: str

    API_KEY: str

    EMAIL_RECIPIENTS: list[str]


settings = Settings()  # type: ignore
