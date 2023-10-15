from pydantic import BaseModel


class ServiceConfig(BaseModel):
    api_key: str

    class Config:
        env_prefix = "service"
        env_file = ".env"
