from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
