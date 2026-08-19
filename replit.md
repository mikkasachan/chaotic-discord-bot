# ChaosBot

A lightweight Discord entertainment bot with harmless social commands, SQLite stats, and multiplayer chaos games.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string
- `python -m discord_bot` — run the Discord bot
- Required secret: `DISCORD_TOKEN` — Discord bot token stored in Replit Secrets

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5 (existing shared service)
- Discord bot: Python 3 + discord.py 2.x
- Bot database: SQLite with WAL mode, `discord_bot/data/chaosbot.sqlite3`

## Where things live

- `discord_bot/main.py` — bot entry point, intents, extension loading, slash-command sync
- `discord_bot/config.py` — environment-only configuration
- `discord_bot/db.py` — SQLite schema and atomic stat updates
- `discord_bot/cogs/core.py` — `/ping`, `/help`, `/whoasked`, lightweight message counters
- `discord_bot/cogs/entertainment.py` — roasts, court, lore, fortune, experiments, ratings, useless commands
- `discord_bot/cogs/games.py` — mini-games, Final Boss, Last One Standing
- `discord_bot/cogs/chaos.py` — events, yap stats, server wrapped

## Architecture decisions

- Slash commands are synced globally on startup; no text command prefix is exposed.
- Message content is only read in memory to count words and trigger the configurable, cooldown-protected Who Asked detector; it is never stored.
- Final Boss and Last One Standing state is intentionally in memory and temporary; user statistics persist in SQLite.
- All generated gameplay is harmless and avoids moderation or destructive server APIs.

## Product

ChaosBot provides harmless roasts, fake court cases, evolving member lore, fortunes, random experiments, arbitrary ratings, funny server events, yap statistics, server summaries, a temporary Final Boss, quick mini-games, and a 4–30 player Last One Standing elimination game.

## User preferences

- Personality: chaotic, funny, Gen-Z, slightly unhinged, but not genuinely offensive.
- Never hardcode or request a Discord token in chat.

## Gotchas

- Enable Guilds, Guild Messages, and Message Content intents in the Discord Developer Portal.
- Invite with only View Channels, Send Messages, Embed Links, Read Message History, and Use Application Commands. Administrator is not needed.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
