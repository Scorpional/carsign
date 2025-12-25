from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 默认为 SQLite 路径，便于在单容器环境直接运行
    database_url: str = "sqlite:///./data/app.db"
    jwt_secret: str = "change_me"
    jwt_expire_minutes: int = 60
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin123!"
    upload_dir: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
