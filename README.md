# Hermes Core Skills

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/chrislamlayer1-gif/hermes-core-skills?style=for-the-badge&logo=github)](https://github.com/chrislamlayer1-gif/hermes-core-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/chrislamlayer1-gif/hermes-core-skills?style=for-the-badge&logo=github)](https://github.com/chrislamlayer1-gif/hermes-core-skills/forks)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-ready-8A2BE2?style=for-the-badge&logo=anthropic)](https://claude.ai)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-ready-8A2BE2?style=for-the-badge&logo=openai)](https://codex.chat)
[![Cursor](https://img.shields.io/badge/Cursor-ready-8A2BE2?style=for-the-badge&logo=cursor)](https://cursor.sh)
[![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-ready-8A2BE2?style=for-the-badge&logo=python)](https://github.com/NousResearch/hermes-agent)

</div>

**Your AI coding agent keeps doing dumb things? Here's the fix.**

After months of daily battles with Hermes Agent — burning tokens, losing context, watching agents fix one bug and create three more — these skills are the hard-earned lessons. Each one is an executable workflow, not vague advice. Your agent loads it and follows it.

### You've been there:

- Agent does `/clear` and forgets everything, you have to re-explain the whole context
- Agent sees "fix this bug" and starts changing code immediately — one fix, three new bugs
- Token burns fast, $5 gone before lunch
- Context fills up and agent starts "forgetting" things you said
- Agent pushes code changes without asking you first

**This skill pack fixes all of that.**

---

<div align="center">

## 📸 Demo

*Screenshot coming soon — [watch the repo](https://github.com/chrislamlayer1-gif/hermes-core-skills) for updates*

</div>

---

## 📦 Quick Start

Drop these skills into your agent and you're done.

### Claude Code

```bash
cp -r skills/* ~/.claude/skills/
```

Claude Code auto-discovers skills in `~/.claude/skills/`. After copying, just ask:

> *"Use the systematic-debugging skill to debug this error."*
> *"Follow the writing-plans skill to plan this feature."*

Claude will load the skill instructions and follow them step by step.

### Cursor

```bash
cp -r skills/* ~/.cursor/skills/
```

Cursor's agent reads skills from `~/.cursor/skills/`. In chat or composer:

> *"Load the token-efficiency skill and apply it to my current task."*

Skills appear in agent context automatically.

### OpenAI Codex

```bash
cp -r skills/* ~/.codex/skills/
```

Codex loads skills from `~/.codex/skills/`. Reference a skill in your prompt:

> *"Follow the checkpoints-and-rewind skill before making changes."*

### Hermes Agent

Hermes auto-dispatches skills by name — no manual loading needed. Skills in `~/.hermes/skills/` are matched automatically when their name fits the task context.

### Any MCP-compatible Agent

Skills are plain Markdown files. Point your agent to the `skills/` directory and it can load them via file system tools.

> 💡 **New to AI agents?** Just copy the skills folder. Then tell your agent: *"I just installed Hermes Core Skills. Please use the systematic-debugging skill to help with this problem."* Your agent will understand.

---

## 💬 Example: How to Use These Skills

### Scenario 1: Your agent keeps making bugs worse

```
You: "Use the systematic-debugging skill on this error: TypeError: Cannot read ..."
Agent: [Loads the 4-stage workflow]
  1. Report — captures the full error context
  2. Context — reads affected files
  3. Hypothesis — identifies root cause
  4. Fix — only applies change after root cause is confirmed
Result: One fix, zero new bugs.
```

### Scenario 2: You're tired of surprise token bills

```
You: "Follow the token-efficiency skill for this task."
Agent: [Loads token-saving rules]
  - Compresses long context before proceeding
  - Delegates heavy research to sub-agents
  - Avoids wasteful pattern loops
Result: Uses 40-60% fewer tokens.
```

### Scenario 3: Complex project needs multiple features

```
You: "Run subagent-driven-development to implement the auth system."
Agent: [Splits into parallel sub-agents]
  - Sub-agent 1: Login page
  - Sub-agent 2: JWT middleware
  - Sub-agent 3: Database schema
  - Review pass: merges all, fixes conflicts
Result: Features built in parallel, completed faster.
```

---

## ✨ Highlight Skills

| Skill | One-liner | Problem it solves |
|-------|-----------|-------------------|
| **systematic-debugging** | No root cause, no fix | Agent randomly patches bugs, making things worse |
| **self-regulation-brake-system** | Force stop after 3 failures | Agent looping forever, burning your budget |
| **writing-plans** | Write a plan before touching code | Agent builds the wrong thing, needs redo |
| **subagent-driven-development** | Split into subagents, review after | Complex tasks overwhelm a single agent's context |
| **token-efficiency** | Every token counts | End-of-month surprise bills |
| **checkpoints-and-rewind** | Auto-backup before any change | Agent destroys a file, can't recover |

---

## 📋 What's Inside

### 🧠 Agent Core (13 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **self-regulation-brake-system** | Agent seatbelt | Agent crashes and keeps burning tokens when you're away | 3-fail stop, 5-min stall report, no bypass allowed |
| **systematic-debugging** | Your Sherlock Holmes | Agent randomly patches bugs, one fix creates three more | 4-stage: Report → Context → Hypothesis → Fix. Iron rule: no root cause, no fix |
| **writing-plans** | Your project manager | Agent builds in wrong direction, discovers at the end | Bite-size tasks, exact file paths, code + test per task |
| **spec-driven-development** | Your requirements doctor | Unclear requirements, builds the wrong thing | Write spec first, no coding without understanding |
| **test-driven-development** | Your quality gate | Agent says "done" but never actually tested | RED-GREEN-REFACTOR, no tests = not done |
| **subagent-driven-development** | Your team lead | Complex task doesn't fit in one agent context | Split tasks → fresh subagent each → review → merge |
| **requesting-code-review** | Your code reviewer | Agent commits bad code, you don't know | Security scan + quality gate + independent reviewer |
| **security-hardening-checklist** | Your security advisor | Agent doesn't know secure coding, leaves vulnerabilities | Input, auth, storage, third-party, item by item |
| **think-tool** | Your rational voice | Agent makes impulsive decisions without thinking first | Pros cons + trade-offs + risk analysis framework |
| **token-efficiency** | Your CFO | Token burn rate is scary, don't know how to save | Context compression, delegate strategy, waste pattern avoidance |
| **checkpoints-and-rewind** | Your undo button | Agent corrupts a file, can't roll back | Auto-backup, snapshot, rollback before any change |
| **context-aware-task-decomposition** | Your context doctor | Context full, agent starts forgetting | Auto-decompose tasks, never hit context limit |
| **context-compaction-verification-and-recovery** | Your memory detective | After compaction, agent doesn't remember what it did | Verify tool commands actually executed |

### 🤖 AI Agent Ecosystem (6 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **agent-capability-comparison-methodology** | Your agent buyer | Don't know which agent is good, marketing lies | Source code + benchmark + hands-on, three-layer verification |
| **open-source-adaptation-pattern** | Your technical due diligence | Install an OSS project, find out it doesn't fit | License + maintenance + community + actual need, four-dimension eval |
| **multi-agent-browser-text-extraction** | Your research team | JS-heavy sites, browser itself can't extract | Multiple subagents extract in parallel, merge results |
| **skill-slimming-strategy** | Your diet plan | SKILL.md too long, agent loads it and half context is gone | Keep core workflow, move details to references/ |
| **batch-skill-description-standardization** | Your admin assistant | Dozens of skills with inconsistent descriptions | Fix 100+ at once |
| **hermes-improvement-multiphase-plan** | Your CTO | Want to improve agent but don't know where to start | IDE docs → nightly release → plugin marketplace → desktop app |

### 🔄 Cross-Session / Planning (3 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **cross-session-execution-framework** | Your project continuity | Next session agent doesn't remember what it did | File-based state persistence, recover without memory loss |
| **plan** | Your brake pedal | User says "plan it first" but agent starts coding immediately | Pure planning mode, output checklist for approval |
| **multi-role-synthesis-framework** | Your board of directors | Single-role decisions have blind spots | Multiple roles each give advice → integrated verdict |

### 🎯 Agent Integration (3 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **openclaw-hermes-arch** | Your architecture diagram | Don't understand how agent and gateway divide work | Clear responsibility docs + failover mechanism |
| **hermes-agent** | Your Hermes setup guide | New to Hermes, don't know how to set up | Complete zero-to-running guide |
| **autonomous-work-signaling** | Your team coordinator | Multiple autonomous agents don't know what each other is doing | Cross-session work status synchronization |

---

## 🆚 How This Compares

| Feature | Hermes Core Skills | LangChain Agents | Manual Prompting |
|---------|-------------------|------------------|-------------------|
| Drop-in ready | ✅ Copy and use | ❌ Requires code integration | ❌ Write prompts yourself |
| Executable workflows | ✅ Agent follows step by step | ❌ Just a framework | ❌ No structure |
| Cross-platform | ✅ Claude / Codex / Cursor / Hermes | ❌ Python only | ✅ Any agent |
| Token-aware | ✅ Built-in efficiency rules | ❌ No token optimization | ❌ No token optimization |
| Self-regulation | ✅ Brake system, stall detection | ❌ Not available | ❌ Not available |
| Open source | ✅ MIT | ✅ MIT | ✅ Free |

Hermes Core Skills is not a framework you integrate — it's a **workflow layer** your agent loads. It works alongside any agent and any framework.

---

## 🌐 Translations

Help translate this README! Click a badge to contribute:

[![中文](https://img.shields.io/badge/中文-翻译-8A2BE2?style=for-the-badge)](https://github.com/chrislamlayer1-gif/hermes-core-skills/discussions)
[![日本語](https://img.shields.io/badge/日本語-翻訳-8A2BE2?style=for-the-badge)](https://github.com/chrislamlayer1-gif/hermes-core-skills/discussions)
[![한국어](https://img.shields.io/badge/한국어-번역-8A2BE2?style=for-the-badge)](https://github.com/chrislamlayer1-gif/hermes-core-skills/discussions)
[![Español](https://img.shields.io/badge/Español-traducción-8A2BE2?style=for-the-badge)](https://github.com/chrislamlayer1-gif/hermes-core-skills/discussions)

> Currently English only. Translations welcome — submit a discussion or PR!

---

## 🧑‍🎓 For Beginners

**New to AI coding agents? Here's everything you need to know.**

1. **What is an AI coding agent?** A tool like Claude Code or Cursor that can write, edit, and debug code for you in your terminal or editor.

2. **What's a "skill"?** A skill is a Markdown file that teaches your agent *how* to do something properly — like a recipe for your AI chef.

3. **How do I use these skills?**
   - Install with one command (`cp -r skills/* ~/.claude/skills/`)
   - Tell your agent: *"Use the [skill name] skill"*
   - Your agent follows the instructions automatically

4. **Which skill should I start with?**
   - **First**: `systematic-debugging` — the most useful for daily coding
   - **Second**: `token-efficiency` — saves you money immediately
   - **Third**: `checkpoints-and-rewind` — safety net, never lose work

Still confused? [Open a discussion](https://github.com/chrislamlayer1-gif/hermes-core-skills/discussions) — we'll help you get started.

---

## 🏆 Use Cases

| Who | Problem | Skill Pack Solution |
|-----|---------|-------------------|
| **Solo developer** | Agent burns tokens, context gets lost | `token-efficiency` + `context-aware-task-decomposition` |
| **Startup CTO** | Junior devs using AI produce inconsistent code | `requesting-code-review` + `spec-driven-development` |
| **Open source maintainer** | Need help but can't trust AI with security | `security-hardening-checklist` + `systematic-debugging` |
| **Agency owner** | Multiple agents running, no coordination | `autonomous-work-signaling` + `cross-session-execution-framework` |
| **AI researcher** | Evaluating which agent to use for a project | `agent-capability-comparison-methodology` + `open-source-adaptation-pattern` |

---

## 🤝 How to Contribute

We'd love your help! Here's how to get started:

**Good first issues (no coding needed):**
- 📝 **Review a skill** — Try one and open an issue with your feedback
- 🌐 **Translate README** — Pick your language and submit a translation
- 🐛 **Report a bug** — If a skill doesn't work with your agent, let us know
- ✨ **Suggest new skills** — Open a discussion with your pain point

**Code contributions:**
1. Browse [open issues](https://github.com/chrislamlayer1-gif/hermes-core-skills/issues) — look for `good first issue` labels
2. Fork the repo and create a feature branch
3. Make your changes and submit a PR
4. Your PR will be reviewed within 48 hours

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md). See the [Contributing Guide](CONTRIBUTING.md) for details.

---

## 🛡️ Security

Found a security vulnerability? Please review our [Security Policy](SECURITY.md) for responsible disclosure.

---

## 📄 License

MIT — Use freely, contribute back when you can.
