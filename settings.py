from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str = "alfabet"
    jwt_algorithem: str = 'HS256'
    hash_salt: bytes = b"$2a$12$w40nlebw3XyoZ5Cqke14M."
    db_username: str = 'postgres'
    db_database: str = 'postgres'
    db_password: str = 'alfabet'
    db_host: str = ''


settings = Settings()
