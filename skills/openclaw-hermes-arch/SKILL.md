---
name: openclaw-hermes-arch
description: Use when understanding the relationship between OpenClaw Gateway and Hermes Agent.
metadata:
  hermes:
    platform: [cursor, codex, claude-code]
domain: integration
subdomain: architecture
tokens:
  scan: 105
  load: 1140
  category: standard
---

# OpenClaw & Hermes — Independent Systems (Both on Same iMac)

## Critical Architecture Finding (2026-04-29)

**Hermes Agent runs locally on the user's iMac, NOT on a cloud VM.** This was discovered mid-session when `tailscale status` showed only one node (chrisimac), `hostname` returned `ChrisdeiMac.local`, and `tailscale ip -1` returned `100.94.45.30` — the same Tailscale IP as the iMac.

**Implication:** All prior SSH setup (key generation, `from=` IP restriction, Tailscale tunnel) was unnecessary — Hermes was SSH-ing into its own machine. The SSH key setup `hermes_to_chris` served no real purpose since Hermes already has local terminal access.

**Critical finding:** OpenClaw Gateway and Hermes Agent are **two separate systems** on the same machine (iMac M1). They are not the same thing.

## Key Facts

| | OpenClaw Gateway | Hermes Agent |
|---|---|---|
| Process manager | PM2 | macOS launchd |
| Config | Shared .env | Shared .env |
| Telegram Token | Must NOT share | Must NOT share |
| Service file | PM2 list | ~/Library/LaunchAgents/hermes*.plist |
| Heartbeat | ~60 mins (token drain) | None by default |

## Token Conflict

Both using same Telegram Bot Token = packet loss / no response. Telegram delivers to whichever grabs it first. OpenClaw heartbeat drains rate limit.

**Fix:** Use a **separate dedicated Telegram Bot** for Hermes. Create via @BotFather, give new token to Hermes only.

**Current state:** Hermes runs with the original OpenClaw bot token. Architecture is independent but bot identity is inherited. To truly separate, create a new bot via @BotFather and update `TELEGRAM_BOT_TOKEN` in `.env` (line 28).

## Dead .env Variables (Leftover from OpenClaw)

Hermes Agent does **NOT** natively read these environment variables — they are OpenClaw-era artifacts:

- `LOGIC_MODEL=deepseek-chat` — inert. Hermes uses `model.default` in `config.yaml`.
- `CODING_MODEL=deepseek-coder` — inert. Hermes has no internal code to read this.
- `CODING_PROVIDER` — inert.
- `DEFAULT_MODEL` / `LLM_MODEL` — also inert if `config.yaml` sets `model.default`.

**Actual model routing in Hermes:** Uses `smart_model_routing` config in `config.yaml`. The env-var-based approach from OpenClaw does not carry over.

**Note:** `deepseek-coder` has been merged into `deepseek-chat` since early 2025.

## Service Management

- **Hermes restart:** `launchctl unload ~/Library/LaunchAgents/com.hermes.gateway.plist && launchctl load ~/Library/LaunchAgents/com.hermes.gateway.plist`
- **OpenClaw stop:** `pm2 stop openclaw-gateway`
- **WhatsApp:** Works through Hermes, not OpenClaw.

## macOS Operation Limits (discovered through live testing)

### What Hermes CAN do (as regular user)
- Run commands via `terminal()` — full shell access as current user
- Read/write files in home directory
- Open applications: `open -a Safari http://localhost:8080/...`
- Delete user-level files (rm without sudo)
- Kill processes, manage servers, read logs

### What Hermes CANNOT do (requires user at keyboard)
- `sudo` anything — macOS demands interactive TTY for password
- Simulate keyboard/mouse — `osascript keystroke` blocked (error 1002)
- Delete sandboxed containers — protected by macOS sandbox
- Modify firewall settings — requires root

### Workflow for operations needing password
1. Have user copy-paste command into Terminal manually
2. Hermes can pre-open Terminal with `open -a Terminal`
3. Hermes can copy command to clipboard with `echo "command" | pbcopy`
4. User pastes (Cmd+V), presses Enter, types password
