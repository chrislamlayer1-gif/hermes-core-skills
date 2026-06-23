---
name: spec-driven-development
description: Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.
version: 1.0.0
author: Hermes Agent (adapted from addyosani/agent-skills)
license: MIT
metadata:
  hermes:
    tags: [spec, planning, workflow, design, specification]
    platform: [cursor, codex, claude-code]
    related_skills: [writing-plans, planning-and-task-breakdown, subagent-driven-development]
  triggers:
    - spec
    - requirement
    - design doc
    - architecture
    - define
    - build from scratch
    - 新功能

domain: agent-core
subdomain: planning
tokens:
  scan: 315
  load: 2910
  category: detailed
---

# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec is the shared source of truth between you and Chris — it defines what we're building, why, and how we'll know it's done. Code without a spec is guessing.

## When to Use

- Starting a new project or feature
- Requirements are ambiguous or incomplete (e.g. "make it better", "add more features")
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 15 minutes to implement

**When NOT to use:** Single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained.

## The Gated Workflow

Spec-driven development has four phases. Do not advance to the next phase until the current one is validated.

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Chris      Chris    Chris      Chris
 reviews    reviews  reviews    reviews
```

### Phase 1: Specify

Start with a high-level vision. Ask Chris clarifying questions until requirements are concrete.

**Surface assumptions immediately.** Before writing any spec content, list what you're assuming:

```
ASSUMPTIONS I'M MAKING:
1. This is a WeChat Mini Program (not a web app)
2. Data is stored locally (not on a server)
3. We use Cocos Creator 3.x for the game engine
4. Target users are Chinese-speaking Buddhists, including elderly
→ Correct me now or I'll proceed with these.
```

**Write a spec document covering these six core areas:**

1. **Objective** — What are we building and why? Who is the user? What does success look like?

2. **Commands** — Full executable commands with flags, not just tool names.
   ```
   Build: npm run build
   Test: npx jest --passWithNoTests
   Verify: npm run compile
   ```

3. **Project Structure** — Where source code lives, where tests go, where docs belong.
   ```
   assets/        → Game assets (images, audio, fonts)
   src/           → Application source code
   src/scenes/    → Cocos Creator scenes
   src/scripts/   → TypeScript game scripts
   ```

4. **Code Style** — One real code snippet showing your style beats three paragraphs describing it.

5. **Testing Strategy** — What framework, where tests live, coverage expectations.

6. **Boundaries** — Three-tier system:
   - **Always do:** Run compile checks before commits, follow naming conventions, validate inputs
   - **Ask first:** Database schema changes, adding dependencies, changing build config
   - **Never do:** Commit secrets, delete source files without approval, commit broken code

**Spec template:**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs Chris's input]
```

**Reframe instructions as success criteria.** When receiving vague requirements, translate them into concrete conditions:

```
REQUIREMENT: "Make the story choices feel more meaningful"

REFRAMED SUCCESS CRITERIA:
- Each choice in a chapter leads to measurably different next-screen content
- At least 30% of choices have a consequence that appears 2+ chapters later
- Player can visibly see their choice's impact (text changes, UI feedback)
→ Are these the right targets?
```

### Phase 2: Plan

With the validated spec, generate a technical implementation plan:

1. Identify the major components and their dependencies
2. Determine the implementation order (what must be built first)
3. Note risks and mitigation strategies
4. Identify what can be built in parallel vs. what must be sequential
5. Define verification checkpoints between phases

The plan should be reviewable: Chris should be able to read it and say "yes, that's the right approach" or "no, change X."

### Phase 3: Tasks

Break the plan into discrete, implementable tasks:

- Each task should be completable in a single focused session
- Each task has explicit acceptance criteria
- Each task includes a verification step (test, build, manual check)
- Tasks are ordered by dependency, not by perceived importance
- No task should require changing more than ~5 files

**Task template:**
```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```

### Phase 4: Implement

Follow the task list in order. Use the `subagent-driven-development` skill for parallel work.

- One task at a time
- Verify after each task before moving to the next
- Commit after each task
- If something unexpected blocks a task, stop and revise the plan (don't hack around it)

## Pitfalls

- **Skipping Phase 1** — "I already know what to build" is the most common source of rework. Write the spec anyway.
- **Vague success criteria** — "Works well" is not a testable condition. Every criterion must be falsifiable.
- **Over-specifying** — Don't write implementation details in the spec. The spec is WHAT and WHY, not HOW.
- **Not surfacing assumptions** — Silent assumptions cause the most expensive bugs. List them explicitly.
- **Skipping Chris review** — Each phase gate requires Chris's approval. Don't proceed without it.

## Verification

After implementation:
1. Run all tests/compile checks
2. Verify against the spec's success criteria
3. If anything differs from the spec, decide: fix code or update spec?
