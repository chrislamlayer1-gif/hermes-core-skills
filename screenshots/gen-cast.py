#!/usr/bin/env python3
"""
Generate a synthetic asciicast v2 file for svg-term demo.
This creates a realistic terminal recording of installing hermes-core-skills.
"""
import json
import time
import math

header = {
    "version": 2,
    "width": 80,
    "height": 24,
    "timestamp": int(time.time()),
    "title": "Hermes Core Skills — Quick Install Demo",
    "env": {
        "SHELL": "/bin/bash",
        "TERM": "xterm-256color",
        "USER": "dev"
    }
}

# Generate frames that look like a real terminal session
frames = []

t = 0.0  # time in seconds

# Helper: append a line of text with delay
def line(text, delay=0.02):
    global t
    for ch in text:
        t += delay
        frames.append([t, "o", ch])
    t += 0.05
    frames.append([t, "o", "\r\n"])

def cmd_prompt(cmd="~ $ ", delay=0.2):
    global t
    t += delay
    for ch in cmd:
        t += 0.01
        frames.append([t, "o", ch])

def cmd_typing(text, speed=0.04):
    global t
    for ch in text:
        t += speed
        frames.append([t, "o", ch])

def output(text, delay=0.3):
    global t
    t += delay
    for ch in text:
        t += 0.002
        frames.append([t, "o", ch])
    frames.append([t, "o", "\r\n"])

# === The Demo ===

# Title screen
t += 0.5
output("\033[1;36m╔══════════════════════════════════════════════════════════╗\033[0m", 0.02)
output("\033[1;36m║     \033[1;33mHermes Core Skills\033[0m \033[1;36m— 25 AI Agent Skills               ║\033[0m", 0.01)
output("\033[1;36m║     \033[0mQuick Install Demo (1 minute)                    \033[1;36m║\033[0m", 0.01)
output("\033[1;36m╚══════════════════════════════════════════════════════════╝\033[0m", 0.02)

t += 0.8

# Step 1
output("")
output("\033[1;32mStep 1:\033[0m Clone the repository")
cmd_prompt("~ $ ")
cmd_typing("git clone https://github.com/chrislamlayer1-gif/hermes-core-skills.git", 0.03)
frames.append([t, "o", "\r\n"])
t += 0.3
output("Cloning into 'hermes-core-skills'...")
t += 0.8
output("remote: Enumerating objects: 42, done.")
t += 0.1
output("remote: Counting objects: 100% (42/42), done.")
t += 0.1
output("remote: Compressing objects: 100% (38/38), done.")
t += 0.3
output("remote: Total 42 (delta 8), reused 24 (delta 3), pack-reused 0")
t += 0.2
output("Receiving objects: 100% (42/42), done.")
t += 0.1
output("Resolving deltas: 100% (8/8), done.")

t += 0.5

# Step 2
output("")
output("\033[1;32mStep 2:\033[0m Change directory")
cmd_prompt("~ $ ")
cmd_typing("cd hermes-core-skills", 0.03)
frames.append([t, "o", "\r\n"])
t += 0.3

output("")
output("\033[1;32mStep 3:\033[0m Install all 25 skills at once")
output("\033[90m# Copy skills to your agent's skills directory\033[0m")
cmd_prompt("~/hermes-core-skills $ ")
cmd_typing("ls skills/", 0.03)
frames.append([t, "o", "\r\n"])
t += 0.4

# List skills output
skills_list = [
    "agent-capability-comparison-methodology",
    "batch-skill-description-standardization",
    "checkpoints-and-rewind",
    "context-aware-task-decomposition",
    "context-compaction-verification-and-recovery",
    "cross-session-execution-framework",
    "github-code-review",
    "github-pr-workflow",
    "github-repo-management",
    "hermes-agent",
    "hermes-improvement-multiphase-plan",
    "multi-agent-browser-text-extraction",
    "multi-role-synthesis-framework",
    "open-source-adaptation-pattern",
    "openclaw-hermes-arch",
    "requesting-code-review",
    "security-hardening-checklist",
    "self-regulation-brake-system",
    "skill-slimming-strategy",
    "spec-driven-development",
    "subagent-driven-development",
    "systematic-debugging",
    "test-driven-development",
    "think-tool",
    "token-efficiency",
    "writing-plans"
]

# Show first 10
for i, s in enumerate(skills_list[:12]):
    t += 0.01
    frames.append([t, "o", f"  {s}\033[0m\r\n"])
    t += 0.03

# Show "..." for the rest
t += 0.2
frames.append([t, "o", "\033[90m  ... and 13 more\033[0m\r\n"])

t += 0.5
output("")
cmd_prompt("~/hermes-core-skills $ ")
cmd_typing("cp -r skills/* ~/.claude/skills/", 0.03)
frames.append([t, "o", "\r\n"])
t += 0.6

output("")
output("\033[1;32mStep 4:\033[0m Verify installation")
cmd_prompt("~/hermes-core-skills $ ")
cmd_typing("ls ~/.claude/skills/ | wc -l", 0.03)
frames.append([t, "o", "\r\n"])
t += 0.4

t += 0.1
frames.append([t, "o", "      25\r\n"])

t += 0.5
output("")
output("\033[1;32m✓ 25 skills installed and ready to use!\033[0m")

t += 0.5
output("")
output("\033[1;33mExplore skills by category:\033[0m")
output("  \033[36mSystematic Debugging\033[0m    → skills/systematic-debugging/SKILL.md")
output("  \033[36mTest-Driven Development\033[0m  → skills/test-driven-development/SKILL.md")
output("  \033[36mCode Review\033[0m              → skills/requesting-code-review/SKILL.md")
output("  \033[36mSecurity Hardening\033[0m       → skills/security-hardening-checklist/SKILL.md")

t += 1.0
output("")
output("\033[90m──────────────────────────────────────────────────────────\033[0m")
output("\033[1;35mNeed help? Open an issue → github.com/chrislamlayer1-gif/hermes-core-skills\033[0m")
output("\033[1;35mStar the repo if you find it useful! ⭐\033[0m")

# Write the asciicast file
with open("/Users/openclawworker/hermes-core-skills-demo/screenshots/demo.cast", "w") as f:
    f.write(json.dumps(header) + "\n")
    for frame in frames:
        f.write(json.dumps(frame) + "\n")

print(f"Generated {len(frames)} frames over {t:.1f} seconds")
print("Output: screenshots/demo.cast")
