from pydantic_settings import BaseSettings


class ServiceConfig(BaseSettings):
    marketstack_api_key: str
    polygon_api_key: str

    class Config:
        env_prefix = "service_"
        env_file = ".env"
