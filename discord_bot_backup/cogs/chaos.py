from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name, pick


class Chaos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="event", description="Trigger a harmless temporary server event.")
    async def event(self, interaction: discord.Interaction) -> None:
        events = (
            ("The Snack Tax", "For the next 5 minutes, anyone who says 'literally' owes the chat one imaginary chip."),
            ("NPC Mode", "The next three messages must include a dramatic stage direction."),
            ("Weather Update", "It is now raining confetti in the vibes. No cleanup required."),
            ("Alliance Arc", "Everyone pair up with a random person and invent a team name."),
            ("Critical Hit", "The next person to send a GIF receives +10 imaginary charisma."),
        )
        title, description = pick(events)
        self.bot.db.bump_guild(interaction.guild_id, events=1)
        await interaction.response.send_message(embed(f"📣 Server Event: {title}", f"{description}\n\nDuration: **temporary**\nImpact: **zero server damage**", "pink"))

    @app_commands.command(name="yap", description="Inspect funny lightweight message statistics.")
    @app_commands.describe(member="Whose yap stats?")
    async def yap(self, interaction: discord.Interaction, member: discord.Member | None = None) -> None:
        target = member or interaction.user
        row = self.bot.db.user(interaction.guild_id, target.id)
        messages, words = row["messages"], row["words"]
        avg = round(words / messages, 1) if messages else 0
        title = "Yap Apprentice" if avg < 12 else "Certified Yapper" if avg < 30 else "Yap Final Boss"
        await interaction.response.send_message(embed(f"🗣️ Yap Detector: {member_name(target)}", f"Rank: **{title}**\nMessages counted: `{messages}`\nWords counted: `{words}`\nAverage words/message: `{avg}`\n\nOnly counts are stored. Message content is not saved.", "blue"))

    @app_commands.command(name="wrapped", description="Get a weekly or monthly funny server activity summary.")
    @app_commands.describe(period="Which time window should be wrapped?")
    @app_commands.choices(period=[
        app_commands.Choice(name="Weekly", value="week"),
        app_commands.Choice(name="Monthly", value="month"),
    ])
    async def wrapped(self, interaction: discord.Interaction, period: app_commands.Choice[str] | None = None) -> None:
        guild_id = interaction.guild_id
        days = 30 if period and period.value == "month" else 7
        label = "Monthly" if days == 30 else "Weekly"
        guild = self.bot.db.guild(guild_id)
        top_yapper = self.bot.db.top_period(guild_id, "words", days)
        top_roasted = self.bot.db.top(guild_id, "roasts_received")
        top_active = self.bot.db.top_period(guild_id, "messages", days)
        def who(rows: list) -> str:
            return f"<@{rows[0]['user_id']}>" if rows else "the silent majority"
        await interaction.response.send_message(embed(
            f"📦 {label} Server Wrapped",
            f"**Top yapper:** {who(top_yapper)}\n"
            f"**Most roasted:** {who(top_roasted)}\n"
            f"**Most active:** {who(top_active)}\n"
            f"**Messages counted:** `{self.bot.db.period_total(guild_id, 'messages', days)}`\n"
            f"**Games played:** `{guild['games_played']}`\n"
            f"**Events triggered:** `{guild['events']}`\n"
            f"**Rating requests:** `{guild['rate_requests']}`\n\n"
            f"Period: last `{days}` days. The spreadsheet is powered by vibes.",
            "purple",
        ))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chaos(bot))