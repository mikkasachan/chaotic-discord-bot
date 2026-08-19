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

    @app_commands.command(name="court", description="Put two members on trial for imaginary crimes.")
    @app_commands.describe(accused="The accused", witness="The alleged accomplice or witness")
    async def court(self, interaction: discord.Interaction, accused: discord.Member, witness: discord.Member) -> None:
        accusation = pick(("stealing the last brain cell", "weaponizing the group chat", "being suspiciously online at 3 AM", "crimes against punctuation"))
        evidence = pick(("a blurry screenshot", "one deeply concerned pigeon", "the vibes", "a snack wrapper with fingerprints"))
        verdict = pick(("GUILTY of being iconic", "NOT GUILTY, but under vibe surveillance", "hung jury; everyone got distracted", "guilty with a sentence of one dramatic apology"))
        case = embed("⚖️ Kalesh Court", f"**Case:** The People vs. {member_name(accused)}", "gold")
        case.add_field(name="Accusation", value=f"{member_name(accused)} is charged with **{accusation}**.", inline=False)
        case.add_field(name="Evidence", value=f"Exhibit A: **{evidence}**.", inline=True)
        case.add_field(name="Witness", value=f"{member_name(witness)} has been summoned for maximum confusion.", inline=True)
        case.add_field(name="Prosecution", value=pick(("The vibes are damning.", "Your honor, look at them.", "The allegations are aggressively plausible.")), inline=False)
        case.add_field(name="Defense", value=pick(("My client was lagging.", "They plead silly.", "No comment, only snacks.")), inline=False)
        case.add_field(name="Verdict", value=f"**{verdict}**", inline=False)
        await interaction.response.send_message(embed=case)

    @app_commands.command(name="fortune", description="Get a funny fortune for a member.")
    @app_commands.describe(member="The chosen one")
    async def fortune(self, interaction: discord.Interaction, member: discord.Member | None = None) -> None:
        target = member or interaction.user
        self.bot.db.bump_user(interaction.guild_id, target.id, fortunes=1)
        await interaction.response.send_message(
            embed("🔮 Kismat.exe", f"**{member_name(target)}:** {pick(FORTUNES)}\n\nConfidence: `{random.randint(11, 99)}%`", "blue")
        )

    @app_commands.command(name="experiment", description="Generate a harmless server experiment.")
    async def experiment(self, interaction: discord.Interaction) -> None:
        self.bot.db.bump_user(interaction.guild_id, interaction.user.id, experiments=1)
        subjects = pick(("the next person who types", "three volunteers", "the most suspicious profile picture", "everyone currently online"))
        task = pick(("must communicate using only food names for 60 seconds", "gets a ceremonial title chosen by the group", "must defend an obviously wrong opinion", "has to invent a new holiday"))
        await interaction.response.send_message(embed("🧪 Random Experiment", f"**Subjects:** {subjects}\n**Protocol:** {task}\n**Safety rating:** harmlessly unhinged", "green"))

    @app_commands.command(name="rate", description="Submit anything for an arbitrary funny rating.")
    @app_commands.describe(thing="What is being judged?")
    async def rate(self, interaction: discord.Interaction, thing: str) -> None:
        score = random.randint(0, 10)
        reasons = ("excellent goblin energy", "too powerful for this economy", "needs more dramatic lighting", "the council is divided", "would survive one Tuesday")
        self.bot.db.bump_guild(interaction.guild_id, rate_requests=1)
        await interaction.response.send_message(embed("📊 Completely Scientific Rating", f"**{clamp_text(thing, 240)}**\n\n## {score}/10\n{pick(reasons)}.\nPeer review: emotionally complicated.", "gold"))

    @app_commands.command(name="banana", description="Deploy a banana.")
    async def banana(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed("🍌 Banana", pick(("banana.", "the banana has unionized.", "this banana knows what you did.")), "gold"))

    @app_commands.command(name="why", description="Ask the ancient question.")
    async def why(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed("❓ Why", pick(("because the moon said so.", "for the plot.", "the prophecy was autocorrected.", "no one knows. especially me.")), "purple"))

    @app_commands.command(name="life", description="Receive life advice from a useless machine.")
    async def life(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed("🧠 Life Advice", pick(("drink water and stop opening the fridge for emotional support.", "you are doing great; the bar is in the basement but still.", "be mysterious. eat a vegetable occasionally.")), "green"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Entertainment(bot))