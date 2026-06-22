---
name: hermes-agent
description: Use when setting up or extending Hermes Agent.
version: 3.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Setup, Configuration, CLI, Agent, Coding-Agent, Multi-Agent, Autonomous, Orchestration]
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent Guide

Hermes Agent is an autonomous AI agent that runs via CLI, Telegram, Discord, and other platforms.

## Quick Install

```bash
pip install hermes-agent          # or
brew install hermes-agent/tap/hermes-agent
hermes --version                  # verify
```

## Key Commands

| Command | What It Does |
|---------|-------------|
| `hermes` | Start interactive session |
| `hermes --model qwen2.5:7b` | Start with specific local model |
| `hermes --listen` | Start in service mode (API) |

## Configuration

Config file: `~/.hermes/config.yaml`

```yaml
provider: ollama
model: qwen2.5:7b
skills:
  dir: ~/.hermes/skills
```

## Spawning Sub-Agents

Use `delegate_task()` to spawn isolated agents for:
- Heavy reasoning (parallel research)
- Long-running code work (keeps your context clean)
- Multi-agent workflows (up to 3 sub-agents)

See `references/advanced-setup.md` for platform setup (Telegram, Discord, CLI gateway).
