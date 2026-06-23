# Hermes Core Skills Demo
# Run: vhs screenshots/demo.tape
# Requires: brew install vhs (includes ttyd)
# Then open demo.gif

Output "screenshots/demo.gif"

Set Shell "zsh"
Set FontSize 14
Set Width 800
Set Height 500
Set TypingSpeed 30ms

Type "# Hermes Core Skills — Quick Demo"
Sleep 500ms
Enter
Sleep 300ms

Type "ls skills/ | head -10"
Sleep 300ms
Enter
Sleep 1500ms

Type ""
Sleep 200ms
Enter
Type "# Install for Claude Code:"
Sleep 300ms
Enter
Type "cp -r skills/* ~/.claude/skills/"
Sleep 400ms
Enter
Sleep 1000ms

Type ""
Sleep 200ms
Enter
Type "# Verify installation:"
Sleep 300ms
Enter
Type "ls ~/.claude/skills/ | wc -l"
Sleep 400ms
Enter
Sleep 1000ms

Type ""
Sleep 200ms
Enter
Type "# ✅ 25 skills ready. Zero config. MIT licensed."
Sleep 500ms
Enter
Sleep 1000ms
