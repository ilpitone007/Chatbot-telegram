from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    # Bot Telegram
    bot_token: str
    webhook_url: Optional[str] = None
    webhook_secret: str = "random_secret_string"
    bot_port: int = 8443

    # Sicurezza
    secret_key: str

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/anonchat.db"

    # Admin Dashboard
    admin_username: str = "admin"
    admin_password: str = "strong_password_here"
    admin_ip_whitelist: Optional[str] = None

    # Sessioni
    default_session_timeout_minutes: int = 60
    idle_timeout_minutes: int = 15
    queue_timeout_seconds: int = 60

    # Referral e Punti
    referral_link_ttl_hours: int = 48
    max_referral_per_day: int = 20
    points_expiry_months: int = 12

    # Notifiche scadenza punti
    expiry_warning_days: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

config = Settings()
