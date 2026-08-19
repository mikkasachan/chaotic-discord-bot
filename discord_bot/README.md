# ChaosBot

A lightweight, slash-command-only Discord entertainment bot built with `discord.py`.
It is intentionally not a moderation bot and never requests Administrator permissions.

## Run

From the repository root:

```bash
python -m discord_bot
```

The bot reads `DISCORD_TOKEN` from the environment and creates `data/chaosbot.sqlite3`
automatically. For local development, copy `.env.example` to `.env` and export the
variables yourself; Replit Secrets is recommended in hosted environments.

## Gateway intents

Enable **Guilds**, **Guild Messages**, and **Message Content** in the Discord Developer
Portal. The bot only uses Message Content to count lightweight message metadata for
the Yap Detector; it does not store message text or message history. No privileged
member intent is needed.

## Permissions

Invite it with only `View Channels`, `Send Messages`, `Embed Links`, and `Read Message
History` (plus `Use Application Commands`). It does not need Administrator,
Manage Server, ban, kick, delete, or channel-management permissions.