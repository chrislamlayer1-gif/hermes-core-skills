---
name: multi-agent-browser-text-extraction
description: Use delegate_task with multiple browser-equipped sub-agents to extract verbatim text from Chinese academic/religious websites with JavaScript-heavy tree navigation. Covers coordination patterns, site-specific navigation, error recovery, and QA verification.
  triggers:
    - browser extract
    - scrape
    - web content
    - extract page

---
# Multi-Agent Browser Text Extraction

Extract large volumes of original text from JavaScript-heavy Chinese websites (e.g. ddc.shengyen.org 法鼓全集) using parallel `delegate_task` sub-agents, each with `browser` toolset.

## When to Use

- Target site has JS-heavy tree menu navigation (not static HTML)
- Need to extract 10+ pages of verbatim text from different chapters/books
- Site has bot detection that varies by URL path
- Each extraction requires clicking through tree menus to reach specific chapters
- Content must be 100% verbatim (no paraphrasing)

## Prerequisites

- `delegate_task` tool with `browser` toolset enabled
- Target site URL (usually a single base URL with query-param navigation)
- Mapping of questions/topics to specific book chapters

## Workflow

### Phase 1: Discovery (single browser session)

1. Navigate to the base URL (e.g. `https://ddc.shengyen.org/`)
2. Explore the tree menu structure. Note:
   - Which expandable levels exist (e.g. 輯 > 冊 > 章)
   - Whether chapters are loaded via `javascript:void(null)` links (they usually are)
   - Whether the URL changes when clicking chapters (it usually doesn't — content loads via AJAX)
3. Test `browser_console` to extract content:
   ```js
   document.querySelector('[class*="content"]')?.innerText || document.body.innerText.substring(0, 5000)
   ```
4. Identify any bot detection early. If the site blocks, try different URL paths.

### Phase 2: Batch Spawn (parallel extraction)

Divide the chapters into batches of 5-9 questions each. Each batch spawns a `delegate_task` with `toolsets: ["browser"]`.

**Critical passing of context:**
- Provide the EXACT chapter names and book numbers (e.g. `05-02 正信的佛教`)
- Provide output format template
- Set `max_iterations=40-55` for 6-9 chapters
- Include site navigation instructions in the context

**Context template:**
```
HOW TO USE THE SITE:
1. Go to https://ddc.shengyen.org/
2. Click "第五輯 佛教入門類" in left sidebar to expand
3. Click the book (e.g. "05-03 學佛群疑") to expand its chapters
4. Click a chapter name from the expanded sub-menu
5. Use browser_console: document.querySelector('[class*="content"]')?.innerText || ...
6. Copy the EXACT text, verbatim

QUESTIONS TO EXTRACT:
{list of questions with book and chapter mapping}

Output format for EACH question:
## Question: {question}
**Source**: 《書名》聖嚴法師 — Chapter Name
**Original Text**:
> {exact, verbatim, can be long}
```

### Phase 3: Compile & Verify

After all sub-agents complete:
1. Compile results into a structured JS/JSON file
2. Write a verification script to check all target IDs have content
3. Verify text is non-empty and reasonably sized (200+ chars per entry)

## Pitfalls

- **Site uses `javascript:void(null)` links** — browser snapshot won't show chapter content directly. You MUST use `browser_console` with innerText extraction after clicking.
- **Tree menu gets truncated** — the snapshot may only show ~50 tree items. You may need to scroll or use `browser_vision` to find which element index to click.
- **Browser sessions are isolated** — sub-agents each get their own browser state; they don't conflict.
- **Bot detection at root URL** — `ddm.org.tw` blocks automated browsers. The mirror `ddc.shengyen.org` works without blocking.
- **Sub-agents hit iteration limits** — set `max_iterations` generously (40-55) for 6-9 chapters. If still failing, split into smaller batches.
- **Sub-agents can't access parent memory** — every context they need must be in the `context` parameter. Don't assume they know project structure.

## Verification

After compiling, run a quick check:
```js
const texts = require('./data/quiz-original-texts.js');
const targetIds = [...]; // all expected IDs
targetIds.forEach(id => {
  if (!texts[id] || texts[id].length === 0) console.error(`MISSING: ${id}`);
});
```

## Real-World Example

Extracting 21 chapters from Master Shengyan's 法鼓全集 at ddc.shengyen.org:
- 3 sub-agents in parallel, each handling 7-9 chapters
- Total time: ~8 minutes (vs ~45 minutes sequential)
- Success rate: 21/21 chapters extracted
- Key insight: search function on the site is unreliable; tree navigation is the only reliable path
- Cost: ~150 browser tool calls total across all agents
