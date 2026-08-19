from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Database:
    """Small synchronous SQLite wrapper; each operation is short and atomic."""

    def __init__(self, path: Path):
        self.path = path
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA busy_timeout=3000")
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS user_stats (
                guild_id INTEGER NOT NULL, user_id INTEGER NOT NULL,
                messages INTEGER DEFAULT 0, words INTEGER DEFAULT 0,
                roasts_received INTEGER DEFAULT 0, roasts_given INTEGER DEFAULT 0,
                lore_level INTEGER DEFAULT 0, games_played INTEGER DEFAULT 0,
                experiments INTEGER DEFAULT 0, fortunes INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            );
            CREATE TABLE IF NOT EXISTS guild_stats (
                guild_id INTEGER PRIMARY KEY, games_played INTEGER DEFAULT 0,
                messages INTEGER DEFAULT 0, roasts INTEGER DEFAULT 0,
                events INTEGER DEFAULT 0, rate_requests INTEGER DEFAULT 0,
                updated_at TEXT
            );
            CREATE TABLE IF NOT EXISTS message_daily (
                guild_id INTEGER NOT NULL, user_id INTEGER NOT NULL,
                day TEXT NOT NULL, messages INTEGER DEFAULT 0, words INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, user_id, day)
            );
            CREATE TABLE IF NOT EXISTS server_settings (
                guild_id INTEGER PRIMARY KEY, who_asked_enabled INTEGER DEFAULT 1
            );
            """
        )
        self.connection.commit()

    def _ensure_user(self, guild_id: int, user_id: int) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO user_stats (guild_id, user_id) VALUES (?, ?)",
            (guild_id, user_id),
        )

    def bump_user(self, guild_id: int, user_id: int, **fields: int) -> None:
        self._ensure_user(guild_id, user_id)
        allowed = {"messages", "words", "roasts_received", "roasts_given",
                   "lore_level", "games_played", "experiments", "fortunes"}
        clean = {key: value for key, value in fields.items() if key in allowed}
        if clean:
            assignments = ", ".join(f"{key} = {key} + ?" for key in clean)
            self.connection.execute(
                f"UPDATE user_stats SET {assignments} WHERE guild_id = ? AND user_id = ?",
                (*clean.values(), guild_id, user_id),
            )
        self.connection.commit()

    def record_message(self, guild_id: int, user_id: int, word_count: int) -> None:
        day = datetime.now(timezone.utc).date().isoformat()
        self.bump_user(guild_id, user_id, messages=1, words=word_count)
        self.connection.execute(
            """INSERT INTO message_daily (guild_id, user_id, day, messages, words)
               VALUES (?, ?, ?, 1, ?)
               ON CONFLICT(guild_id, user_id, day) DO UPDATE SET
               messages = messages + 1, words = words + excluded.words""",
            (guild_id, user_id, day, word_count),
        )
        self.bump_guild(guild_id, messages=1)
        self.connection.commit()

    def bump_guild(self, guild_id: int, **fields: int) -> None:
        allowed = {"games_played", "messages", "roasts", "events", "rate_requests"}
        self.connection.execute(
            "INSERT OR IGNORE INTO guild_stats (guild_id, updated_at) VALUES (?, ?)",
            (guild_id, datetime.now(timezone.utc).isoformat()),
        )
        clean = {key: value for key, value in fields.items() if key in allowed}
        if clean:
            assignments = ", ".join(f"{key} = {key} + ?" for key in clean)
            self.connection.execute(
                f"UPDATE guild_stats SET {assignments}, updated_at = ? WHERE guild_id = ?",
                (*clean.values(), datetime.now(timezone.utc).isoformat(), guild_id),
            )
        self.connection.commit()

    def user(self, guild_id: int, user_id: int) -> sqlite3.Row:
        self._ensure_user(guild_id, user_id)
        self.connection.commit()
        return self.connection.execute(
            "SELECT * FROM user_stats WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        ).fetchone()

    def top(self, guild_id: int, field: str, limit: int = 1) -> list[sqlite3.Row]:
        if field not in {"messages", "words", "roasts_received", "roasts_given", "games_played"}:
            raise ValueError("unsupported stats field")
        return list(self.connection.execute(
            f"SELECT * FROM user_stats WHERE guild_id = ? ORDER BY {field} DESC LIMIT ?",
            (guild_id, limit),
        ).fetchall())

    def top_period(self, guild_id: int, field: str, days: int, limit: int = 1) -> list[sqlite3.Row]:
        if field not in {"messages", "words"}:
            raise ValueError("period stats support message counts only")
        rows = self.connection.execute(
            f"""SELECT user_id, SUM({field}) AS period_value
                FROM message_daily
                WHERE guild_id = ? AND day >= date('now', ?)
                GROUP BY user_id ORDER BY period_value DESC LIMIT ?""",
            (guild_id, f"-{days} days", limit),
        ).fetchall()
        return list(rows)

    def period_total(self, guild_id: int, field: str, days: int) -> int:
        if field not in {"messages", "words"}:
            raise ValueError("period stats support message counts only")
        row = self.connection.execute(
            f"""SELECT COALESCE(SUM({field}), 0) AS total FROM message_daily
                WHERE guild_id = ? AND day >= date('now', ?)""",
            (guild_id, f"-{days} days"),
        ).fetchone()
        return int(row["total"])

    def guild(self, guild_id: int) -> sqlite3.Row:
        self.bump_guild(guild_id)
        return self.connection.execute(
            "SELECT * FROM guild_stats WHERE guild_id = ?", (guild_id,)
        ).fetchone()

    def setting(self, guild_id: int, name: str = "who_asked_enabled") -> bool:
        row = self.connection.execute(
            "SELECT who_asked_enabled FROM server_settings WHERE guild_id = ?", (guild_id,)
        ).fetchone()
        return bool(row[name]) if row else True

    def set_setting(self, guild_id: int, enabled: bool) -> None:
        self.connection.execute(
            """INSERT INTO server_settings (guild_id, who_asked_enabled) VALUES (?, ?)
               ON CONFLICT(guild_id) DO UPDATE SET who_asked_enabled = excluded.who_asked_enabled""",
            (guild_id, int(enabled)),
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()