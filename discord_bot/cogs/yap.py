import json
import random
import aiohttp
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands


SETTINGS_FILE = Path("discord_bot/yap_channels.json")


VERDICTS = [
    "Bhai bas kar 😭 itna yap kyun kar raha hai?",
    "Yeh message nahi, poora podcast tha 💀",
    "Kisi ne poocha bhi nahi tha bhai 😭",
    "Bhai keyboard ko thoda rest de 🗿",
    "Itna bol diya ki anime character bhi thak gaya 💀",
    "Yap level dangerous hai, paani pee le 😂",
    "Bhai tu rukega ya season 2 bhi aayega? 😭",
    "Kahani interesting thi... par bahut lambi thi 💀",
    "Yeh yap nahi, Mahabharat ka extended version hai 😭",
    "Bhai 3 line bolne aaya tha, novel likh diya 💀",
]


class Yap(commands.GroupCog, group_name="yap", group_description="Enable or disable Yap in this channel"):
    def __init__(self, bot):
        self.bot = bot
        self.enabled_channels = self.load_settings()
        self.recent_reactions = []
        self.recent_verdicts = []
        self.used_verdicts = []

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id not in self.enabled_channels:
            return

        content = message.content.strip()

        # Short messages ko ignore karo
        if len(content) < 120:
            return

        # Recent replies repeat mat karo
        # 🧠 Anti-repeat verdict system
        unique_verdicts = list(dict.fromkeys(VERDICTS))
        available = [
            v for v in unique_verdicts
            if v not in self.recent_verdicts
        ]

        if not available:
            self.recent_verdicts.clear()
            available = unique_verdicts

        verdict = random.choice(available)
        self.recent_verdicts.append(verdict)

        # Last 20 verdicts repeat nahi honge
        if len(self.recent_verdicts) > 20:
            self.recent_verdicts.pop(0)

        # 🎭 Anime character reaction
        reaction_categories = [
            "angry", "baka", "bleh", "blush", "bored",
            "confused", "cry", "facepalm", "happy", "laugh",
            "nope", "pout", "shrug", "shocked", "sleep",
            "smug", "stare", "think", "yawn", "yeet",
            "bonk", "slap", "teehee"
        ]

        reaction_url = None

        try:
            async with aiohttp.ClientSession() as session:
                for _ in range(6):
                    category = random.choice(reaction_categories)

                    async with session.get(
                        f"https://nekos.best/api/v2/{category}",
                        timeout=aiohttp.ClientTimeout(total=8)
                    ) as r:
                        if r.status != 200:
                            continue

                        data = await r.json()
                        candidate = data["results"][0]["url"]

                        if candidate not in self.recent_reactions:
                            reaction_url = candidate
                            break

        except Exception as e:
            print(f"⚠️ Anime reaction failed: {e}")

        # Embed mein anime character dikhao
        embed = discord.Embed(
            description=f"🗣️ **{verdict}**",
            color=discord.Color.orange()
        )

        if reaction_url:
            self.recent_reactions.append(reaction_url)

            if len(self.recent_reactions) > 20:
                self.recent_reactions.pop(0)

            embed.set_image(url=reaction_url)

        embed.set_footer(text="Yap detector activated 🎭")

        await message.channel.send(embed=embed)

    def load_settings(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(int(channel_id) for channel_id in data)
        except Exception:
            pass

        return set()

    def save_settings(self):
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(self.enabled_channels), f)

    @app_commands.command(
        name="enable",
        description="Enable Yap in this channel"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def enable(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id

        self.enabled_channels.add(channel_id)
        self.save_settings()

        await interaction.response.send_message(
            "🗣️ **Yap enabled!**\n"
            "Ab is channel mein zyada yap hua toh main pakad lunga 💀",
            ephemeral=True
        )

    @app_commands.command(
        name="disable",
        description="Disable Yap in this channel"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def disable(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id

        self.enabled_channels.discard(channel_id)
        self.save_settings()

        await interaction.response.send_message(
            "🤐")

async def setup(bot):
    cog = Yap(bot)
    await bot.add_cog(cog)
