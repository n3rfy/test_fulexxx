from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    host: str = Field(..., env='DB_HOST')
    port: str = Field(..., env='DB_PORT')
    username: str = Field(..., env='DB_USERNAME')
    password: str = Field(..., env='DB_PASSWORD')
    database: str = Field(..., env='DB_DATABASE')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class HostSettings(BaseSettings):
    host: str = Field(..., env='HOST')
    port: str = Field(..., env='PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
