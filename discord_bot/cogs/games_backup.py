from __future__ import annotations

import random
from dataclasses import dataclass, field

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name, pick


@dataclass
class StandingGame:
    host_id: int
    players: dict[int, str] = field(default_factory=dict)
    alive: set[int] = field(default_factory=set)
    round_no: int = 0
    choices: dict[int, str] = field(default_factory=dict)
    started: bool = False


SITUATIONS = (
    "The floor is now legally soup. Pick your survival strategy.",
    "A goose with a clipboard is auditing everyone.",
    "The server has one charger and 30% battery total.",
    "A portal opened and is offering suspiciously good snacks.",
    "The group chat has become a reality show with no producer.",
)
ACTIONS = ("hide", "negotiate", "snack", "yeet", "dance")


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.standing: dict[int, StandingGame] = {}
        self.bosses: dict[int, dict] = {}


    async def boss(self, interaction: discord.Interaction) -> None:
        if not interaction.guild:
            return await interaction.response.send_message("Final Bosses need a server arena.", ephemeral=True)
        candidates = [m for m in interaction.guild.members if not m.bot]
        if not candidates:
            return await interaction.response.send_message("No mortal members found.", ephemeral=True)
        target = random.choice(candidates)
        boss = {
            "member_id": target.id, "hp": random.randint(80, 160),
            "max_hp": 0, "weakness": pick(("compliments", "dad jokes", "dramatic entrances", "being asked nicely")),
            "abilities": random.sample(("tax paperwork", "summon a minor inconvenience", "weaponized side-eye", "confusing monologue"), 2),
        }
        boss["max_hp"] = boss["hp"]
        self.bosses[interaction.guild.id] = boss
        self.bot.db.bump_guild(interaction.guild.id, events=1)
        await interaction.response.send_message(embed("👑 FINAL BOSS SPAWNED", f"**{member_name(target)}** has become the temporary Final Boss.\n\nHP: `{boss['hp']}/{boss['max_hp']}`\nWeakness: **{boss['weakness']}**\nAbilities: {', '.join(boss['abilities'])}\n\nUse `/boss_attack` to bonk the narrative.", "red"))




    async def _new_round(self, interaction: discord.Interaction, game: StandingGame, followup: bool = False) -> None:
        game.round_no += 1
        game.choices.clear()
        message = embed(f"🏁 Round {game.round_no}", f"**Situation:** {pick(SITUATIONS)}\n\nChoose secretly-ish with `/laststanding action:act choice:<{' | '.join(ACTIONS)}>`.\nSurvivors this round: `{len(game.alive)}`", "green")
        if followup:
            await interaction.channel.send(embed=message)
        else:
            await interaction.response.send_message(embed=message)

    async def _resolve_round(self, interaction: discord.Interaction, game: StandingGame) -> None:
        # Hidden outcome: action names are flavorful, but survival is randomized with a
        # small round-scaled elimination so four players remain fun and meaningful.
        count = len(game.alive)
        eliminate = 1 if count <= 6 else max(1, count // 4)
        ranked = list(game.alive)
        random.shuffle(ranked)
        losers = set(ranked[:eliminate])
        game.alive -= losers
        names = ", ".join(game.players[p] for p in losers)
        if len(game.alive) == 1:
            winner = game.players[next(iter(game.alive))]
            self.bot.db.bump_guild(interaction.guild_id, games_played=1)
            await interaction.channel.send(embed("🏆 LAST ONE STANDING", f"**{winner}** wins after surviving the situation economy.\nEliminated this round: {names}", "gold"))
            self.standing.pop(interaction.guild.id, None)
        else:
            await interaction.channel.send(embed(f"💥 Round {game.round_no} Resolved", f"Eliminated: **{names}**\nRemaining: `{len(game.alive)}`\n\nThe arena reloads its nonsense.", "red"))
            await self._new_round(interaction, game, followup=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Games(bot))