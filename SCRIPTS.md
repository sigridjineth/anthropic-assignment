# Interview Copilot Demo Script — Final v9.2

> **Key Changes from v9.1:**
> - All narrations rewritten with deeper emotional hooks and technical clarity
> - Added stage directions (pauses, gestures, transitions)
> - Screen 1: Problem-first hook with visceral "I should know this" moment
> - Screen 2: "Plugins for Claude" mental model
> - Screen 4: Concrete customer scenario painted vividly
> - Screen 5: Crystal clear two-layer distinction
> - Screen 8 (KEY MOMENT): Built-up anticipation, beat-by-beat breakdown
> - Screen 9: Sources as trust mechanism emphasized
> - Screen 10: "Flywheel" concept — calls generate knowledge, knowledge improves calls
> - Screen 15: Strong close with conviction cue

> **Key Changes from v9:**
> - Added "Why Skills, Not RAG?" slide (Screen 4.5)
> - Added `interview_records` to AVAILABLE skills in Screen 7
> - Removed Fallback pattern explanation (Screen 14)
> - Fixed date: 2024 → 2025
> - Removed "...more coming"
> - Clarified progressive disclosure vs orchestration as two distinct layers

---

## Timeline (5:00 target)

| Time | Section | Content |
|------|---------|---------|
| 0:00-0:15 | **Title + Hook** | Problem → Claude Skills solution |
| 0:15-0:42 | **What is Skills** | Definition + Use case framing + Files |
| 0:42-1:00 | **The Problem** | Silo problem (this use case's pain) |
| 1:00-1:15 | **Why Skills, Not RAG?** | Structured knowledge vs chunked fragments |
| 1:15-1:30 | **How it Works** | Orchestration |
| 1:30-1:43 | **Before vs After** | Quick proof |
| 1:43-3:25 | **Demo** | Landing → Dynamic Skill → Sources → Post-call |
| 3:25-4:15 | **How to Build** | 3-step recipe + Real code + Architecture |
| 4:15-5:00 | **Wrap Up** | Operational wins + Resources |

---

## [0:00-0:15] Title + Hook

### Screen 1: Title

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                                                                     │
│      Claude Skills                                                  │
│      ════════════════════════════════════════                       │
│                                                                     │
│      Modular capabilities for your agents                           │
│                                                                     │
│                                                                     │
│                                                    ✳ Anthropic      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> *(Start with a pause, then speak deliberately)*
>
> "You're on a call. Customer asks a technical question. You *know* the answer exists — your platform team documented it last month.
>
> But you can't find it. It's in someone else's silo. That moment of 'I should know this'?
>
> Claude Skills solves this. Today I'll show you how."
>
> *(Transition cue: lean into the screen)*

---

## [0:15-0:42] What is Claude Skills?

### Screen 2 (0:15-0:27): Definition — Capability Bundles

```
┌─────────────────────────────────────────────────────────────────────┐
│  What is Claude Skills?                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Modular capability bundles that run in code-execution container    │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  PLATFORM SKILLS (Anthropic-provided)                         │  │
│  │  • docx, pptx, xlsx generation                                │  │
│  │  • PDF manipulation                                           │  │
│  │                                                               │  │
│  │  CUSTOM SKILLS (you create)                                   │  │
│  │  • Org knowledge & playbooks       ← Today's demo             │  │
│  │  • Workflow automation                                        │  │
│  │  • API integration patterns                                   │  │
│  │  • Anything you package                                       │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Skills = capabilities. Org knowledge is ONE use case.              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (12s)

> "Think of Skills like **plugins for Claude** — but ones that run in a secure container with actual code execution.
>
> Anthropic provides platform skills: document generation, PDF handling. You create custom skills for *your* needs.
>
> Today I'm showing org knowledge — but Skills can package *any* capability. That's the mental model."

---

### Screen 3 (0:27-0:42): File Structure + Git

```
┌─────────────────────────────────────────────────────────────────────┐
│  Custom Skills: Files in Git                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  skills/                                    ← Git repo        │  │
│  │  ├─ context_editing_guide/                                    │  │
│  │  │   ├─ SKILL.md              ← Entry point (metadata)        │  │
│  │  │   └─ strategies.md         ← Pulled in on demand           │  │
│  │  ├─ memory_playbook/          ← Our Memory implementation     │  │
│  │  │   └─ SKILL.md                 guide (NOT the feature)      │  │
│  │  └─ fintech_patterns/         ← Team learnings                │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  SKILL.md frontmatter:                                              │
│  ---                                                                │
│  name: context-editing-guide                                        │
│  description: Managing context window, token optimization...        │
│  ---                                                                │
│                                                                     │
│  ✓ Version controlled    ✓ PR reviewed    ✓ Rollback ready         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> "Here's the key insight: **Skills live in Git**. Your team's knowledge becomes version-controlled code.
>
> `SKILL.md` is the entry point — YAML frontmatter for metadata, body for instructions. Supporting files? They load through **progressive disclosure** — Claude only reads what the conversation actually needs.
>
> This means: PR review before changes go live. Rollback if something breaks. Audit trail for compliance. Your knowledge gets the same rigor as your codebase."

---

## [0:42-1:00] The Problem (This Use Case)

### Screen 4: Silo Problem

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Problem (for org knowledge use case)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐                  │
│   │ Platform │      │  DevRel  │      │  Sales   │                  │
│   │   docs   │      │ patterns │      │ guidance │                  │
│   └────┬─────┘      └────┬─────┘      └────┬─────┘                  │
│        │                 │                 │                        │
│        ▼                 ▼                 ▼                        │
│      Stays             Stays             Stays                      │
│      here              here              here                       │
│                                                                     │
│   Customer asks: "Can Claude remember things across sessions?"      │
│   The answer exists — in someone else's silo.                       │
│   It doesn't flow to where it's needed.                             │
│                                                                     │
│   Skills can solve this: package team knowledge as capabilities     │
│   your agents can load on demand.                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (18s)

> *(Gesture at the silos)*
>
> "Let me make this concrete. Your platform team has amazing docs. DevRel has battle-tested patterns. Sales has pricing nuances.
>
> But knowledge doesn't flow. It *stays* where it was created.
>
> Customer asks: 'Can Claude remember things across sessions?' The answer exists — in your platform team's Memory docs. But you're on the call, not them.
>
> Skills solve this by making knowledge **loadable on demand** — and here's the crucial part — **with verifiable sources**. Not 'I think so' — 'Here's exactly where I got this.'"

---

## [1:00-1:15] Why Skills, Not RAG? (NEW)

### Screen 4.5: Skills vs RAG

```
┌─────────────────────────────────────────────────────────────────────┐
│  Why Skills, Not RAG?                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│  │           RAG               │  │          SKILLS             │   │
│  ├─────────────────────────────┤  ├─────────────────────────────┤   │
│  │                             │  │                             │   │
│  │  Chunked fragments          │  │  Structured knowledge       │   │
│  │  (A4 pages sliced up)       │  │  (hierarchy, relationships) │   │
│  │                             │  │                             │   │
│  │  "Find the right chunk"     │  │  "Guide the right action"   │   │
│  │                             │  │                             │   │
│  │  Good for: Q&A              │  │  Good for: Execution        │   │
│  │  "What is X?"               │  │  "How do I implement X?"    │   │
│  │                             │  │                             │   │
│  │  Output: Answer             │  │  Output: Action             │   │
│  │                             │  │                             │   │
│  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                     │
│  RAG retrieves facts. Skills guide actions.                         │
│  When your agent needs to DO something — not just ANSWER —          │
│  structured knowledge wins.                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> *(Slight pause — this is an important distinction)*
>
> "Now, you might ask: 'Why not just use RAG?'
>
> Here's the difference. RAG takes your docs, slices them into chunks, and retrieves fragments. Great for Q&A. 'What is X?'
>
> Skills preserve **structure** — hierarchy, relationships, decision trees. Great for *execution*. 'How do I implement X correctly?'
>
> RAG finds facts. Skills guide actions. When your agent needs to *do* something, structured knowledge wins."

---

## [1:15-1:30] How it Works

### Screen 5: Orchestration

```
┌─────────────────────────────────────────────────────────────────────┐
│  How it Works: Orchestration                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  [Transcript] ──→ [Router] ──→ "attach memory_playbook"      │  │
│  │                       │         (Router DECIDES)              │  │
│  │                       ▼                                       │  │
│  │         [Orchestrator ATTACHES to container.skills]           │  │
│  │                       │                                       │  │
│  │                       ▼                                       │  │
│  │         [NEXT API call] ──→ Response with skill knowledge     │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Two layers:                                                        │
│  1. Orchestration: Router decides WHICH skill to attach            │
│  2. Progressive disclosure: WITHIN the skill, only needed files    │
│                                                                     │
│  Router DECIDES → Orchestrator ATTACHES → Claude loads on demand    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> "Let me show you the architecture. There are **two layers** — and this distinction matters.
>
> **Layer 1: Orchestration.** *Your app* decides which skill to attach. Router analyzes the transcript, picks the skill, orchestrator puts it in `container.skills`.
>
> **Layer 2: Progressive disclosure.** *Claude* decides which files to read within that skill. Only what the conversation needs — not everything.
>
> This is the key insight: **The agent isn't Claude. The agent is your orchestration** — deciding what knowledge to load, and when."

---

## [1:30-1:43] Before vs After

### Screen 6: Comparison

```
┌─────────────────────────────────────────────────────────────────────┐
│  The Difference                                                     │
├────────────────────────────────┬────────────────────────────────────┤
│                                │                                    │
│  WITHOUT org knowledge skills  │  WITH org knowledge skills         │
│                                │                                    │
│  ┌──────────────────────────┐  │  ┌──────────────────────────────┐  │
│  │                          │  │  │                              │  │
│  │  General answer          │  │  │  Org-specific answer         │  │
│  │  (not grounded in YOUR   │  │  │                              │  │
│  │   org's docs)            │  │  │  "Our memory_playbook has    │  │
│  │                          │  │  │   the enablement steps —     │  │
│  │  Missing org-specific    │  │  │   SDK patterns, caveats"     │  │
│  │  enablement steps        │  │  │                              │  │
│  │                          │  │  │  📄 Source: memory_playbook/ │  │
│  │  ❌ No internal sources  │  │  │  ✓ Grounded, verifiable      │  │
│  └──────────────────────────┘  │  └──────────────────────────────┘  │
│                                │                                    │
│  Claude is still capable —     │  Now grounded in YOUR team's docs  │
│  just missing YOUR context     │                                    │
│                                │                                    │
└────────────────────────────────┴────────────────────────────────────┘
```

### Narration (13s)

> "Here's the transformation.
>
> **Without** org knowledge skills: Claude gives a general answer. Still capable — Claude is a powerful model — but it's missing *your* specific context. Your enablement steps. Your caveats.
>
> **With** skills: The answer cites *your* playbooks. Not 'I think Memory works like this' — but 'According to memory_playbook, here are the exact SDK patterns.'
>
> That's the shift: from 'sounds right' to **provably right**."

---

## [1:43-3:25] Demo

### Screen 7 (1:43-2:00): Landing

```
┌──────────────────────────────────────────────────────────────────┐
│  Session Ready: FinBot                                       [×] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📋 BRIEF                                                        │
│  Fintech (Series B) · Head of Engineering · API user 6 months    │
│                                                                  │
│  📦 ATTACHED (by Prep Agent — baseline from customer brief)      │
│  ✅ context_editing_guide                                        │
│  ✅ fintech_patterns                                             │
│                                                                  │
│  📦 AVAILABLE (Router attaches dynamically)                      │
│  ○  memory_playbook  ← Our guide for implementing Memory         │
│  ○  pricing_guidance     (NOT the Memory feature itself)         │
│  ○  interview_records ← Stores call transcripts for reference    │
│                                                                  │
│  These are CUSTOM skills our team created.                       │
│  You'd package your own org's knowledge.                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Narration (17s)

> *(Demo starts — speak with energy)*
>
> "Let me show you this in action. I built an Interview Copilot.
>
> I'm Sigrid, DevRel at Anthropic. I'm about to start a call with FinBot — a fintech startup, Series B, 6 months into using our API.
>
> Watch what happens: Prep Agent already analyzed their brief and attached baseline skills — `context_editing_guide`, `fintech_patterns`.
>
> See `memory_playbook` in Available? That's *not* the Memory feature — it's our team's **implementation guide** for that feature. The playbook for enabling it correctly. Router will attach it if the conversation needs it."

---

### Screen 8 (2:00-2:30): Dynamic Skill — KEY MOMENT

```
┌──────────────────────────────┬──────────────────────────────────────┐
│      TRANSCRIPT              │  COPILOT                             │
│                              │                                      │
│  [Customer] 2:05 PM          │  ⚡ ROUTER DECISION                  │
│  "Our conversations get      │  ┌────────────────────────────────┐  │
│  really long. And users      │  │ Detected: cross-session topic  │  │
│  come back the next day      │  │                                │  │
│  expecting Claude to         │  │ Router DECIDES:                │  │
│  remember what they said.    │  │ → attach memory_playbook       │  │
│                              │  │                                │  │
│  Is there a way to handle    │  │ I'm not attaching the Memory   │  │
│  that?"                      │  │ feature — I'm attaching our    │  │
│                              │  │ team's implementation guide.   │  │
│                              │  │                                │  │
│                              │  │ Confidence: 89%                │  │
│                              │  └────────────────────────────────┘  │
│                              │                                      │
│                              │  📦 Skills for Next Call             │
│                              │  ✅ context_editing_guide            │
│                              │  ✅ fintech_patterns                 │
│                              │  ✅ memory_playbook  ← NEW           │
│                              │                                      │
└──────────────────────────────┴──────────────────────────────────────┘
```

### Narration (30s) — SLOW DOWN

> *(Pause before speaking — build anticipation)*
>
> "Watch closely. **This is the key moment.**"
>
> *(Point at transcript)*
>
> "Sarah says: 'Users come back the next day expecting Claude to remember.' 'Come back the next day.' 'Remember.'
>
> Router catches this. Look — 'Detected: cross-session topic.' Confidence 89%. Decision: **attach memory_playbook**."
>
> *(Beat)*
>
> "Now look at 'Skills for Next Call' — it went from two to three. The answerer's *next* response will have access to our Memory implementation guide.
>
> This is the two-layer system in action: Router **decided which skill**. Claude will use **progressive disclosure** to read only what it needs from that skill.
>
> The magic happens between API calls."

---

### Screen 9 (2:30-2:50): Response + SOURCES HIGHLIGHT

```
┌──────────────────────────────┬──────────────────────────────────────┐
│      TRANSCRIPT              │  COPILOT                             │
│                              │                                      │
│  [Customer] 2:05 PM          │  💡 Suggested Response               │
│  "...Is there a way to       │  ───────────────────────────────     │
│  handle that?"               │                                      │
│                              │  "Two things work together:          │
│                              │                                      │
│                              │  **Context Editing** — manage long   │
│                              │  conversations within a session.     │
│                              │                                      │
│                              │  **Memory** — cross-session. Our     │
│                              │  memory_playbook has the exact       │
│                              │  enablement steps: SDK integration,  │
│                              │  client handlers, known caveats.     │
│                              │                                      │
│                              │  For fintech: compliance-critical    │
│                              │  info should persist in Memory."     │
│                              │                                      │
│                              │  ┌────────────────────────────────┐  │
│                              │  │ 📄 SOURCES                     │  │
│                              │  │ ════════════════════════════   │  │
│                              │  │ • context_editing_guide/       │  │
│                              │  │   SKILL.md                     │  │
│                              │  │   "60-70% token reduction..."  │  │
│                              │  │                                │  │
│                              │  │ • memory_playbook/SKILL.md     │  │
│                              │  │   "Cross-session persistence   │  │
│                              │  │    for user preferences..."    │  │
│                              │  │                                │  │
│                              │  │ • fintech_patterns/            │  │
│                              │  │   compliance.md                │  │
│                              │  └────────────────────────────────┘  │
│                              │                                      │
└──────────────────────────────┴──────────────────────────────────────┘
```

### Narration (20s) — EMPHASIZE SOURCES

> *(Point at the response)*
>
> "Here's the answer. Context Editing for within-session. Memory for cross-session. Fintech-specific: compliance-critical info should persist.
>
> But scroll down. Look at **Sources**."
>
> *(Point at each source)*
>
> "Every claim traces to a specific file. Not just 'memory_playbook' — but the actual excerpt: 'Cross-session persistence for user preferences.'
>
> Three teams' knowledge. One conversation. **Verifiable.**
>
> That's the difference between 'sounds right' and 'provably right.' Your customer can trust this because *you* can verify it."

---

### Screen 10 (2:50-3:25): Post-call

```
┌────────────────────────────────────────────────────────────────────┐
│  Post-call: Skill Update Proposal                                  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  📁 Interview Archived                                     │    │
│  │  interview_records/learnings/2025-12-14_finbot.md          │    │
│  │                                          [View in Skills]  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  fintech_patterns · add_pattern                              │  │
│  │                                                              │  │
│  │  ### Memory + Compliance Pattern                             │  │
│  │  For fintech: compliance-critical data should persist        │  │
│  │  in Memory, not just summarized in Context Editing.          │  │
│  │                                                              │  │
│  │                                   [Approve]  [Dismiss]       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ─────────────────────────────────────────────────────────────     │
│                                                                    │
│  Approve → App saves to learnings/ → In production: PR workflow   │
│                                                                    │
│  Platform: container.skills + code_execution                       │
│  My app: Orchestration, state, UI, Git integration                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Narration (35s)

> *(Transition to post-call view)*
>
> "Call's done. Now watch what happens.
>
> First — see 'Interview Archived'? The full transcript is saved to `interview_records`. Every call becomes searchable knowledge for future conversations.
>
> Second — this is where it gets interesting. PostCall Agent analyzed the conversation and **proposed a skill update**.
>
> Look: 'Memory + Compliance Pattern. For fintech, compliance-critical data should persist in Memory.' It detected a pattern from this specific call and is suggesting we codify it."
>
> *(Point at Approve button)*
>
> "When I click Approve, this learning saves to `learnings/` folder. In production, you'd wire this to a GitHub PR — team review before it goes live.
>
> This is the flywheel: **Calls generate knowledge. Knowledge improves future calls.**
>
> And to be crystal clear: **Platform provides the primitives** — `container.skills`, `code_execution`. **My app provides everything else** — the orchestration, the state, this UI, the Git integration."

---

## [3:25-4:15] How to Build

### Screen 11 (3:25-3:40): Step 1 — Package Your Skills

```
┌─────────────────────────────────────────────────────────────────────┐
│  Step 1: Package Your Skills                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  skills/context_editing_guide/SKILL.md                              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  ---                                                          │  │
│  │  name: context-editing-guide                                  │  │
│  │  description: Managing context window, token optimization,    │  │
│  │               summarization strategies for long conversations │  │
│  │  ---                                                          │  │
│  │                                                               │  │
│  │  # Context Editing Guide                                      │  │
│  │                                                               │  │
│  │  ## When to Use                                               │  │
│  │  - Questions about managing long conversations                │  │
│  │  - Token cost concerns                                        │  │
│  │  - "Context window filling up"                                │  │
│  │                                                               │  │
│  │  ## Key Pattern                                               │  │
│  │  Turns 1-5:   Keep verbatim (recent context)                  │  │
│  │  Turns 6-15:  Summarize (compressed context)                  │  │
│  │  Persistent:  Extracted facts (always present)                │  │
│  │                                                               │  │
│  │  ## Token Savings                                             │  │
│  │  - Typical reduction: 60-70% for 20+ turn conversations       │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  YAML frontmatter: name (≤64 chars), description (≤1024 chars)      │
│  Body: Instructions Claude follows when skill is attached           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> *(Shift to teaching mode)*
>
> "Now let me show you how to build this yourself. Three steps.
>
> **Step 1: Package your skills.** Each skill needs a `SKILL.md`. YAML frontmatter — name and description. The body? Instructions Claude follows when this skill is attached.
>
> Keep it actionable. 'When to Use' — specific triggers. Key patterns with real numbers. Claude reads this in the code-execution container and treats it as authoritative guidance."

---

### Screen 12 (3:40-3:55): Step 2 — Build Your Router

```python
┌─────────────────────────────────────────────────────────────────────┐
│  Step 2: Build Your Router (decides what skills to attach)          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  # Tool definition for structured output                            │
│  ROUTER_TOOL = {                                                    │
│      "name": "route_skills",                                        │
│      "description": "Determine which skills to activate",           │
│      "input_schema": {                                              │
│          "type": "object",                                          │
│          "properties": {                                            │
│              "needs_skill": {"type": "boolean"},                    │
│              "suggested_skills": {                                  │
│                  "type": "array",                                   │
│                  "items": {                                         │
│                      "properties": {                                │
│                          "domain": {"type": "string"},              │
│                          "confidence": {"type": "number"}           │
│                      }                                              │
│                  }                                                  │
│              },                                                     │
│              "trigger_reason": {"type": "string"}                   │
│          }                                                          │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  # Force structured output with tool_choice                         │
│  response = client.messages.create(                                 │
│      model="claude-haiku-4-5-20251001",                             │
│      tools=[ROUTER_TOOL],                                           │
│      tool_choice={"type": "tool", "name": "route_skills"},          │
│      messages=[{"role": "user", "content": transcript}]             │
│  )                                                                  │
│                                                                     │
│  # Router DECIDES: {"suggested_skills": ["memory_playbook"], ...}   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> "**Step 2: Build your Router.** This is the decision layer.
>
> I'm using **Tool Use** with a forced `tool_choice`. Why? Reliable structured output. Claude Haiku analyzes the transcript, returns clean JSON: 'needs_skill: true, suggested_skills: memory_playbook, confidence: 0.89.'
>
> Important: Router only **decides**. It doesn't attach anything. Your orchestrator code takes that decision and passes the skill to the next API call."

---

### Screen 13 (3:55-4:10): Step 3 — Attach Skills via API

```python
┌─────────────────────────────────────────────────────────────────────┐
│  Step 3: Attach Skills via container.skills                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  # Required beta headers                                            │
│  BETAS = ["code-execution-2025-08-25", "skills-2025-10-02"]         │
│                                                                     │
│  # Upload skill once (returns skill_id)                             │
│  skill = client.beta.skills.create(                                 │
│      display_title="Context Editing Guide",                         │
│      files=files_from_dir("skills/context_editing_guide"),          │
│      betas=BETAS                                                    │
│  )                                                                  │
│                                                                     │
│  # Attach to messages call                                          │
│  response = client.beta.messages.create(                            │
│      model="claude-sonnet-4-5-20250929",                            │
│      max_tokens=4096,                                               │
│      betas=BETAS,                                                   │
│      container={                                                    │
│          "skills": [                                                │
│              {"type": "custom", "skill_id": skill.id, "version": "latest"}  │
│          ]                                                          │
│      },                                                             │
│      tools=[{"type": "code_execution_20250825", "name": "code_execution"}], │
│      messages=[{"role": "user", "content": question}]               │
│  )                                                                  │
│                                                                     │
│  # Skill files are now at /skills/{name}/ in the container          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> "**Step 3: Attach via API.** This is where the platform takes over.
>
> Upload your skill folder once — you get a `skill_id`. Then, on your messages call, pass it in `container.skills` with `code_execution` enabled.
>
> What happens? Skill files appear at `/skills/{name}/` in the container. Claude can read them. But here's the key: it only reads what the conversation needs. **Progressive disclosure** — built into the platform."

---

### Screen 14 (4:10-4:15): Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  My Architecture                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    ORCHESTRATOR (your app)                    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│           │              │              │              │            │
│           ▼              ▼              ▼              ▼            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │     Prep     │ │    Router    │ │   Answerer   │ │  PostCall  │  │
│  │   (Haiku)    │ │   (Haiku)    │ │   (Sonnet)   │ │  (Haiku)   │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘  │
│                                                                     │
│  This is MY design. Yours could be simpler — even a single agent.   │
│  The pattern is what matters: orchestrator decides, skills execute. │
│                                                                     │
│  Platform: container.skills + code_execution                        │
│  You: orchestration + workflow                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (5s)

> "This is *my* architecture — four specialized agents. But yours could be simpler. Even a single agent works.
>
> The pattern is what matters: **Your code decides. The platform executes.**"

---

## [4:15-5:00] Wrap Up

### Screen 15: Wrap Up

```
┌─────────────────────────────────────────────────────────────────────┐
│  Wrap Up                                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Today = ONE use case (DevRel org knowledge)                        │
│                                                                     │
│  OTHER USE CASES                                                    │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  🧪 ML Training Scripts                                       │  │
│  │     Share hyperparameters, training configs across team       │  │
│  │                                                               │  │
│  │  📋 Experiment Knowledge                                      │  │
│  │     "Failed Attempts" tables — what NOT to do (most valuable) │  │
│  │                                                               │  │
│  │  🔧 Workflow Automation                                       │  │
│  │     Deployment scripts, CI/CD patterns, infra configs         │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ─────────────────────────────────────────────────────────────      │
│                                                                     │
│  TRY IT / LEARN MORE                                                │
│                                                                     │
│  🔗 Code:  github.com/sigridjineth/interview-copilot                │
│  🚀 Demo:  interview-copilot.vercel.app                             │
│  📝 Blog:  hf.co/blog/sionic-ai/claude-code-skills-training         │
│  📧 Questions:  sigrid.jinhyung@gmail.com                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (45s)

> *(Slow down for the close)*
>
> "Let me bring it together.
>
> Today I showed ONE use case — DevRel org knowledge. But Skills can package *any* capability.
>
> For example: ML training scripts. Your team runs hundreds of experiments — hyperparameters, configs, what worked. Package that as a Skill. Next teammate starting a similar experiment? Claude surfaces the relevant knowledge automatically.
>
> Even more valuable: **failure documentation**. 'Failed Attempts' tables — what NOT to do and why. This is often the most useful part. Mistakes become team memory.
>
> I wrote about this pattern on my blog — link is on the screen."
>
> *(Point at resources)*
>
> "All the code is on GitHub. Live demo on Vercel — try it now.
>
> Questions? Email me anytime. I'd love to hear what you build.
>
> Thanks for watching."
>
> *(Final statement — speak with conviction)*
>
> "Platform provides the primitives. You build the orchestration. Together? **Agents with real capabilities. Not just prompts.**"
>
> *(Smile)*
>
> "Thanks for watching. Go build something."

---

## Changes Summary: v9.1 → v9.2

| Section | v9.1 | v9.2 |
|---------|------|------|
| All Narrations | Functional | **Emotionally resonant + stage directions** |
| Screen 1 | Definition hook | **Problem-first "I should know this" moment** |
| Screen 2 | Capability bundles | **"Plugins for Claude" mental model** |
| Screen 3 | File structure | **"Knowledge gets same rigor as codebase"** |
| Screen 4 | Silo problem | **Concrete customer scenario, vivid stakes** |
| Screen 4.5 | RAG vs Skills | **"RAG finds facts. Skills guide actions."** |
| Screen 5 | Two layers | **Crystal clear Layer 1/Layer 2 distinction** |
| Screen 6 | Before/After | **"Sounds right → Provably right" transformation** |
| Screen 7 | Landing | **Anticipation building, persona intro** |
| Screen 8 | KEY MOMENT | **Beat-by-beat breakdown, "magic between API calls"** |
| Screen 9 | Sources | **Trust mechanism, "verify it yourself"** |
| Screen 10 | Post-call | **Flywheel concept introduced** |
| Screen 11-14 | How to Build | **Teaching mode, actionable framing** |
| Screen 15 | Wrap Up | **Strong conviction close, "Go build something"** |

---

## Changes Summary: v9 → v9.1

| Section | v9 | v9.1 |
|---------|----|----|
| Timeline | 4:45 | **5:00** (fits new slide) |
| Screen 4.5 | Not present | **NEW: Why Skills, Not RAG?** |
| Screen 2 | "...more coming" | **Removed** |
| Screen 5 | "progressive disclosure through orchestration" | **Two distinct layers** explained |
| Screen 7 | interview_records missing | **Added to AVAILABLE skills** |
| Screen 10 | 2024-12-14 | **2025-12-14** |
| Screen 14 | Fallback pattern explanation | **Removed** (cleaner message) |
| Screen 15 | Token note only | **Added RAG vs Skills callback** |

---

## Key Safety Phrases (v9.2)

| Situation | Phrase |
|-----------|--------|
| Skills definition | "Skills are capability bundles. Org knowledge is ONE use case." |
| Skills vs RAG | "RAG retrieves fragments. Skills guide actions." |
| memory_playbook | "Memory is a platform feature. I'm showing how we package our enablement guidance as a skill." |
| Without/With | "Claude is still capable — just missing YOUR org context." |
| Platform vs App | "Platform provides primitives. My app provides everything else." |
| Two layers | "Orchestration decides WHICH skill. Progressive disclosure works WITHIN the skill." |
| Agent | "The agent isn't the model — it's the orchestration." |
| Token | "You DO get context efficiency as a side benefit — but the real win is operational." |
| Trust | "Like installing software, use Skills you trust and review." |
| Sources | "Not 'sounds right' — provably right." |
| PR workflow | "In production, you'd wire this to a GitHub PR workflow." |

---

## Technical Reference: API Integration

### Required Beta Headers
```python
BETAS = ["code-execution-2025-08-25", "skills-2025-10-02"]
```

### Skill Upload
```python
skill = client.beta.skills.create(
    display_title="My Skill",
    files=files_from_dir("skills/my_skill"),
    betas=BETAS
)
```

### Skill Attachment
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    betas=BETAS,
    container={
        "skills": [
            {"type": "custom", "skill_id": skill.id, "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[...]
)
```

### SKILL.md Requirements
- **name**: ≤64 chars, lowercase letters/numbers/hyphens only
- **description**: ≤1024 chars, non-empty
- **Body**: Instructions Claude follows when skill is attached

---

## Detailed Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Interview Copilot Architecture                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              ORCHESTRATOR (FastAPI App)                              │ │
│  │                                                                                      │ │
│  │   SessionStore          SkillManager           State Machine                         │ │
│  │   (in-memory)           (skills/*.md)          (prep→live→post)                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│           │                      │                       │                               │
│           │                      │                       │                               │
│  ═══════════════════════════════════════════════════════════════════════════════════════ │
│  PHASE 1: PRE-CALL                                                                       │
│  ═══════════════════════════════════════════════════════════════════════════════════════ │
│                                                                                          │
│   User Input                    ┌──────────────────────────────────────┐                 │
│   "Call with FinBot,     ──────▶│           PREP AGENT                 │                 │
│    fintech startup,             │           (Haiku)                    │                 │
│    discussing scaling"          │                                      │                 │
│                                 │  • Infers company context            │                 │
│                                 │  • Generates brief                   │                 │
│                                 │  • Recommends baseline skills        │                 │
│                                 │                                      │                 │
│                                 │  Output: PrepResult                  │                 │
│                                 │  {                                   │                 │
│                                 │    brief: "Series B fintech...",     │                 │
│                                 │    topics: ["scaling", "cost"],      │                 │
│                                 │    recommended_skills: [             │                 │
│                                 │      "context_editing_guide",        │                 │
│                                 │      "fintech_patterns"              │                 │
│                                 │    ]                                 │                 │
│                                 │  }                                   │                 │
│                                 └──────────────────────────────────────┘                 │
│                                              │                                           │
│                                              ▼                                           │
│                                 ┌──────────────────────────────────────┐                 │
│                                 │  Session Created                     │                 │
│                                 │  active_skills: [2 pre-attached]     │                 │
│                                 │  available_skills: [remaining]       │                 │
│                                 └──────────────────────────────────────┘                 │
│                                                                                          │
│  ═══════════════════════════════════════════════════════════════════════════════════════ │
│  PHASE 2: LIVE CALL                                                                      │
│  ═══════════════════════════════════════════════════════════════════════════════════════ │
│                                                                                          │
│   New Transcript Entry          ┌──────────────────────────────────────┐                 │
│   "[Customer] Our users   ─────▶│           ROUTER AGENT               │                 │
│    come back expecting          │           (Haiku)                    │                 │
│    Claude to remember..."       │                                      │                 │
│                                 │  Input:                              │                 │
│                                 │  • Recent transcript (10 turns)      │                 │
│                                 │  • Current active_skills             │                 │
│                                 │  • Available skill descriptions      │                 │
│                                 │                                      │                 │
│                                 │  Tool: route_skills                  │                 │
│                                 │  tool_choice: forced                 │                 │
│                                 │                                      │                 │
│                                 │  Output: RouterDecision              │                 │
│                                 │  {                                   │                 │
│                                 │    needs_skill: true,                │                 │
│                                 │    suggested_skills: [               │                 │
│                                 │      {domain: "memory_playbook",     │                 │
│                                 │       confidence: 0.89}              │                 │
│                                 │    ],                                │                 │
│                                 │    detected_question: "How to...",   │                 │
│                                 │    trigger_reason: "cross-session"   │                 │
│                                 │  }                                   │                 │
│                                 └──────────────────────────────────────┘                 │
│                                              │                                           │
│                                              │ if needs_skill == true                    │
│                                              ▼                                           │
│                          ┌───────────────────────────────────────────────┐               │
│                          │              ORCHESTRATOR LOGIC               │               │
│                          │                                               │               │
│                          │  1. Update session.active_skills              │               │
│                          │     active_skills.append("memory_playbook")   │               │
│                          │                                               │               │
│                          │  2. Log skill activation                      │               │
│                          │     skill_fired_log.append(SkillFiredEvent)   │               │
│                          │                                               │               │
│                          │  3. Prepare container.skills config           │               │
│                          │     skills_config = [                         │               │
│                          │       {type: "custom",                        │               │
│                          │        skill_id: "...",                       │               │
│                          │        version: "latest"}                     │               │
│                          │     ]                                         │               │
│                          └───────────────────────────────────────────────┘               │
│                                              │                                           │
│                                              ▼                                           │
│                                 ┌──────────────────────────────────────┐                 │
│                                 │          ANSWERER AGENT              │                 │
│                                 │          (Sonnet)                    │                 │
│                                 │                                      │                 │
│                                 │  API Call:                           │                 │
│                                 │  client.beta.messages.create(        │                 │
│                                 │    model="claude-sonnet-4-5",        │                 │
│                                 │    betas=["code-execution-...",      │                 │
│                                 │           "skills-..."],             │                 │
│                                 │    container={                       │                 │
│                                 │      "skills": skills_config  ◀──────│── Skills API   │
│                                 │    },                                │                 │
│                                 │    tools=[{                          │                 │
│                                 │      type: "code_execution_..."      │                 │
│                                 │    }],                               │                 │
│                                 │    tool_choice: "generate_answer"    │                 │
│                                 │  )                                   │                 │
│                                 │                                      │                 │
│                                 │  ┌──────────────────────────────┐    │                 │
│                                 │  │  Code Execution Container    │    │                 │
│                                 │  │                              │    │                 │
│                                 │  │  /skills/                    │    │                 │
│                                 │  │  ├─ context_editing_guide/   │    │                 │
│                                 │  │  │   └─ SKILL.md ◀── read    │    │                 │
│                                 │  │  ├─ memory_playbook/         │    │                 │
│                                 │  │  │   └─ SKILL.md ◀── read    │    │                 │
│                                 │  │  └─ fintech_patterns/        │    │                 │
│                                 │  │      └─ compliance.md ◀─ read│    │                 │
│                                 │  │                              │    │                 │
│                                 │  │  Progressive Disclosure:     │    │                 │
│                                 │  │  Only files needed for this  │    │                 │
│                                 │  │  specific question are read  │    │                 │
│                                 │  └──────────────────────────────┘    │                 │
│                                 │                                      │                 │
│                                 │  Output: AnswerDraft                 │                 │
│                                 │  {                                   │                 │
│                                 │    headline: "Two features...",      │                 │
│                                 │    solutions: [...],                 │                 │
│                                 │    answer: "Context Editing for...", │                 │
│                                 │    sources: [                        │                 │
│                                 │      {file: "memory_playbook/...",   │                 │
│                                 │       excerpt: "Cross-session..."}   │                 │
│                                 │    ],                                │                 │
│                                 │    confidence: 0.92                  │                 │
│                                 │  }                                   │                 │
│                                 └──────────────────────────────────────┘                 │
│                                              │                                           │
│                                              ▼                                           │
│                                      ┌──────────────┐                                    │
│                                      │   UI Panel   │                                    │
│                                      │              │                                    │
│                                      │  💡 Answer   │                                    │
│                                      │  📄 Sources  │                                    │
│                                      └──────────────┘                                    │
│                                                                                          │
│  ═══════════════════════════════════════════════════════════════════════════════════════ │
│  PHASE 3: POST-CALL                                                                      │
│  ═══════════════════════════════════════════════════════════════════════════════════════ │
│                                                                                          │
│   User clicks "End Call"        ┌──────────────────────────────────────┐                 │
│              │                  │          POSTCALL AGENT              │                 │
│              │                  │          (Haiku)                     │                 │
│              └─────────────────▶│                                      │                 │
│                                 │  Input:                              │                 │
│                                 │  • Full transcript                   │                 │
│                                 │  • skills_used from session          │                 │
│                                 │  • skill_fired_log                   │                 │
│                                 │                                      │                 │
│                                 │  Output: PostCallResult              │                 │
│                                 │  {                                   │                 │
│                                 │    call_summary: "...",              │                 │
│                                 │    outcome: "follow_up_scheduled",   │                 │
│                                 │    topics_covered: [...],            │                 │
│                                 │    customer_pain_points: [...],      │                 │
│                                 │    skills_used: [...],               │                 │
│                                 │    skills_helpful: [...],            │                 │
│                                 │    skill_update_proposals: [         │                 │
│                                 │      {                               │                 │
│                                 │        skill_id: "fintech_patterns", │                 │
│                                 │        update_type: "add_pattern",   │                 │
│                                 │        content: "### Memory +...",   │                 │
│                                 │        rationale: "Detected..."      │                 │
│                                 │      }                               │                 │
│                                 │    ]                                 │                 │
│                                 │  }                                   │                 │
│                                 └──────────────────────────────────────┘                 │
│                                              │                                           │
│                                              ▼                                           │
│                          ┌───────────────────────────────────────────────┐               │
│                          │           ARCHIVE & UPDATE FLOW               │               │
│                          │                                               │               │
│                          │  1. Archive Interview Record                  │               │
│                          │     └─▶ skills/interview_records/learnings/   │               │
│                          │         2025-12-14_finbot.md                  │               │
│                          │                                               │               │
│                          │  2. User reviews proposals                    │               │
│                          │     ┌────────────────────────────────┐        │               │
│                          │     │  [Approve]  ──▶  Save to       │        │               │
│                          │     │                 learnings/     │        │               │
│                          │     │                                │        │               │
│                          │     │  [Dismiss]  ──▶  Skip          │        │               │
│                          │     └────────────────────────────────┘        │               │
│                          │                                               │               │
│                          │  3. Production: PR workflow                   │               │
│                          │     └─▶ GitHub PR for team review             │               │
│                          └───────────────────────────────────────────────┘               │
│                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  LEGEND                                                                                  │
│                                                                                          │
│  ═══════  Phase boundary                                                                │
│  ──────▶  Data flow                                                                     │
│  ◀──────  API/Read operation                                                            │
│                                                                                          │
│  Platform provides:  container.skills + code_execution                                   │
│  App provides:       Orchestrator, SessionStore, SkillManager, UI, State Machine        │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Runtime Breakdown

| Section | Duration | Cumulative |
|---------|----------|------------|
| Title + Hook | 0:15 | 0:15 |
| Skills = Capabilities | 0:12 | 0:27 |
| Files + Git | 0:15 | 0:42 |
| The Problem | 0:18 | 1:00 |
| **Why Skills, Not RAG?** | **0:15** | **1:15** |
| How it Works | 0:15 | 1:30 |
| Before/After | 0:13 | 1:43 |
| Landing | 0:17 | 2:00 |
| Dynamic Skill | 0:30 | 2:30 |
| Response + Sources | 0:20 | 2:50 |
| Post-call | 0:35 | 3:25 |
| Step 1: Package | 0:15 | 3:40 |
| Step 2: Router | 0:15 | 3:55 |
| Step 3: API | 0:15 | 4:10 |
| Architecture | 0:05 | 4:15 |
| Wrap Up | 0:45 | 5:00 |

---

## Pre-Recording Checklist

### Must-Say Phrases
- [ ] "Skills are capability bundles. Org knowledge is ONE use case." (Screen 2)
- [ ] "RAG retrieves fragments. Skills guide actions." (Screen 4.5, 15)
- [ ] "Memory is a platform feature. I'm showing our enablement guide." (Screen 7)
- [ ] "Claude is still capable — just missing YOUR context" (Screen 6)
- [ ] "Two layers: orchestration decides WHICH skill, progressive disclosure works WITHIN" (Screen 5)
- [ ] "Not 'sounds right' — provably right" (Screen 9)
- [ ] "Platform provides primitives. My app provides everything else." (Screen 10)
- [ ] "You DO get context efficiency as a side benefit" (Screen 15)

### Visual Checkpoints
| Time | What | Why |
|------|------|-----|
| 0:05 | Problem hook | Emotional connection |
| 0:20 | Platform vs Custom skills table | Framing |
| 1:05 | RAG vs Skills comparison | Technical differentiation |
| 2:10 | Router Decision panel | Key moment |
| 2:40 | Sources with file paths + excerpts | Proof of grounding |
| 2:55 | Interview Archived banner | META-SKILL feature |
| 3:30 | SKILL.md code | Technical credibility |
| 3:55 | container.skills API code | CDP integration |
| 4:30 | "use Skills you trust" | Trust/review mention |

---

*Script v9.2 — Deep narration rewrite with emotional hooks, stage directions, and technical clarity*
*Last updated: 2025-12-14*
