import random
import discord
from discord.ext import commands
from discord import app_commands


FORTUNES = [
    "Aaj kismat tumhare side hai 🍀",
    "Aaj risk liya toh fayda ho sakta hai 👀",
    "Aaj ka din thoda sus hai... sambhal ke 😭",
    "Kismat bol rahi hai: try kar le 😎",
    "Aaj luck: 69% — baaki Bhagwan bharose 💀",
    "Aaj kuch unexpected accha ho sakta hai ✨",
    "Aaj patience rakho, result mil sakta hai 🔮",
    "Kismat ne aaj tumhe VIP pass diya hai 👑",
]


class Kismat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kismat", description="Apni aaj ki kismat dekho 🔮")
    async def kismat(self, interaction: discord.Interaction):
        fortune = random.choice(FORTUNES)
        luck = random.randint(1, 100)

        embed = discord.Embed(
            title="🔮 Aaj Ki Kismat",
            description=f"**{fortune}**\n\n🍀 **Luck:** `{luck}%`",
            color=discord.Color.gold(),
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kismat(bot))
