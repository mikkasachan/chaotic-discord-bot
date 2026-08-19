from __future__ import annotations

import time
from collections import defaultdict

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name, pick


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_who_asked: dict[int, float] = defaultdict(float)

    @app_commands.command(name="ping", description="Check if ChaosBot is alive.")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            embed=embed(
                "🏓 Pong!",
                f"Chaos latency: `{round(self.bot.latency * 1000)}ms`\nThe creature lives.",
                "green",
            )
        )

    @app_commands.command(name="help", description="See the ChaosBot command menu.")
    async def help(self, interaction: discord.Interaction) -> None:
        commands_text = (
            "**Social chaos**\n`/roast` `/court` `/lore` `/fortune` `/rate` `/whoasked`\n"
            "**Games**\n`/game` `/laststanding` `/boss` `/boss_attack` `/boss_status`\n"
            "**Server nonsense**\n`/experiment` `/event` `/wrapped` `/yap`\n"
            "**Useless but important**\n`/banana` `/why` `/life`"
        )
        await interaction.response.send_message(embed("ChaosBot command deck", commands_text, "pink"))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return
        words = len(message.content.split())
        self.bot.db.record_message(message.guild.id, message.author.id, words)
        settings = self.bot.settings
        if (
            len(message.content) >= settings.who_asked_min_length
            and self.bot.db.setting(message.guild.id)
            and time.monotonic() - self.last_who_asked[message.guild.id] >= settings.who_asked_cooldown
        ):
            self.last_who_asked[message.guild.id] = time.monotonic()
            if len(message.mentions) <= 6:
                await message.channel.send(
                    f"**Who asked?** {pick(['the paragraph department is concerned', 'bestie this is a TED Talk', 'the yap economy is booming'])}."
                )

    @app_commands.command(name="whoasked", description="Toggle the low-frequency long-message detector.")
    @app_commands.describe(enabled="Whether to react to very long messages")
    async def whoasked(self, interaction: discord.Interaction, enabled: bool) -> None:
        if not interaction.guild:
            return await interaction.response.send_message("This only works in a server.", ephemeral=True)
        self.bot.db.set_setting(interaction.guild.id, enabled)
        await interaction.response.send_message(
            embed("Who Asked settings", f"Long-message reactions are now **{'on' if enabled else 'off'}**.", "blue")
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core(bot))