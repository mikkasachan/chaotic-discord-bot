import os
import discord
from discord.ext import commands

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Sync error: {e}")

async def main():
    for cog in ["games","chaos","core","kalesh","lore","entertainment","roast","experiment","kismat","boss","survive"]:
        await bot.load_extension(f"discord_bot.cogs.{cog}")
    await bot.start(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
