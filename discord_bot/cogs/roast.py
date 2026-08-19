from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name


OPENERS = (
    "Bro has",
    "Bestie has",
    "This absolute legend has",
    "Respectfully, bro has",
    "The server has discovered that this person has",
)

ROAST_TEMPLATES = (
    "{opener} the aura of a loading screen on airport Wi-Fi.",
    "{opener} main-character confidence with side-character patch notes.",
    "{opener} so little aura even the NPCs are asking for directions.",
    "{opener} three braincells and all of them are buffering.",
    "{opener} the communication skills of a router during a thunderstorm.",
    "{opener} turned a skill issue into a full-time career.",
    "{opener} the energy of someone who says 'trust me' before making the worst decision.",
    "{opener} enough brainrot to make the algorithm request a wellness check.",
    "{opener} been yapping so long the subtitles filed for overtime.",
    "{opener} the stealth of a notification at 3 AM.",
    "{opener} a side quest personality and a final-boss level of confidence.",
    "{opener} the dramatic timing of a season finale nobody renewed.",
)

TAILS = (
    "The group chat is still processing.",
    "Even the loading icon is embarrassed.",
    "Please do not let this become a personality arc.",
    "The vibes are recoverable. Barely.",
    "Scientists are calling it a fascinating skill issue.",
    "The council has seen enough.",
)


class Roast(commands.Cog):
    """The isolated Beizzati feature."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roast", description="Give a member a harmless, randomized roast.")
    @app_commands.describe(user="The brave volunteer")
    @app_commands.checks.cooldown(1, 8.0, key=lambda interaction: (interaction.guild_id, interaction.user.id))
    async def roast(self, interaction: discord.Interaction, user: discord.Member) -> None:
        if not interaction.guild:
            await interaction.response.send_message(
                embed("🔥 BEIZZATI.exe", "This roast requires a server audience. The void has no comedic timing.", "red"),
                ephemeral=True,
            )
            return

        bot_user = self.bot.user
        if bot_user and user.id == bot_user.id:
            description = (
                f"{member_name(user)} tried to roast the bot, but the bot has already read its own source code.\n\n"
                f"**Counter-roast:** {member_name(interaction.user)} has the courage of a main character "
                "and the decision-making of a loading screen."
            )
            await interaction.response.send_message(embed("🤖 BEIZZATI.exe: SELF-ROAST PROTOCOL", description, "purple"))
            return

        if user.id == interaction.user.id:
            description = (
                f"**{member_name(user)}** attempted to roast themselves.\n\n"
                "That is either peak self-awareness or an advanced form of boredom. "
                "The council awards +4 courage and -2 aura."
            )
            await interaction.response.send_message(embed("🔥 BEIZZATI.exe", description, "gold"))
            return

        roast = random.choice(ROAST_TEMPLATES).format(opener=random.choice(OPENERS))
        aura = random.randint(-99, -11)
        braincells = random.choice(("Currently buffering...", "On airplane mode.", "One is doing its best.", "Out for maintenance."))
        response = embed(
            "🔥 BEIZZATI.exe",
            f"“{roast}”\n\n"
            f"💀 **Aura:** `{aura}`\n"
            f"🧠 **Braincells:** {braincells}\n\n"
            f"*{random.choice(TAILS)}*",
            "red",
        )
        self.bot.db.bump_user(interaction.guild.id, user.id, roasts_received=1)
        self.bot.db.bump_user(interaction.guild.id, interaction.user.id, roasts_given=1)
        self.bot.db.bump_guild(interaction.guild.id, roasts=1)
        await interaction.response.send_message(embed=response)

    @roast.error
    async def roast_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                embed(
                    "⏳ Beizzati cooldown",
                    f"Take a breath, bro. Try again in `{error.retry_after:.1f}s`.",
                    "gold",
                ),
                ephemeral=True,
            )
            return
        raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roast(bot))