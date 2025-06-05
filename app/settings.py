import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Settings:
    ENV: str
    APP_NAME: str
    APP_VERSION: str
    LOG_DIR: str
    SOURCES: list
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    
    @property
    def STORAGE(self):
        return {
            "PATH": (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            ),
            "SOURCES": self.SOURCES
        }
    
    @property
    def HANDLER(self):
        return {
            ""
        }

    @classmethod
    def build(cls, config_dict):
        env = os.getenv("ENV", config_dict.get("ENV", "prod"))

        if env == "prod":
            load_dotenv()

        return cls(
            ENV=env,
            APP_NAME=config_dict.get("APP_NAME", "app"),
            APP_VERSION=config_dict.get("APP_VERSION", "1.0.0"),
            
            LOG_DIR=config_dict.get("LOG_DIR", "./logs"),

            SOURCES=config_dict.get("SOURCES", []),

            POSTGRES_HOST=os.getenv("POSTGRES_HOST", "postgres"),
            POSTGRES_USER=os.getenv("POSTGRES_USER", "admin"),
            POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "pass"),
            POSTGRES_DB=os.getenv("POSTGRES_DB", "db-name"),
            POSTGRES_PORT=int(os.getenv("POSTGRES_PORT", "5432")),
        )