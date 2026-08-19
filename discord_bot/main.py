from __future__ import annotations

import asyncio
import logging

import discord
from discord.ext import commands

from .config import load_settings
from .db import Database

COGS = (
    "discord_bot.cogs.core",
        "discord_bot.cogs.roast",
        "discord_bot.cogs.kalesh",
        "discord_bot.cogs.lore",
    "discord_bot.cogs.entertainment",
    "discord_bot.cogs.games",
    "discord_bot.cogs.chaos",
)


class ChaosBot(commands.Bot):
    def __init__(self, database: Database):
        intents = discord.Intents(guilds=True, messages=True, message_content=True)
        super().__init__(command_prefix=commands.when_mentioned, intents=intents,
                         help_command=None)
        self.db = database

    async def setup_hook(self) -> None:
        for cog in COGS:
            await self.load_extension(cog)
        synced = await self.tree.sync()
        logging.getLogger(__name__).info("Synced %d slash commands", len(synced))

    async def on_ready(self) -> None:
        logging.getLogger(__name__).info("Logged in as %s (%s)", self.user, self.user.id)


def main() -> None:
    settings = load_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    bot = ChaosBot(Database(settings.db_path))
    bot.settings = settings
    try:
        bot.run(settings.token, log_handler=None)
    except discord.LoginFailure:
        logging.getLogger(__name__).error("Discord rejected DISCORD_TOKEN.")
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Shutdown requested.")
    finally:
        bot.db.close()