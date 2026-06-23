#!/bin/bash
# Generate asciicast file for svg-term demo
# This creates a synthetic but realistic terminal recording

COMMANDS=(
  "# 🚀 Hermes Core Skills — 30-Second Quick Start"
  ""
  "# Step 1: Clone the repo"
  "git clone https://github.com/chrislamlayer1-gif/hermes-core-skills.git"
  ""
  "# Step 2: Install all 25 skills at once"
  "# Just copy them to your Claude Code / Hermes skills directory"
  "cp -r skills/* ~/.claude/skills/"
  ""
  "# Step 3: Verify installation"
  "ls ~/.claude/skills/ | head -15"
  ""
  "# That's it! Check your skills inventory:"
  "ls ~/.claude/skills/ | wc -l"
  "# → 25 skills ready to use"
  ""
  "# Explore specific skills:"
  "cat skills/systematic-debugging/SKILL.md | head -20"
)

for cmd in "${COMMANDS[@]}"; do
  echo "$cmd"
  sleep 0.5
done

sleep 1
echo ""
echo "# 🎯 Demo complete — happy coding!"
