from pathlib import Path

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = False
    APP_NAME: str = "AbsoluteWallet"
    VERSION: str = "1.0.0"
    BASE_DIR: str = str(Path.cwd())  # base dir detected for render templates

    POSTGRES_PORT: str  # DB port
    POSTGRES_DB: str  # DB name
    POSTGRES_USER: str  # DB user permission
    POSTGRES_PASSWORD: str  # DB password permission
    POSTGRES_HOST: str  # DB host permission if using in docker db else localhost
    POSTGRES_PORT: str  # DB port

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def get_db_uri(self):
        return f'postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def base_path(self):
        return '/api/v1'

    @property
    def unicorn_config(self):
        server = {
            'app': "main:app",
            'host': "0.0.0.0",
            'port': 5007,
            'debug': self.DEBUG,
        }
        if self.DEBUG:
            server['reload'] = True
        else:
            server['root_path'] = self.base_path
        return server


config = Settings()
