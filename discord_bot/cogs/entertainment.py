from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import clamp_text, embed, member_name, pick

FORTUNES = (
    "A suspiciously good snack is approaching.",
    "You will say 'one more episode' and unlock a new timezone.",
    "Your next decision has a 72% chance of being iconic.",
    "The universe has put you on read, but it is thinking about it.",
    "A random compliment will hit you like a critical hit.",
)


class Entertainment(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot








async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Entertainment(bot))