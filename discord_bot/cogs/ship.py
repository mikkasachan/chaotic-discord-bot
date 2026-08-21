import discord
from discord import app_commands
from discord.ext import commands
import hashlib


class Ship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ship",
        description="Check the fictional compatibility between two members."
    )
    @app_commands.describe(
        user1="First member",
        user2="Second member"
    )
    async def ship(
        self,
        interaction: discord.Interaction,
        user1: discord.Member,
        user2: discord.Member
    ):
        pair = ":".join(sorted([str(user1.id), str(user2.id)]))
        score = int(hashlib.sha256(pair.encode()).hexdigest(), 16) % 101

        # ❤️ LOVE BAR
        filled = score // 10
        empty = 10 - filled
        love_bar = "❤️" * filled + "🖤" * empty

        if score >= 90:
            verdict = "💍 Soulmate level! This is dangerously perfect."
        elif score >= 75:
            verdict = "💖 Pretty strong match! There is definitely something here."
        elif score >= 50:
            verdict = "💕 There might be something here..."
        elif score >= 25:
            verdict = "💀 It's complicated. Proceed with caution."
        else:
            verdict = "🚫 Absolutely cursed. Run."

        embed = discord.Embed(
            title="💘 LOVE-O-METER",
            description=(
                f"## 💕 {user1.display_name} × {user2.display_name}\n\n"
                f"{love_bar}\n\n"
                f"💗 **Compatibility: {score}%**\n"
                f"{verdict}"
            ),
            color=discord.Color.from_rgb(255, 105, 180)
        )

        # 👤 Profile photos
        embed.set_thumbnail(url=user1.display_avatar.url)
        embed.set_image(url=user2.display_avatar.url)

        embed.add_field(
            name="💞 The Pair",
            value=f"**{user1.display_name}** 💕 **{user2.display_name}**",
            inline=False
        )

        embed.add_field(
            name="🔮 Relationship Status",
            value=verdict,
            inline=False
        )

        embed.set_footer(
            text="💘 Powered by the completely scientific Love-O-Meter"
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ship(bot))