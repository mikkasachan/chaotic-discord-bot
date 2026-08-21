from __future__ import annotations

import discord
from discord.ext import commands

from ..utils import embed, pick


SUBJECTS = (
    "the next person who types",
    "three volunteers",
    "the most suspicious profile picture",
    "everyone currently online",
)

PROTOCOLS = (
    "must communicate using only food names for 60 seconds",
    "gets a ceremonial title chosen by the group",
    "must defend an obviously wrong opinion",
    "has to invent a new holiday",
)


class Experiment(commands.Cog):
    """The isolated harmless Random Experiment feature."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="experiment", description="Generate a harmless server experiment.")
    async def experiment(self, interaction: discord.Interaction) -> None:
        self.bot.db.bump_user(interaction.guild_id, interaction.user.id, experiments=1)
        subject = pick(SUBJECTS)
        protocol = pick(PROTOCOLS)
        await interaction.response.send_message(
            embed=embed(
                "🧪 Random Experiment",
                f"**Subjects:** {subject}\n"
                f"**Protocol:** {protocol}\n"
                "**Safety rating:** harmlessly unhinged",
                "green",
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Experiment(bot))