# Interview Copilot Demo Script — Final v9.8

> **Key Changes from v9.7:**
> - **Demo Section 개편**: 실제 UI 스크린샷 기반으로 재작성
> - **Screen 7 (Landing)**: 유지 — Session Ready 모달
> - **Screen 8**: Router Decision Box + Skills for Next Call (실제 UI 반영)
> - **Screen 9**: Suggested Response + Sources 패널 (실제 UI 반영)
> - **Screen 10**: Post-call Summary 상세화 (Call Summary, Pain Points, Proposals)
> - **Screen 11**: Knowledge Base 페이지 추가 (flywheel 완성)
> - **Customer name**: FinBot (Series B fintech, 50K+ users) 통일

> **Key Changes from v9.6:**
> - **PDF 순서 정렬**: RAG vs Skills를 Before/After 뒤로 이동 (Screen 6.5)
> - **Live Demo 전환 슬라이드** 추가 (Screen 6.6)
> - **RAG vs Skills 나레이션 강화**:
>   - "Naive RAG" 표현 사용 (PDF 슬라이드 7 반영)
>   - "Consistent & **Accumulative**" — 지식 축적 강조
>   - "**Evolvable**" — 진화 가능성 추가
>   - 하단 메시지: "consistent execution > finding the chunk"
> - Timeline 재정렬: Problem → How it Works → Before/After → Why Skills? → Live Demo

> **Key Changes from v9.5:**
> - **Core Message Sharpened**: "Single Point of Truth" + "Lazy-loading team knowledge" as central theme
> - Screen 2: "lazy-loaded into the agent only when needed" added
> - Screen 3: "progressive disclosure = lazy-loading team knowledge" connection explicit
> - Screen 8: "Without Skills, I'd Slack mid-call" — silo breaking
> - Screen 9: "Single point of truth" explicitly stated
> - Screen 10: "This is how silos stay broken" — flywheel connection
> - Step 3: BETAS simplified to 2 (skills + code-execution)

> **Key Changes from v9.4:**
> - **Screen 14 (Architecture)**: Expanded from 5s to 15s with detailed 3-phase walkthrough
> - ASCII diagram updated to match visual (Pre-call → Live call → Post-call flows)
> - Narration explains each agent's role: Prep (Haiku), Router (Haiku), Answerer (Sonnet), Postmortem (Haiku)
> - Total runtime: 5:00 → 5:10

> **Key Changes from v9.3:**
> - **Persona Anchor**: "Technical Leaders" (staff engineers, EMs, platform teams) — not "Managers" label
> - Screen 1 Title: "Make team knowledge flow" (goal-oriented subtitle)
> - Screen 1 Hook: Added audience clarification — "If you're a staff engineer, an engineering manager..."
> - Screen 4: Added EM-relevant metrics — "interrupt cost, consistency, auditability"
> - Maintains "technical audience" requirement while adding persona sharpness

> **Key Changes from v9.2:**
> - **Risk 1 Fixed**: Screen 4.5 reframed — RAG vs Skills "운영/일관성 관점"
> - **Risk 2 Fixed**: "provably right" → "verifiable" / "auditable"
> - **Risk 3 Fixed**: Beta headers 3개 (`files-api-2025-04-14` 추가)

> **Key Changes from v9.1:**
> - All narrations rewritten with deeper emotional hooks and stage directions
> - Screen 8 (KEY MOMENT): Built-up anticipation, beat-by-beat breakdown
> - Screen 10: "Flywheel" concept — calls generate knowledge, knowledge improves calls

> **Key Changes from v9:**
> - Added "Why Skills, Not RAG?" slide (Screen 4.5)
> - Added `interview_records` to AVAILABLE skills in Screen 7

---

## Timeline (5:25 target) — 실제 UI 기반

| Time | Section | Content |
|------|---------|---------|
| 0:00-0:15 | **Title + Hook** | Problem → Claude Skills solution |
| 0:15-0:42 | **What is Skills** | Definition + Use case framing + Files |
| 0:42-1:00 | **The Problem** | Silo problem (this use case's pain) |
| 1:00-1:15 | **How it Works** | Orchestration (Progressive Disclosure) |
| 1:15-1:28 | **Before vs After** | Quick proof |
| 1:28-1:43 | **Why Skills, Not RAG?** | Execution > Retrieval (Accumulative, Evolvable) |
| 1:43-1:45 | **Live Demo** | Transition slide |
| 1:45-3:40 | **Demo** | Landing → Router Decision → Sources → Post-call → Knowledge Base |
| 3:40-4:40 | **How to Build** | 3-step recipe + Real code + Architecture |
| 4:40-5:25 | **Wrap Up** | Operational wins + Resources |

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
│      Make team knowledge flow                                       │
│                                                                     │
│                                                                     │
│                                                    ✳ Anthropic      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> *(Start with a pause, then speak deliberately)*
>
> "If you're a staff engineer, an engineering manager, or anyone building on a platform team — this is for you.
>
> You're on a call. Customer asks a technical question. You *know* the answer exists — your platform team documented it last month.
>
> But you can't find it. It's in someone else's silo.
>
> The problem isn't lack of knowledge — it's that **knowledge doesn't flow**.
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
> Anthropic provides platform skills for document generation. You create custom skills for *your* needs.
>
> Today I'm using Skills as a **single source of truth**: our team's playbooks, shipped like code, **lazy-loaded into the agent only when the conversation needs them**."

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
> `SKILL.md` is the entry point — YAML frontmatter for metadata, body for instructions. Supporting files? They load through **progressive disclosure** — basically **lazy-loading team knowledge**. We don't dump the whole org wiki into the prompt. We load the right playbook at the moment it becomes relevant.
>
> PR review before changes go live. Rollback if something breaks. Audit trail for compliance. Your knowledge gets the same rigor as your codebase."

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
> For technical leaders, this is expensive: **interrupt cost goes up, consistency goes down, auditability is zero**.
>
> Skills solve this by making knowledge **loadable on demand** — with verifiable sources. Not 'I think so' — 'Here's exactly where I got this.'"

---

## [1:00-1:15] How it Works

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

## [1:15-1:28] Before vs After

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
> That's the shift: from 'sounds right' to **verifiable**."

---

## [1:28-1:43] Why Skills, Not Naive RAG?

### Screen 6.5: Skills vs RAG (PDF 슬라이드 7)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Solution: Why Skills, Not Naive RAG?                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│  │        Naive RAG            │  │       Claude Skills         │   │
│  ├─────────────────────────────┤  ├─────────────────────────────┤   │
│  │                             │  │                             │   │
│  │  Great for: Retrieval 🔍    │  │  Great for: Execution 👩‍💻    │   │
│  │  • Broad search             │  │  • Org-approved playbooks   │   │
│  │  • Latest content           │  │  • Reviewed & versioned     │   │
│  │  • Flexible queries         │  │  • Consistent & Accumulative│   │
│  │                             │  │                             │   │
│  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  For Sales & DevRel: "consistent execution" > "finding chunk" │  │
│  │  Skills = org-approved, auditable, consistently applied       │  │
│  │  & evolvable                                                  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> *(Slight pause — this is an important distinction)*
>
> "Now you might wonder — why not just use RAG?
>
> Here's how I think about it. **Naive RAG is great for retrieval** — broad search, latest content, flexible queries. Good for 'What is X?'
>
> **Skills are great for execution** — org-approved playbooks, reviewed and versioned, **consistent and accumulative**. Good for 'How should we do X?'
>
> For Sales and DevRel enablement, **consistent execution** matters more than finding the right chunk.
>
> And Skills are **evolvable** — every call can improve the next one. That's the flywheel I'll show you."

---

## [1:43-1:45] Live Demo Transition

### Screen 6.6: Live Demo

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                                                                     │
│                                                                     │
│                         Live Demo ✳                                 │
│                                                                     │
│                                                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (2s)

> *(Brief pause, then transition)*
>
> "Let me show you."

---

## [1:45-3:40] Demo

### Screen 7 (1:45-2:02): Landing — Session Ready

```
┌──────────────────────────────────────────────────────────────────┐
│  Session Ready                                               [×] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BRIEF                                                           │
│  FinBot (Series B fintech) is scaling an AI financial advisor    │
│  chatbot with 50K+ retail users. Their core challenge: 20-50     │
│  turn conversations are exploding token costs and losing         │
│  context (user preferences, investment constraints), creating    │
│  both UX and compliance risks.                                   │
│                                                                  │
│  LIKELY TOPICS                                                   │
│  ┌─────────────────────────────────────────────────────┐  95%   │
│  │ Context window management & token optimization...   │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐  92%   │
│  │ Cross-conversation memory & persistent user state   │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
│  📦 ATTACHED (BY PREP AGENT — BASELINE FROM CUSTOMER BRIEF)      │
│  ✅ cdp context editing                                          │
│  ✅ cdp memory                                                   │
│                                                                  │
│  📦 AVAILABLE (ROUTER ATTACHES DYNAMICALLY)                      │
│  ○  pricing guidance                                             │
│  ○  fintech patterns                                             │
│                                                                  │
│  These are CUSTOM skills our team created.                       │
│  You'd package your own org's knowledge.                         │
│                                                                  │
│                                    [Back]  [Enter Session]       │
└──────────────────────────────────────────────────────────────────┘
```

### Narration (17s)

> *(Demo starts — speak with energy)*
>
> "Let me show you this in action. I built an Interview Copilot.
>
> I'm Sigrid, DevRel at Anthropic. I'm about to start a call with FinBot — a Series B fintech with 50K+ users.
>
> Watch what happens: Prep Agent already analyzed their brief and attached baseline skills — `cdp context editing`, `cdp memory`.
>
> These are our team's playbooks — not the features themselves, but our **implementation guides** for those features. The remaining skills stay available for Router to attach dynamically if the conversation needs them."

---

### Screen 8 (2:02-2:22): Live Call — Router Decision (KEY MOMENT)

**실제 UI 요소:**
- Live Transcript (왼쪽) — [C] Customer, [S] Sigrid
- LIVE SUMMARY
- ⚡ ROUTER DECISION 패널 (주황색)
- 📦 SKILLS FOR NEXT CALL (META 배지 + ← NEW)

```
┌──────────────────────────────┬──────────────────────────────────────┐
│      LIVE TRANSCRIPT         │  COPILOT                             │
│                              │                                      │
│  [C] 02:23 AM                │  LIVE SUMMARY                        │
│  "Our conversations get      │  Customer operates a conversational  │
│  really long, and users      │  application with multi-day...       │
│  come back the next day      │                                      │
│  expecting Claude to         │  ⚡ ROUTER DECISION                  │
│  remember what they said.    │  ┌────────────────────────────────┐  │
│  Is there a way to handle    │  │ Detected: Customer explicitly  │  │
│  that?"                      │  │ asked about Claude remembering │  │
│                              │  │ context across multiple days/  │  │
│  [S] 02:28 AM                │  │ sessions...                    │  │
│  "Then I can say for long    │  │                                │  │
│  conversations that span     │  │ Router DECIDES:                │  │
│  multiple days, you need     │  │ → attach memory_playbook       │  │
│  two complementary           │  │ → attach context_editing_guide │  │
│  features..."                │  │                                │  │
│                              │  │ Confidence: 95%                │  │
│                              │  └────────────────────────────────┘  │
│                              │                                      │
│                              │  📦 SKILLS FOR NEXT CALL             │
│                              │  ✅ META memory_playbook      ← NEW  │
│                              │  ✅ META context_editing_guide ← NEW │
│                              │  ○  fintech-patterns                 │
│                              │  ○  pricing-guidance                 │
│                              │                                      │
└──────────────────────────────┴──────────────────────────────────────┘
```

### Narration (20s) — SLOW DOWN, KEY MOMENT

> *(Point at the screen)*
>
> "Here's the Interview Copilot in action. Customer says: 'Users come back the next day expecting Claude to remember.'
>
> Watch the right panel. Router catches it instantly.
>
> 'Detected: Customer asked about remembering context across multiple days.' Decision: **attach memory_playbook and context_editing_guide**. Confidence 95%.
>
> See 'Skills for Next Call'? Two new skills just got attached — both marked META. The answerer's next response will draw from both.
>
> This is **lazy-loading team knowledge** in action."

---

### Screen 9 (2:22-2:42): Suggested Response + SOURCES

**실제 UI 요소 (Image 5):**
- 💡 SUGGESTED RESPONSE (노란색 헤더)
- Headline: "Use Memory for cross-session persistence and Context Editing to optimize within-session conversations."
- 3-step 솔루션 (주황색 왼쪽 바)
- 📁 SOURCES 섹션
- 92% confidence 바

```
┌──────────────────────────────┬──────────────────────────────────────┐
│      LIVE TRANSCRIPT         │  COPILOT                             │
│                              │                                      │
│  [C] 02:47 AM                │  💡 SUGGESTED RESPONSE               │
│  "our conversations get      │  ───────────────────────────────     │
│  really long, and users      │                                      │
│  come back the next day      │  Use Memory for cross-session        │
│  expecting Claude to         │  persistence and Context Editing     │
│  remember what they said.    │  to optimize within-session          │
│  Is there a way to handle    │  conversations.                      │
│  that"                       │                                      │
│                              │  → Store compliance-critical facts   │
│                              │    (KYC data, transaction history,   │
│                              │    regulatory flags) in Memory at    │
│                              │    natural conversation breaks...    │
│                              │                                      │
│                              │  → Within a single long conversation │
│                              │    use Context Editing's summarize() │
│                              │    to condense early exchanges when  │
│                              │    approaching 80-90% token capacity │
│                              │                                      │
│                              │  → At end-of-session checkpoints,    │
│                              │    write a Memory entry with:        │
│                              │    (1) customer financial profile    │
│                              │    (2) regulatory flags              │
│                              │    (3) next session priorities       │
│                              │                                      │
│                              │  ┌────────────────────────────────┐  │
│                              │  │ 📁 SOURCES                     │  │
│                              │  │ • cdp_memory/SKILL.md          │  │
│                              │  │ • cdp_context_editing/SKILL.md │  │
│                              │  │ • fintech-patterns/SKILL.md    │  │
│                              │  └────────────────────────────────┘  │
│                              │                                      │
│                              │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░ 92% confidence │
└──────────────────────────────┴──────────────────────────────────────┘
```

### Narration (20s) — EMPHASIZE SOURCES

> *(Point at the suggested response)*
>
> "Now look at the answer. Three specific steps — not generic advice.
>
> 'Store compliance-critical facts in Memory at natural breaks.' 'Use summarize() when approaching 80-90% token capacity.' 'Write Memory entries with customer profile, regulatory flags, next session priorities.'
>
> This is fintech-specific guidance. And scroll down — **Sources**.
>
> Three skill files. Every claim traces back to reviewed documentation.
>
> That's the difference between 'sounds right' and **auditable**."

---

### Screen 10 (2:42-3:10): Post-call Summary

**실제 UI 요소 (Images 3-4):**
- Interview Archived 배너 (초록색)
- Call Summary 카드
- Topics Covered / Customer Pain Points (2컬럼)
- Key Requirements
- Skill Update Proposals (2개 — ADD_PATTERN)
- Recommended Follow-ups

```
┌────────────────────────────────────────────────────────────────────┐
│  S Sigrid | Post-call: FinBot (Series B fintech, 50K+ users)...   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  📁 Interview Archived                     [View in Skills →]│   │
│  │  interview_records/learnings/2025-12-15_finbot_(series_b_...│   │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Call Summary                                               │   │
│  │  FinBot, a Series B fintech with 50K+ users, is struggling  │   │
│  │  with token cost explosion and context loss in their 20-50  │   │
│  │  turn Claude-powered financial advisor chatbot. Sarah Chen  │   │
│  │  (ex-Stripe, Head of Engineering) presented the challenge   │   │
│  │  of users returning multi-day later expecting Claude to     │   │
│  │  remember previous conversations...                         │   │
│  │                                                             │   │
│  │  Outcome: Solution positioned - follow-up expected to       │   │
│  │  discuss implementation details, pricing, and ROI...        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌─────────────────────────┐  ┌────────────────────────────────┐   │
│  │  Topics Covered         │  │  Customer Pain Points          │   │
│  │  • Cross-session        │  │  ⚠ Token cost explosion from   │   │
│  │    conversation persist │  │    20-50 turn conversations    │   │
│  │  • Multi-day memory     │  │  ⚠ Context loss requiring      │   │
│  │  • Token cost optim     │  │    users to repeat info        │   │
│  │  • Long conversation    │  │  ⚠ Users returning next day    │   │
│  │    context management   │  │    expecting context retained  │   │
│  │  • Financial advisor    │  │  ⚠ Managing conversation       │   │
│  │    chatbot use case     │  │    memory while maintaining    │   │
│  │  • Compliance in finte  │  │    compliance in fintech       │   │
│  └─────────────────────────┘  └────────────────────────────────┘   │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  fintech_patterns · ADD_PATTERN                              │  │
│  │  fintech_compliance_memory.md                                │  │
│  │  ┌────────────────────────────────────────────────────────┐  │  │
│  │  │ Compliance-aware Memory in Fintech: When implementing  │  │  │
│  │  │ Memory in financial services, ensure stored context    │  │  │
│  │  │ includes audit trail metadata (timestamp, conversation │  │  │
│  │  │ ID, user action confirmation). Memory should exclude   │  │  │
│  │  │ sensitive PII fields but retain transaction context... │  │  │
│  │  └────────────────────────────────────────────────────────┘  │  │
│  │  Sarah Chen's mention of 'compliance constraints' indicates  │  │
│  │  that fintech customers need guidance on implementing Memory │  │
│  │  in compliance-aware ways...                                 │  │
│  │                                   [Approve]  [Dismiss]       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Recommended Follow-ups                                      │  │
│  │  □ Send FinBot a ROI calculator showing token savings with   │  │
│  │    Memory + Context Editing vs. status quo (estimate 30-50%  │  │
│  │    reduction on resumed conversations)                       │  │
│  │  □ Prepare implementation architecture diagram showing       │  │
│  │    Memory storage strategy with compliance audit trails...   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Narration (28s)

> *(Transition to post-call summary)*
>
> "Call's done. I click 'End Call' and land here — the Post-call Summary.
>
> First — see 'Interview Archived'? The full transcript is saved automatically. Every call becomes searchable knowledge.
>
> Below that — Call Summary. Topics covered. Customer pain points — four of them extracted automatically. All by the Postmortem Agent.
>
> But here's the interesting part. Scroll down — **Skill Update Proposal**.
>
> 'fintech_patterns · ADD_PATTERN.' The agent detected a new pattern from this call: 'Compliance-aware Memory in Fintech.' It even wrote the content — audit trail metadata, conversation ID, PII handling.
>
> When I click Approve, this becomes part of our team's knowledge. Next fintech call? This pattern is already available."

---

### Screen 11 (3:10-3:40): Knowledge Base — Flywheel Complete

**실제 UI 요소 (Image 1):**
- Knowledge Base 타이틀 + 서브타이틀
- 🔀 Version Control 카드 (main 브랜치)
- ⚠ Uncommitted changes 경고
- Skills 목록 (접기/펼치기 가능)
- 📁 COMPANY KNOWLEDGE vs ✏️ INTERVIEW LEARNINGS 구분
- 날짜별 FinBot learnings + [Add Pattern] 버튼

```
┌─────────────────────────────────────────────────────────────────────┐
│  Knowledge Base  Company knowledge and learnings from previous     │
│                  interviews                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  🔀 Version Control                              ⌥ main       │  │
│  │  Last commit: edcf56b: still display names updated           │  │
│  │  Remote: https://github.com/sigridjineth/anthropic-assignment│  │
│  │                                                               │  │
│  │  ⚠ Uncommitted changes in skills/                            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  context_editing_guide                          📄 3  ✏️ 3  ∧ │  │
│  │  Managing context window, token optimization, summarization   │  │
│  │  strategies for long conversations.                           │  │
│  │                                                               │  │
│  │  📁 COMPANY KNOWLEDGE                                         │  │
│  │  📄 SKILL.md                                                  │  │
│  │  📄 references/persistent_facts.md                            │  │
│  │  📄 references/strategies.md                                  │  │
│  │                                                               │  │
│  │  ✏️ INTERVIEW LEARNINGS                                       │  │
│  │  💡 FinBot is a Series B fintech startup with 50K+ use       │  │
│  │                              [Add Pattern]    Dec 14, 2025   │  │
│  │  💡 FinBot is a Series B fintech startup with 50K+ use       │  │
│  │                              [Add Example]    Dec 14, 2025   │  │
│  │  💡 FinBot (Series B fintech, 50K+ users) has been usi       │  │
│  │                              [Add Pattern]    Dec 14, 2025   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  fintech-patterns                                📄 3  ✏️ 1  ∨ │  │
│  │  Common fintech customer patterns, objections, and success   │  │
│  │  stories. Compliance handling, long conversation management. │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (30s)

> *(Navigate to Skills page)*
>
> "Now let me show you where all this lives. This is the Knowledge Base.
>
> See Version Control at the top? Skills are in Git. Last commit, remote URL, uncommitted changes — just like code.
>
> Look at `context_editing_guide`. Two sections: **Company Knowledge** — the original skill files your team wrote. **Interview Learnings** — patterns extracted from actual calls.
>
> Those FinBot learnings I just approved? They show up here. Tagged with dates — December 14th. Ready to be promoted to Company Knowledge through a PR.
>
> This is what I mean by **single point of truth**. Not scattered in Slack. Not in someone's head. One reviewed, versioned, auditable surface.
>
> This is the flywheel: **Calls generate knowledge. Knowledge improves future calls.**
>
> And to be crystal clear: **Platform provides the primitives** — `container.skills`, `code_execution`. **My app provides everything else** — this UI, the Git integration, the learning extraction."

---

## [3:40-4:40] How to Build

### Screen 12 (3:40-3:55): Step 1 — Package Your Skills

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

### Screen 13 (3:55-4:10): Step 2 — Build Your Router

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

### Screen 14 (4:10-4:25): Step 3 — Attach Skills via API

```python
┌─────────────────────────────────────────────────────────────────────┐
│  Step 3: Attach Skills via container.skills                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  # Required beta headers (add files-api if you need file downloads) │
│  BETAS = ["skills-2025-10-02", "code-execution-2025-08-25"]         │
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
> Two beta headers: `skills` and `code-execution`. Upload your skill folder once — you get a `skill_id`. Then pass it in `container.skills`.
>
> What happens? Skill files appear at `/skills/{name}/` in the container. Claude reads only what the conversation needs — **lazy-loading** built into the platform."

---

### Screen 15 (4:25-4:40): Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  Agents Architecture                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │         Interview Copilot App (written in Python FastAPI)     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Interviewee    ┌─────────────┐    Session Created              ││
│  │ Persona   ────▶│ Prep Agent  │────▶ with skills enabled        ││
│  │                │ (Haiku 4.5) │                                  ││
│  │                └─────────────┘                                  ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Transcript ┌─────────────┐ ┌─────────────┐ Recommend Answers   ││
│  │ Entry ────▶│Router Agent │▶│Answer Agent │▶ running skills     ││
│  │            │(Haiku 4.5)  │ │(Sonnet 4.5) │  script on behind   ││
│  │            └─────────────┘ └─────────────┘                     ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ User clicks   ┌─────────────┐   Create & Update Skills         ││
│  │ 'End Call'───▶│Postmortem   │───▶ Reuse Skills afterwards      ││
│  │               │Agent(Haiku) │                                  ││
│  │               └─────────────┘                                  ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  Platform: container.skills + code_execution                        │
│  You: orchestration + agent design + workflow                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Narration (15s)

> *(Point at the diagram — walk through each flow)*
>
> "Here's the full picture. Three phases, four agents.
>
> **Pre-call**: Customer persona comes in → Prep Agent analyzes it → creates a session with baseline skills attached.
>
> **Live call**: Transcript entry → Router Agent decides which skill to add → Answer Agent generates the response with skills running behind the scenes. Router uses Haiku for speed. Answerer uses Sonnet for quality.
>
> **Post-call**: User ends the call → Postmortem Agent proposes skill updates → those learnings become reusable for the next call.
>
> This is *my* design. Yours could be simpler — even a single agent works.
>
> The pattern is what matters: **Your app orchestrates. The platform executes skills.**"

---

## [4:40-5:25] Wrap Up

### Screen 16: Wrap Up

```
┌─────────────────────────────────────────────────────────────────────┐
│  Wrap Up                                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Today = ONE use case (DevRel org knowledge)                        │
│                                                                     │
│  ANOTHER USE CASE                                                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  🧪 ML Training Scripts                                       │  │
│  │                                                               │  │
│  │  Team runs 100s of experiments — hyperparameters, configs,    │  │
│  │  what worked, what failed. Package as Skills.                 │  │
│  │                                                               │  │
│  │  Next teammate starting similar experiment?                   │  │
│  │  Claude surfaces the relevant knowledge automatically.        │  │
│  │                                                               │  │
│  │  → I wrote about this: hf.co/blog/sionic-ai/claude-code-...   │  │
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
> "So — that's Claude Skills.
>
> Today I showed DevRel org knowledge. But this is just one use case.
>
> Another example I use daily: ML training scripts. My team runs hundreds of experiments — hyperparameters, configs, what worked, what failed. We package all of that as Skills. Next time someone starts a similar experiment? Claude surfaces the relevant knowledge automatically. I wrote about this on my blog — link is on the screen."
>
> *(Pause, then point at resources)*
>
> "If you want to dig deeper — code is on GitHub, live demo is on Vercel.
>
> Questions? My email is right there. Reach out anytime — I'd love to hear what you build with Skills."
>
> *(Final beat — speak slower, with conviction)*
>
> "Platform provides the primitives. You build the orchestration.
>
> Together? **Agents with real capabilities.**"
>
> *(Smile, final beat)*
>
> "Go build something. Thanks for watching."

---

## Changes Summary: v9.7 → v9.8

| Section | v9.7 | v9.8 |
|---------|------|------|
| **Demo Section** | 4 screens (7-10) | **5 screens (7-11) — Knowledge Base 추가** |
| **Screen 7** | Session Ready (기존) | **Landing — Session Ready (유지)** |
| **Screen 8** | Dynamic Skill (간략) | **Router Decision Box (실제 UI 반영)** |
| **Screen 9** | Response + Sources | **Suggested Response + Sources (실제 UI 반영)** |
| **Screen 10** | Post-call (간략) | **Post-call Summary 상세 (실제 UI 반영)** |
| **Screen 11** | N/A | **NEW: Knowledge Base — Flywheel Complete** |
| **Customer name** | Sarah / FinBot 혼용 | **FinBot (Series B fintech, 50K+ users) 통일** |
| **Total runtime** | 5:12 | **5:25** |

---

## Changes Summary: v9.6 → v9.7

| Section | v9.6 | v9.7 |
|---------|------|------|
| **Slide Order** | Problem → RAG → How → Before/After | **Problem → How → Before/After → RAG** (PDF 순서) |
| **Live Demo slide** | None | **NEW: Screen 6.6 전환 슬라이드** |
| Screen 6.5 | "RAG helps find, Skills help ship" | **"Naive RAG for retrieval, Skills for execution"** |
| RAG description | "Consistent application" | **"Consistent & Accumulative"** |
| Skills trait | Not mentioned | **"Evolvable — every call improves the next"** |
| Total runtime | 5:10 | **5:12** |

---

## Changes Summary: v9.4 → v9.5

| Section | v9.4 | v9.5 |
|---------|------|------|
| Screen 14 | 5s narration | **15s with 3-phase walkthrough** |
| Architecture diagram | Simple 4-box | **Pre-call → Live call → Post-call flows** |
| Agent explanation | Brief | **Each agent's role + model choice** |
| Total runtime | 5:00 | **5:10** |

---

## Changes Summary: v9.3 → v9.4

| Section | v9.3 | v9.4 |
|---------|------|------|
| Screen 1 Title | "Modular capabilities..." | **"Make team knowledge flow"** |
| Screen 1 Hook | Problem-first | **+ Audience clarification (staff/EM/platform)** |
| Screen 4 | Silo problem | **+ EM metrics (interrupt cost, consistency)** |
| Persona | Implicit | **Explicit "Technical Leaders" anchor** |

---

## Changes Summary: v9.2 → v9.3

| Section | v9.2 | v9.3 |
|---------|------|------|
| Screen 4.5 | Binary RAG vs Skills | **Operational/consistency framing** |
| Screen 6 | "provably right" | **"verifiable"** |
| Screen 9 | "provably right" | **"auditable"** |
| Step 3 | 2 beta headers | **3 beta headers (+ files-api)** |

---

## Changes Summary: v9.1 → v9.2

| Section | v9.1 | v9.2 |
|---------|------|------|
| All Narrations | Functional | **Emotionally resonant + stage directions** |
| Screen 1 | Definition hook | **Problem-first "I should know this" moment** |
| Screen 4.5 | RAG vs Skills | **"RAG finds facts. Skills guide actions."** |
| Screen 8 | KEY MOMENT | **Beat-by-beat breakdown, "magic between API calls"** |
| Screen 10 | Post-call | **Flywheel concept introduced** |
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

## Key Safety Phrases (v9.7)

| Situation | Phrase |
|-----------|--------|
| Audience anchor | "If you're a staff engineer, an engineering manager, or anyone on a platform team — this is for you." |
| Hook (core message) | "The problem isn't lack of knowledge — it's that knowledge doesn't flow." |
| EM metrics | "Interrupt cost goes up, consistency goes down, auditability is zero." |
| Skills definition | "Skills are capability bundles. Org knowledge is ONE use case." |
| **Skills vs RAG** | **"Naive RAG for retrieval. Skills for execution — consistent, accumulative, evolvable."** |
| **Execution vs Finding** | **"Consistent execution matters more than finding the right chunk."** |
| memory_playbook | "Memory is a platform feature. I'm showing how we package our enablement guidance as a skill." |
| Without/With | "Claude is still capable — just missing YOUR org context." |
| Platform vs App | "Platform provides primitives. My app provides everything else." |
| Two layers | "Orchestration decides WHICH skill. Progressive disclosure works WITHIN the skill." |
| Agent | "The agent isn't the model — it's the orchestration." |
| Architecture | "Three phases, four agents. Router uses Haiku for speed. Answerer uses Sonnet for quality." |
| **Flywheel (evolvable)** | **"Skills are evolvable — every call can improve the next one."** |
| Trust | "Like installing software, use Skills you trust and review." |
| Sources | "Not 'sounds right' — verifiable and auditable." |
| PR workflow | "In production, you'd wire this to a GitHub PR workflow." |

---

## Technical Reference: API Integration

### Required Beta Headers
```python
BETAS = ["skills-2025-10-02", "code-execution-2025-08-25", "files-api-2025-04-14"]
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

## Runtime Breakdown (실제 UI 기반 v9.8)

| Section | Duration | Cumulative |
|---------|----------|------------|
| Title + Hook | 0:15 | 0:15 |
| Skills = Capabilities | 0:12 | 0:27 |
| Files + Git | 0:15 | 0:42 |
| The Problem | 0:18 | 1:00 |
| How it Works | 0:15 | 1:15 |
| Before/After | 0:13 | 1:28 |
| **Why Skills, Not RAG?** | **0:15** | **1:43** |
| **Live Demo Transition** | **0:02** | **1:45** |
| **Landing (Session Ready)** | **0:17** | **2:02** |
| **Router Decision** | **0:20** | **2:22** |
| **Suggested Response + Sources** | **0:20** | **2:42** |
| **Post-call Summary** | **0:28** | **3:10** |
| **Knowledge Base (NEW)** | **0:30** | **3:40** |
| Step 1: Package | 0:15 | 3:55 |
| Step 2: Router | 0:15 | 4:10 |
| Step 3: API | 0:15 | 4:25 |
| **Architecture** | **0:15** | **4:40** |
| Wrap Up | 0:45 | **5:25** |

---

## Pre-Recording Checklist

### Must-Say Phrases
- [ ] "If you're a staff engineer, an engineering manager, or anyone on a platform team" (Screen 1)
- [ ] "The problem isn't lack of knowledge — it's that knowledge doesn't flow" (Screen 1)
- [ ] "Skills are capability bundles. Org knowledge is ONE use case." (Screen 2)
- [ ] "Interrupt cost goes up, consistency goes down, auditability is zero" (Screen 4)
- [ ] "Two layers: orchestration decides WHICH skill, progressive disclosure works WITHIN" (Screen 5)
- [ ] "Claude is still capable — just missing YOUR context" (Screen 6)
- [ ] **"Naive RAG for retrieval. Skills for execution — consistent, accumulative, evolvable." (Screen 6.5)**
- [ ] **"Consistent execution matters more than finding the right chunk." (Screen 6.5)**
- [ ] "Memory is a platform feature. I'm showing our enablement guide." (Screen 7)
- [ ] "Not 'sounds right' — verifiable and auditable" (Screen 9)
- [ ] "Platform provides primitives. My app provides everything else." (Screen 10)
- [ ] "Three phases, four agents: Pre-call → Live call → Post-call" (Screen 14)
- [ ] "Router uses Haiku for speed. Answerer uses Sonnet for quality." (Screen 14)

### Visual Checkpoints (실제 UI 기반 v9.8)
| Time | What | Why |
|------|------|-----|
| 0:05 | Problem hook | Emotional connection |
| 0:20 | Platform vs Custom skills table | Framing |
| 1:05 | How it Works diagram | Orchestration flow |
| 1:20 | Before/After comparison | Quick proof |
| **1:35** | **RAG vs Skills comparison** | **Technical differentiation** |
| **1:43** | **Live Demo transition** | **Energy shift** |
| **2:02** | **Landing — Session Ready modal** | **Prep Agent baseline skills** |
| **2:15** | **Router Decision Box (주황색)** | **KEY MOMENT — skill attachment** |
| **2:35** | **Suggested Response + Sources** | **Auditable answers** |
| **2:55** | **Post-call Summary (상세)** | **Call Summary + Pain Points** |
| **3:20** | **Knowledge Base 페이지** | **Flywheel — learnings 축적** |
| **3:50** | **SKILL.md code** | **Technical credibility** |
| **4:15** | **container.skills API code** | **CDP integration** |
| **4:30** | **Agents Architecture diagram** | **3-phase flow visualization** |
| **5:00** | **"use Skills you trust"** | **Trust/review mention** |

---

*Script v9.8 — 실제 UI 스크린샷 기반 Demo Section 전면 개편 + Knowledge Base 추가*
*Last updated: 2025-12-15*
