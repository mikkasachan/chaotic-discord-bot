from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    token: str
    db_path: Path
    log_level: str
    who_asked_min_length: int
    who_asked_cooldown: int


def load_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token:
        raise RuntimeError("DISCORD_TOKEN is missing. Add it in Replit Secrets.")
    db_path = Path(os.getenv("BOT_DB_PATH", "data/chaosbot.sqlite3"))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return Settings(
        token=token,
        db_path=db_path,
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        who_asked_min_length=max(40, int(os.getenv("WHO_ASKED_MIN_LENGTH", "180"))),
        who_asked_cooldown=max(10, int(os.getenv("WHO_ASKED_COOLDOWN_SECONDS", "45"))),
    )