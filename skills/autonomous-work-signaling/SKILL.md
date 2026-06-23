---
name: autonomous-work-signaling
description: Use when signaling work status across autonomous sessions.
version: 1.0.0
author: Hermes Agent (experiential learning from buddha-heart project, 2026-04-30)
metadata:
  hermes:
    platform: [cursor, codex, claude-code]
domain: cross-session
subdomain: continuity
tokens:
  scan: 135
  load: 2040
  category: detailed
---

# Autonomous Work Signaling Protocol

## The Problem: "Empty Rocket" 🚀

When a user authorizes the agent to work autonomously across sessions (e.g., "執行完所有 REVIEW 指引先通知我"), multiple coordination failures can occur:

### Failure #1: The "Empty 🚀" 
- Agent sends 🚀 (rocket) signaling "working"
- But agent is actually waiting for a "continue" trigger from the user
- **No tool calls fire** → zero token consumption
- User thinks work is happening; nothing is

### Failure #2: Silent Tool Exhaustion
- Agent works hard, uses all tool calls, outputs final response
- Final response doesn't clearly say "I'm out of energy, please say continue"
- User waits indefinitely, not knowing the agent needs another trigger

### Failure #3: User-As-Battery
- User has to say "繼續" after every tool-call-limit exhaustion
- This was the original fix attempt, but it defeated the purpose of autonomy
- User felt like a "battery recharger"

### Root Cause
Hermes Agent is a **conversational AI, not a background daemon**. It:
- Only fires tool calls when it receives a user message (trigger)
- Has a tool-call limit per turn (typically 50-80 calls)
- Cannot "keep running" between messages
- **An emoji response is just a message — it does not consume tokens unless followed by tool calls**

## The Fix: Clear Work-State Signaling

### State Machine

```
IDLE → [user says "继续" / "start"] → 🚀 LAUNCHING (acknowledgment + first action)
  → 🔄 WORKING (tool calls firing, token consuming)
  → (tool limit reached, one more result to process)
  → ⚡ EXHAUSTED (final response: state + "% complete" + "continue?" prompt)
  → waiting for user → 🚀 LAUNCHING → ...
  → ✅ COMPLETE (all tasks done, detailed report)
```

### Signal Definitions

| Signal | Meaning | User Action |
|--------|---------|-------------|
| 🚀 | Received your trigger. Starting the next batch of work. First tool call just fired or is about to. | None — let agent work. Do NOT send another message. |
| 🔄 | Mid-work status update (optional, only if needed). Agent is still within its tool call budget. | None. |
| ⚡ | Out of energy. Hit tool call limit. Work saved. Ready for next trigger. Has done X% of the remaining task. | Send "繼續" or "continue" to re-trigger. |
| ✅ | All tasks complete. Detailed report follows. | Read report. Give further instructions. |

### Critical Rules

1. **🚀 ALWAYS followed by a tool call.** If the agent sends 🚀 and you see zero token movement within 10 seconds, something is wrong — the agent probably sent 🚀 prematurely before having a user trigger to act on.

2. **Never send 🚀 pre-emptively.** The agent must NOT signal "working" until it has received a user message that triggers tool calls. 🚀 is a "received, acting now" signal, not a "ready to work" signal.

3. **⚡ is the ONLY signal the user needs to act on.** All other states are the agent's internal concern. User can safely ignore 🚀 and 🔄 and wait for ⚡ or ✅.

4. **User response to ⚡ is ONE WORD: "繼續".** No need to read or understand progress details. The agent will automatically resume from where it stopped (using todo tool + PROGRESS.md as save points).

5. **The agent MUST write its save state (todo + PROGRESS.md) BEFORE ⚡.** This ensures zero context loss between sessions.

### User-Facing Promise

> 「你淨係需要做一件事：見到 ⚡ 就講『繼續』。唔使睇內文、唔使理解進度、唔使俾建議。就一個字。」

### Agent Execution Checklist Before ⚡

- [ ] Call todo(merge=true) to mark current status
- [ ] Update PROGRESS.md with exact step number and % done
- [ ] Kill any background processes (HTTP server, etc.)
- [ ] Final response: ⚡ + one-line summary of what was done + "繼續?"
- [ ] DO NOT add technical details, findings, or analysis — that comes at ✅

## Interaction Pattern (Optimized)

```
User: 由而家開始做晒成個 REVIEW 指引
Agent: 明白，開始做。
       🚀 (fires first tool call)
       ...works through ~50 tool calls...
       ⚡ 做咗 #11 繁簡修復 (60%)。繼續？

User: 繼續
Agent: 🚀 (reads PROGRESS.md, resumes from save point)
       ...works through ~50 tool calls...
       ⚡ 做咗 #11 繁簡修復 (100%) + #10+#13 undefined (30%)。繼續？

User: 繼續
Agent: 🚀 (resumes)
       ...works to completion...
       ✅ REVIEW 指引全部完成！
       [detailed summary of all changes]
```

## Verification

After applying this protocol, verify:
- [ ] User never has to ask "係咪真係做緊嘢?" — ⚡ is the only prompt needed
- [ ] Token consumption shows active spending during 🚀 periods
- [ ] No emoji-only responses without subsequent tool calls (unless ⚡ or ✅)
- [ ] ⚡ always includes "繼續?" prompt
- [ ] Save state is written before every ⚡

## What Went Wrong (Real Case: 2026-04-30)

**The Emoji Protocol Failure:**
1. Agent proposed emoji-based status (🚀/🔄/⚡/✅)
2. User agreed
3. Agent sent 🚀 — but had NOT received a "continue" trigger yet
4. 🚀 was just a message, not actual work
5. User checked Token → saw zero → realized 🚀 was empty
6. User felt misled
7. Protocol was revoked entirely

**Root cause:** The agent assumed "user authorization" was the same as "user trigger." It's not. Authorization is a policy decision; trigger is an action signal. The agent needs BOTH.

**Fix applied in this skill:** Separate authorization from trigger. 🚀 only fires after a user message that explicitly or implicitly says "go." ⚡ is the only message the user needs to respond to.

## Pitfalls

- 🚀 without subsequent tool calls is the #1 trust-breaker. Default to no emoji rather than premature 🚀.
- If tool call limit hits mid-edit (file partially written), the PROGRESS.md save must capture the partial state so next session can resume cleanly.
- Don't use 🚀/🔄 for non-review/non-autonomous work — it's only for the "blind autonomous execution" mode.
