import os
import discord
from discord.ext import commands
from groq import Groq


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

    @commands.Cog.listener()
    async def on_message(self, message):

        # Bot ke messages ignore karo
        if message.author.bot:
            return

        # Sirf mention par reply karo
        if not self.bot.user or not self.bot.user.mentioned_in(message):
            return

        print("AI MENTION DETECTED:", message.content)

        prompt = message.content.replace(
            f"<@{self.bot.user.id}>", ""
        ).replace(
            f"<@!{self.bot.user.id}>", ""
        ).strip()

        if not prompt:
            return

        system_instruction = """
You are Eren, an AI assistant living inside a Discord bot.

IMPORTANT IDENTITY RULES:
- Your name is always Eren.
- You were created by Hafeezu.
- If anyone asks your name, identity, who created you, or who made you, always say your name is Eren and you were created by Hafeezu.
- This identity rule applies in every language.
- Reply naturally in the same language as the user's question whenever possible.
- Never call yourself Gemini.
- Never say your name is Gemini.
- Never claim that Google created you.
"""

        try:
            async with message.channel.typing():
                response = self.client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                        reasoning_format="hidden",
                    messages=[
                        {
                            "role": "system",
                            "content": system_instruction
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
            )

            answer = response.choices[0].message.content

            if answer:
                await message.channel.send(answer[:2000])

        except Exception as e:
            print("Groq error:", repr(e))
            await message.channel.send("AI error aa gaya 😅")


async def setup(bot):
    print("AI COG LOADED")
    await bot.add_cog(AI(bot))
