# Hermes Core Skills

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/chrislamlayer1-gif/hermes-core-skills?style=for-the-badge&logo=github)](https://github.com/chrislamlayer1-gif/hermes-core-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/chrislamlayer1-gif/hermes-core-skills?style=for-the-badge&logo=github)](https://github.com/chrislamlayer1-gif/hermes-core-skills/forks)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-ready-8A2BE2?style=for-the-badge&logo=python)](https://github.com/NousResearch/hermes-agent)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-ready-8A2BE2?style=for-the-badge&logo=anthropic)](https://claude.ai)
[![Codex](https://img.shields.io/badge/OpenAI%20Codex-ready-8A2BE2?style=for-the-badge&logo=openai)](https://codex.chat)

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

### ✨ Highlight Skills

| Skill | One-liner | Problem it solves |
|-------|-----------|-------------------|
| **systematic-debugging** | No root cause, no fix | Agent randomly patches bugs, making things worse |
| **self-regulation-brake-system** | Force stop after 3 failures | Agent looping forever, burning your budget |
| **writing-plans** | Write a plan before touching code | Agent builds the wrong thing, needs redo |
| **subagent-driven-development** | Split into subagents, review after | Complex tasks overwhelm a single agent's context |
| **token-efficiency** | Every token counts | End-of-month surprise bills |
| **checkpoints-and-rewind** | Auto-backup before any change | Agent destroys a file, can't recover |

### Installation

```bash
# Hermes Agent
# Skills are auto-dispatched - copy to your skills directory:

# Claude Code
cp -r skills/* ~/.claude/skills/

# Cursor
cp -r skills/* ~/.cursor/skills/
```

### What's Inside

#### 🧠 Agent Core (13 skills)

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

#### 🤖 AI Agent Ecosystem (6 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **agent-capability-comparison-methodology** | Your agent buyer | Don't know which agent is good, marketing lies | Source code + benchmark + hands-on, three-layer verification |
| **open-source-adaptation-pattern** | Your technical due diligence | Install an OSS project, find out it doesn't fit | License + maintenance + community + actual need, four-dimension eval |
| **multi-agent-browser-text-extraction** | Your research team | JS-heavy sites, browser itself can't extract | Multiple subagents extract in parallel, merge results |
| **skill-slimming-strategy** | Your diet plan | SKILL.md too long, agent loads it and half context is gone | Keep core workflow, move details to references/ |
| **batch-skill-description-standardization** | Your admin assistant | Dozens of skills with inconsistent descriptions | Fix 100+ at once |
| **hermes-improvement-multiphase-plan** | Your CTO | Want to improve agent but don't know where to start | IDE docs → nightly release → plugin marketplace → desktop app |

#### 🔄 Cross-Session / Planning (3 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **cross-session-execution-framework** | Your project continuity | Next session agent doesn't remember what it did | File-based state persistence, recover without memory loss |
| **plan** | Your brake pedal | User says "plan it first" but agent starts coding immediately | Pure planning mode, output checklist for approval |
| **multi-role-synthesis-framework** | Your board of directors | Single-role decisions have blind spots | Multiple roles each give advice → integrated verdict |

#### 🎯 Agent Integration (3 skills)

| Skill | Role | Pain Point | Highlight |
|-------|------|-----------|-----------|
| **openclaw-hermes-arch** | Your architecture diagram | Don't understand how agent and gateway divide work | Clear responsibility docs + failover mechanism |
| **hermes-agent** | Your Hermes setup guide | New to Hermes, don't know how to set up | Complete zero-to-running guide |
| **autonomous-work-signaling** | Your team coordinator | Multiple autonomous agents don't know what each other is doing | Cross-session work status synchronization |

### License

MIT — Use freely, contribute back when you can.
