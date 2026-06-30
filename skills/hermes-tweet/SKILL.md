---
name: hermes-tweet
description: Use when Hermes Agent needs X/Twitter search, public signal research, monitoring, or approval-gated account actions through the Hermes Tweet plugin.
version: 0.1.6
author: Xquik
license: MIT
tags:
  - hermes-agent
  - xquik
  - twitter
  - social-media
  - automation
---

# Hermes Tweet

Use this skill when a coding or research agent needs current X/Twitter context
without guessing API routes or bypassing account-safety gates.

## Install

Install the native Hermes plugin:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
hermes tools list
```

Set `XQUIK_API_KEY` in the Hermes runtime environment before authenticated
reads. Keep `HERMES_TWEET_ENABLE_ACTIONS` unset unless a workflow explicitly
needs approved account actions.

## Workflow

1. Use `tweet_explore` to find the relevant endpoint.
2. Use `tweet_read` for public search, replies, profiles, trends, and monitoring context.
3. Summarize the exact account action, payload, and reason before `tweet_action`.
4. Do not guess endpoint paths or paste API keys into chat.

## Good Fits

- Research X/Twitter discussions before planning a launch or incident response.
- Inspect replies and public profiles while debugging social feedback loops.
- Monitor project, product, or maintainer mentions.
- Draft and post only after the user approves the final content and account.
