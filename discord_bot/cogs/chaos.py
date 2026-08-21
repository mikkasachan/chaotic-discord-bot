from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name, pick


class Chaos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot





async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chaos(bot))