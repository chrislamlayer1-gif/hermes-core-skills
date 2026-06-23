## [SHARE] I open-sourced 25 Hermes Agent skills — here's what I learned from months of daily battles

I've been using Hermes Agent daily for coding, and I kept running into the same problems:

- Agent would `/clear` and instantly forget everything
- "Fix this bug" → agent changes code blindly → 3 new bugs
- Token burn rate was terrifying
- Context fills up → agent memory loss
- Agent pushes code without asking

So I wrote **executable workflows** (skills) that enforce the right behaviors. Not vague advice — your agent loads them and follows them like rules.

**Highlights:**

- **systematic-debugging** — No root cause, no fix. 4-stage process before touching any code.
- **self-regulation-brake-system** — Agent fails 3 times? It stops and reports back. No infinite loops.
- **writing-plans** — Forces agent to write a plan before coding. Saves so many wrong-direction builds.
- **token-efficiency** — Context compression, delegate strategies, waste pattern detection.

All 25 skills work with Hermes Agent, Claude Code, Codex, and Cursor.

**Repo:** https://github.com/chrislamlayer1-gif/hermes-core-skills

I'm releasing 6 repos total (Core → DevOps → Cocos → Desktop → Creative → Research), one every few days. This is just the first batch.

Not trying to promote anything — genuinely think this can save other devs the pain I went through. Feedback and PRs welcome!
