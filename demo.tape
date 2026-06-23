# Hermes Core Skills Demo
# Shows how to use a skill with Claude Code

Output "demo.gif"

# Set a nice terminal theme
Set Shell "zsh"
Set FontSize 16
Set Width 800
Set Height 400
Set TypingSpeed 40ms

# Title
Type "🐚 Hermes Core Skills — Quick Demo"
Sleep 500ms
Enter

# Step 1: Show what skills look like
Type "# Let's see what's inside the skills pack"
Sleep 300ms
Enter
Sleep 200ms

Type "ls -la skills/"
Sleep 400ms
Enter
Sleep 1s

# Step 2: Show a specific skill
Type ""
Sleep 300ms
Enter
Type "# Each skill is a ready-to-use workflow"
Sleep 300ms
Enter
Sleep 200ms

Type "head -30 skills/systematic-debugging/SKILL.md"
Sleep 400ms
Enter
Sleep 2s

# Step 3: Install for Claude Code
Type ""
Sleep 300ms
Enter
Type "# Install for Claude Code:"
Sleep 300ms
Enter
Type "cp -r skills/* ~/.claude/skills/"
Sleep 400ms
Enter
Sleep 1s

# Step 4: Verify
Type ""
Sleep 300ms
Enter
Type "# Verify installation:"
Sleep 300ms
Enter
Type "ls ~/.claude/skills/ | head -6"
Sleep 400ms
Enter
Sleep 1.5s

# Step 5: Show README header
Type ""
Sleep 300ms
Enter
Type "# Done. Your agent now has 25 executable workflows."
Sleep 300ms
Enter
Type "cat README.md | head -20"
Sleep 400ms
Enter
Sleep 2s

# End
Type ""
Sleep 300ms
Enter
Type "✅ Skills ready. Zero config. MIT licensed."
Sleep 500ms
Enter
Sleep 1s
