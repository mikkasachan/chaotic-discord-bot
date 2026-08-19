from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name


ROAST_TEMPLATES = (
    "Bhai teri aura itni low hai ki Wi-Fi bhi tujhe connect karne se pehle sochta hai.",
    "Tera confidence 4K hai, skills abhi bhi 144p mein buffering kar rahe hain.",
    "Bhai tu itna NPC hai ki dialogue options bhi tujhe ignore kar rahe hain.",
    "Teri planning dekh ke Google Maps bhi bolta hai: bhai khud dekh le.",
    "Tu group chat ka woh banda hai jiska message padh ke sab notification clear kar dete hain.",
    "Tera brain loading screen pe atka hai aur cancel button bhi resign kar chuka hai.",
    "Bhai teri decision-making dekh ke coin toss bhi therapist ke paas jaata hai.",
    "Teri vibe itni side-character hai ki background music bhi tujhe skip kar deta hai.",
    "Tu skill issue ko personality bana ke ghoom raha hai, respect the commitment.",
    "Bhai tu itna late reply karta hai ki conversation ka sequel aa jaata hai.",
    "Teri aura negative mein hai, calculator bhi tujhe dekh ke error dikha raha hai.",
    "Tu woh banda hai jo tutorial padh ke bhi game ko blame karta hai.",
    "Bhai tera Wi-Fi signal aur tera focus dono ek hi tower se bhaage hue hain.",
    "Teri life ka plot twist har baar bas ek aur bad decision hota hai.",
    "Tu itna confused hai ki Google bhi search bar mein likhta hai: bhai decide kar.",
    "Bhai teri strategy dekh ke chess pieces khud random move karne lagte hain.",
    "Tera confidence main character ka hai, par entry side gate se hoti hai.",
    "Tu group project ka woh member hai jo bas 'seen' karke contribution samajhta hai.",
    "Bhai teri braincells ne group chat bana ke tujhe mute kar diya hai.",
    "Teri typing speed fast hai, par thoughts abhi dial-up internet pe chal rahe hain.",
    "Tu itna overthink karta hai ki simple question bhi courtroom drama ban jaata hai.",
    "Bhai teri timing itni kharaab hai ki punchline bhi tujhe dekh ke awkward ho jaati hai.",
    "Teri personality ka update install hua tha, par restart kabhi complete nahi hua.",
    "Tu woh NPC hai jo same line repeat karta hai aur phir usse wisdom bolta hai.",
    "Bhai teri memory selective nahi, full-time vacation pe hai.",
    "Tera aura dekh ke even the loading icon bolta hai: thoda jaldi kar bhai.",
    "Tu plan banata hai jaise CEO, execute karta hai jaise sleepy intern.",
    "Bhai tera logic itna creative hai ki reality ne tujhe beta access de diya.",
    "Teri conversation mein plot nahi, bas unnecessary filler episodes hain.",
    "Tu notification jaisa hai: aate hi sab pehle swipe karte hain.",
    "Bhai teri productivity ka screenshot hamesha 'kal se pakka' hota hai.",
    "Tera brain ek browser hai jisme 47 tabs open hain aur sab mein buffering chal rahi hai.",
    "Tu itna dramatic hai ki chhota sa typo bhi season finale bana deta hai.",
    "Bhai tera common sense online hai, par last seen kal ka hai.",
    "Teri confidence ki battery 100% hai, par performance power-saving mode mein.",
    "Tu advice aise deta hai jaise life sorted ho, jabki khud ka charger nahi milta.",
    "Bhai teri vibe 'do not disturb' pe hai, par chaos phir bhi full volume mein aata hai.",
    "Tera comeback itna late aata hai ki tab tak topic ka naam bhi badal chuka hota hai.",
    "Tu woh banda hai jo shortcut dhoondte dhoondte extra 5 kilometre chala jaata hai.",
    "Bhai teri planning ko dekh ke calendar bhi bolta hai: mujhe beech mein mat lao.",
    "Tera focus itna slippery hai ki thought pakadne se pehle hi nikal jaata hai.",
    "Tu main character banna chahta hai, par abhi tak intro scene mein atka hua hai.",
    "Bhai teri energy Monday morning ke alarm jaisi hai: loud, confusing, aur unwanted.",
    "Tera brainrot itna advanced hai ki memes bhi tujhe context samjhate hain.",
    "Tu har situation mein expert banta hai, bas apni situation chhod ke.",
    "Bhai teri social battery full dikhti hai, par charger kisi aur ke paas hai.",
    "Teri life ka compass har baar 'thoda aur chaos' ki direction mein ghoomta hai.",
    "Tu itna confidently galat hota hai ki sach bhi fact-check ke liye tere paas aata hai.",
    "Bhai teri typing mein confidence hai, grammar abhi respawn hone ka wait kar rahi hai.",
    "Teri vibe dekh ke algorithm bhi bolta hai: isko thoda fresh content dikhao.",
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

        roast = random.choice(ROAST_TEMPLATES)
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