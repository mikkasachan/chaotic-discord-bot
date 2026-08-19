from __future__ import annotations

import random
from typing import Iterable

import discord

COLORS = {
    "pink": discord.Color.from_rgb(255, 91, 146),
    "purple": discord.Color.from_rgb(155, 89, 255),
    "gold": discord.Color.from_rgb(255, 193, 7),
    "green": discord.Color.from_rgb(46, 204, 113),
    "red": discord.Color.from_rgb(231, 76, 60),
    "blue": discord.Color.from_rgb(52, 152, 219),
}


def pick(items: Iterable[str]) -> str:
    return random.choice(tuple(items))


def embed(title: str, description: str, color: str = "purple") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=COLORS[color])


def member_name(member: discord.abc.User) -> str:
    return getattr(member, "display_name", member.name)


def clamp_text(text: str, limit: int = 900) -> str:
    return text if len(text) <= limit else f"{text[:limit - 1]}…"