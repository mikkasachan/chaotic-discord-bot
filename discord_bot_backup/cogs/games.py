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

    @app_commands.command(name="game", description="Play a tiny multiplayer-friendly chaos game.")
    async def game(self, interaction: discord.Interaction) -> None:
        title, rules, result = random.choice((
            ("Emoji Charades", "Describe a movie using three emojis.", "The winning answer is whatever gets the loudest reaction."),
            ("Hot Take Roulette", "Everyone posts a harmless hot take.", "The most cursed take wins imaginary points."),
            ("Speed Lore", "First person tagged gets 10 seconds to invent a backstory.", "Canon accepted. Continuity not guaranteed."),
            ("Alphabet Duel", "Pick a letter; everyone names a snack starting with it.", "The last snack standing claims the pantry."),
        ))
        self.bot.db.bump_guild(interaction.guild_id, games_played=1)
        self.bot.db.bump_user(interaction.guild_id, interaction.user.id, games_played=1)
        await interaction.response.send_message(embed(f"🎮 {title}", f"**Rules:** {rules}\n\n**Outcome:** {result}", "blue"))

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

    @app_commands.command(name="boss_status", description="Inspect the current Final Boss.")
    async def boss_status(self, interaction: discord.Interaction) -> None:
        boss = self.bosses.get(interaction.guild_id)
        if not boss:
            return await interaction.response.send_message("No Final Boss. The arena is suspiciously peaceful.", ephemeral=True)
        target = interaction.guild.get_member(boss["member_id"]) if interaction.guild else None
        await interaction.response.send_message(embed("👑 Boss Status", f"**{member_name(target) if target else 'Unknown entity'}**\nHP: `{boss['hp']}/{boss['max_hp']}`\nWeakness: **{boss['weakness']}**", "red"))

    @app_commands.command(name="boss_attack", description="Attack the Final Boss with a funny move.")
    @app_commands.describe(move="Your attack style")
    @app_commands.choices(move=[app_commands.Choice(name=x.title(), value=x) for x in ("compliment", "dad_joke", "side_eye", "dramatic_entrance")])
    async def boss_attack(self, interaction: discord.Interaction, move: app_commands.Choice[str]) -> None:
        boss = self.bosses.get(interaction.guild_id)
        if not boss:
            return await interaction.response.send_message("There is no boss to bonk.", ephemeral=True)
        damage = random.randint(8, 28)
        if move.value.replace("_", " ") in boss["weakness"]:
            damage += 20
        boss["hp"] = max(0, boss["hp"] - damage)
        outcome = "The boss has been defeated by the power of nonsense." if boss["hp"] == 0 else f"The boss is visibly reconsidering the plot. `{boss['hp']}/{boss['max_hp']}` HP remains."
        await interaction.response.send_message(embed("⚔️ Boss Battle", f"**{member_name(interaction.user)}** used `{move.name}` for **{damage} damage**.\n\n{outcome}", "gold"))
        if boss["hp"] == 0:
            self.bosses.pop(interaction.guild_id, None)

    @app_commands.command(name="laststanding", description="Start, join, or inspect the elimination game.")
    @app_commands.describe(action="What you want to do", choice="Your action for the current round")
    @app_commands.choices(
        action=[app_commands.Choice(name=x.title(), value=x) for x in ("start", "join", "begin", "status", "act")],
        choice=[app_commands.Choice(name=x.title(), value=x) for x in ACTIONS],
    )
    async def laststanding(self, interaction: discord.Interaction, action: app_commands.Choice[str], choice: app_commands.Choice[str] | None = None) -> None:
        if not interaction.guild:
            return await interaction.response.send_message("This game needs a server.", ephemeral=True)
        guild_id = interaction.guild.id
        game = self.standing.get(guild_id)
        if action.value == "start":
            if game:
                return await interaction.response.send_message("A Last One Standing game already exists here.", ephemeral=True)
            self.standing[guild_id] = StandingGame(interaction.user.id, {interaction.user.id: member_name(interaction.user)})
            await interaction.response.send_message(embed("🏁 Last One Standing", f"**{member_name(interaction.user)}** opened the arena.\nPlayers: `1/30`\nUse `/laststanding action:join` to enter, then the host uses `begin`.", "green"))
            return
        if not game:
            return await interaction.response.send_message("No game running. Use `/laststanding action:start`.", ephemeral=True)
        if action.value == "join":
            if game.started:
                return await interaction.response.send_message("The doors are locked; this game already started.", ephemeral=True)
            if interaction.user.id in game.players:
                return await interaction.response.send_message("You are already in the arena.", ephemeral=True)
            if len(game.players) >= 30:
                return await interaction.response.send_message("The arena is full (30 players).", ephemeral=True)
            game.players[interaction.user.id] = member_name(interaction.user)
            await interaction.response.send_message(f"**{member_name(interaction.user)}** joined. Players: `{len(game.players)}/30`.")
            return
        if action.value == "begin":
            if interaction.user.id != game.host_id:
                return await interaction.response.send_message("Only the host can start the chaos.", ephemeral=True)
            if len(game.players) < 4:
                return await interaction.response.send_message("Need at least **4 players** so the drama has witnesses.", ephemeral=True)
            game.started, game.alive = True, set(game.players)
            await self._new_round(interaction, game)
            return
        if action.value == "status":
            living = ", ".join(game.players[p] for p in game.alive) if game.started else ", ".join(game.players.values())
            await interaction.response.send_message(embed("🏁 Arena Status", f"Round: `{game.round_no}`\nState: **{'live' if game.started else 'lobby'}**\nPlayers: {living}", "green"))
            return
        if action.value == "act":
            if not game.started or interaction.user.id not in game.alive:
                return await interaction.response.send_message("You are not an active player in a live round.", ephemeral=True)
            if not choice:
                return await interaction.response.send_message(f"Choose one: {', '.join(ACTIONS)}.", ephemeral=True)
            game.choices[interaction.user.id] = choice.value
            await interaction.response.send_message(f"Action locked: `{choice.value}`. The arena has received your questionable decision.", ephemeral=True)
            if game.alive and game.choices.keys() >= game.alive:
                await self._resolve_round(interaction, game)

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