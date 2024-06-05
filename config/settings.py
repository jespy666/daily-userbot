import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from dataclasses import dataclass


load_dotenv()

# Set root path
BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(slots=True, frozen=True)
class BotConfig:
    api_id: str
    api_hash: str
    app_name: str


@dataclass(slots=True)
class DBConfig:
    db_type: Optional[str] = os.getenv('DB_TYPE')
    db_host: Optional[str] = os.getenv('DB_HOST')
    db_port: Optional[int] = os.getenv('DB_PORT')
    username: Optional[str] = os.getenv('DB_USERNAME')
    password: Optional[str] = os.getenv('DB_PASSWORD')
    db_name: Optional[str] = os.getenv('DB_NAME')

    def get_db_url(self) -> str:
        match self.db_type:
            case t if t == 'mysql':
                return self._get_mysql_url()
            case t if t == 'postgres':
                return self._get_postgres_url()
            case t if t == 'mongo':
                return self._get_mongo_url()
            case t if t == 'sqlite':
                return self._get_sqlite_url()
            case t if t == 'redis':
                return self._get_redis_url()
            case _:
                raise ValueError(f"Unsupported database type: {self.db_type}")

    def _get_mysql_url(self) -> str:
        return (f"mysql://{self.username}:{self.password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}")

    def _get_postgres_url(self) -> str:
        return (f"postgresql://{self.username}:{self.password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}")

    def _get_mongo_url(self) -> str:
        credentials = f"{self.username}:{self.password}@"\
            if self.username and self.password else ""
        return (f"mongodb://{credentials}{self.db_host}:"
                f"{self.db_port}/{self.db_name}")

    def _get_sqlite_url(self) -> str:
        return f"sqlite://{BASE_DIR}/{self.db_name}.db"

    def _get_redis_url(self) -> str:
        credentials = f"{self.username}:{self.password}@"\
            if self.username and self.password else ""
        port_part = f":{self.db_port}" if self.db_port else ""
        return f"redis://{credentials}{self.db_host}{port_part}/0"
