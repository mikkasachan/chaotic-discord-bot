import random
import discord
from discord.ext import commands


class Boss(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="boss", description="Fight a random Final Boss!")
    async def boss(self, interaction: discord.Interaction):
        bosses = [
            ("👹 Chaos Demon", "The ruler of absolute chaos.", 100),
            ("⚡ Chaos Strike", "A boss powered by pure nonsense.", 120),
            ("🗿 Goblin Bonk", "Small goblin. Huge bonk.", 90),
        ]

        boss_name, description, hp = random.choice(bosses)

        attacks = [
            "💥 Reality Bonk",
            "⚡ Chaos Strike",
            "🗿 Goblin Bonk",
        ]

        attack = random.choice(attacks)
        damage = random.randint(10, 45)
        remaining = max(0, hp - damage)

        if remaining == 0:
            result = "🏆 **BOSS DEFEATED!**"
        elif remaining <= hp // 2:
            result = "😈 **Boss is getting nervous...**"
        else:
            result = "💀 **Boss is still standing.**"

        embed = discord.Embed(
            title="👹 FINAL BOSS",
            description=(
                f"**{boss_name}**\n\n"
                f"*{description}*\n\n"
                f"❤️ **HP:** `{remaining}/{hp}`\n"
                f"⚔️ **Attack:** {attack}\n"
                f"💥 **Damage:** `{damage}`\n\n"
                f"{result}"
            ),
            color=discord.Color.red(),
        )

        embed.set_footer(
            text=f"Challenged by {interaction.user.display_name}"
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Boss(bot))
