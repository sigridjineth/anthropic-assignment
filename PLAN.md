# Interview Copilot — Production Implementation Plan

> **Production-Grade**: No mocks, no simulations. Real Claude API calls only.

## Overview

**Persona**: Sigrid, Anthropic Developer Relations IC

**Goal**: Build a production-ready Interview Copilot that helps DevRel understand customer needs and recommend the right Claude Developer Platform (CDP) features.

- **Pre-call (Landing)**: DevRel describes upcoming call → AI generates session brief, likely topics, recommended skills
- **Live call (Session)**: Real-time transcript input → Dynamic skill activation → AI-powered answers with sources
- **Post-call**: Call notes + skill update proposals

**Key Value**: "Curated, versioned playbooks" — "Knowledge that flows to the field"

---

## Persona: Sigrid (Anthropic DevRel)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   👤 You: Sigrid — Anthropic Developer Relations                    │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   Role: Developer Relations IC                                      │
│   Mission: Help developers build better with Claude                 │
│                                                                     │
│   Today's call:                                                     │
│   • Technical discovery with potential enterprise customer          │
│   • They're evaluating Claude for their AI product                  │
│   • Need to understand their use case, recommend CDP features       │
│                                                                     │
│   Your tools:                                                       │
│   • Skills: CDP feature docs, pricing, case studies, best practices │
│   • Goal: Match their problem to the right platform feature         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

This persona is:
1. Injected into all Claude API calls
2. Displayed on the frontend

---

## Skills (CDP-focused)

### Skill Domains

| Skill ID | Name | Owner | Description |
|----------|------|-------|-------------|
| `cdp_context_editing` | Context Editing | platform-docs | Managing context window, token optimization |
| `cdp_memory` | Memory | platform-docs | Persistent memory across conversations |
| `cdp_skills` | Skills | platform-docs | Custom knowledge packages for agents |
| `fintech_patterns` | Fintech Patterns | devrel-learnings | Common fintech use cases, objections, wins |
| `pricing_guidance` | Pricing & Tiers | sales-enablement | Token pricing, tier recommendations |

### Skill Structure
```
skills/
├── cdp_context_editing/
│   ├── SKILL.md              # Entry point
│   └── references/
│       ├── strategies.md     # Summarization, extraction
│       └── persistent_facts.md
├── cdp_memory/
│   ├── SKILL.md
│   └── references/
│       └── cross_conversation.md
├── cdp_skills/
│   ├── SKILL.md
│   └── references/
│       └── skill_structure.md
├── fintech_patterns/
│   ├── SKILL.md
│   └── references/
│       ├── compliance_handling.md
│       └── long_conversation_handling.md
└── pricing_guidance/
    ├── SKILL.md
    └── references/
        └── context_editing_roi.md
```

---

## UX Flow

### Page 1: Landing (Pre-call Setup)

**URL**: `/`

**Purpose**: DevRel describes upcoming call in natural language

**UI Layout**:
```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│   👤 Sigrid — Anthropic DevRel                                  │
│   Role: Developer Relations IC                                  │
│                                                                 │
│               What's on the agenda today?                       │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │ Call with FinBot (fintech startup). Head of Engineering.  │ │
│   │ They're using Claude API for 6 months, having issues with │ │
│   │ long conversations and token costs.                        │ │
│   ├──────────────────────────────────────────────────────────┤ │
│   │ [🕐 Light thinking ▼]                              [→]  │ │
│   └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**After Submit → Session Ready Modal**:
```
┌──────────────────────────────────────────────────────────────┐
│  Session Ready: FinBot                                   [×]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  BRIEF                                                       │
│  Fintech (Series B) • Head of Engineering • Current user     │
│  Flagged: Long conversations, Token costs                    │
│                                                              │
│  LIKELY TOPICS                                               │
│  [Context window management (95%)]                           │
│  [Token cost optimization (90%)]                             │
│  [Memory / state persistence (75%)]                          │
│                                                              │
│  SKILLS                                                      │
│  ✅ cdp_context_editing  (pre-attached — likely needed)      │
│  ✅ fintech_patterns     (pre-attached — fintech customer)   │
│  ○  cdp_memory           (ready if needed)                   │
│  ○  pricing_guidance     (ready if needed)                   │
│                                                              │
│  ▸ Discovery Questions (expand)                              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                              [Back]  [Enter Session →]       │
└──────────────────────────────────────────────────────────────┘
```

### Page 2: Session (Live Copilot)

**URL**: `/session/{id}`

**Purpose**: Real-time assistance during the call

**UI Layout**:
```
┌────────────────────────────────────────────────────────────────┐
│  👤 Sigrid | Session: FinBot                    [ End Call ]   │
├──────────────────────────────┬─────────────────────────────────┤
│      TRANSCRIPT              │         COPILOT                 │
│                              │                                  │
│  ┌────────────────────────┐  │  🧠 Context Analysis            │
│  │ Add transcript entry   │  │  ─────────────────────────────  │
│  │                        │  │  Signals detected:              │
│  │ Speaker:               │  │  • "long conversations"         │
│  │ [Customer ▼]           │  │  • "loses track"                │
│  │                        │  │  • "burning through tokens"     │
│  │ Text:                  │  │                                  │
│  │ ┌──────────────────┐   │  │  ⚡ Using: cdp_context_editing  │
│  │ │                  │   │  │                                  │
│  │ └──────────────────┘   │  │  ─────────────────────────────  │
│  │ [ Add Entry ]          │  │                                  │
│  └────────────────────────┘  │  💡 Suggested Response           │
│                              │  "This is exactly what Context   │
│  ─────────────────────────── │  Editing is designed for..."     │
│                              │                                  │
│  [Customer] 14:32            │  📄 Sources:                     │
│  So yeah, we've been using   │  • cdp_context_editing/SKILL.md  │
│  Claude for about six months │  • fintech_patterns/...          │
│  ...long conversations...    │                                  │
│                              │  💡 Follow-up to ask:            │
│                              │  "What's your average length?"   │
│                              │                                  │
└──────────────────────────────┴─────────────────────────────────┘
```

---

## Architecture

### 3-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                     PRE-CALL                                │
│                                                             │
│  [Landing Input] → [Prep Agent] → [Session Brief]          │
│                    + Persona      [Likely Topics]           │
│                                   [Recommended Skills]      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     LIVE CALL                               │
│                                                             │
│  [Transcript Entry]                                         │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │   Router    │ → Decides which skills to attach          │
│  └─────────────┘   (pre-attach + dynamic)                  │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │ Summarizer  │ → Updates summary, key moments            │
│  └─────────────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │  Answerer   │ → Generates answer with skills            │
│  └─────────────┘   + Persona context                       │
│         │                                                   │
│         ▼                                                   │
│  [Suggested Answer + Sources + Follow-ups]                 │
└─────────────────────────────────────────────────────────────┘
```

### Persona Injection

All Claude API calls include the persona context:
```python
PERSONA_CONTEXT = """
You are helping Sigrid, an Anthropic Developer Relations IC.

Sigrid's role:
- Help developers build better with Claude
- Technical discovery with enterprise customers
- Match customer problems to CDP features

Sigrid's tools:
- CDP feature docs (Context Editing, Memory, Skills)
- Pricing guidance
- Fintech customer patterns and case studies
"""
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page (with persona display) |
| `/api/prep` | POST | Generate session brief |
| `/api/session` | POST | Create new session |
| `/session/{id}` | GET | Session page |
| `/api/session/{id}/transcript` | POST | Add transcript entry |
| `/api/session/{id}/ask` | POST | Direct question |
| `/api/session/{id}/state` | GET | Current session state |

---

## Implementation Checklist

### Phase 1: Foundation ✅
- [x] Project setup
- [x] Data models
- [x] Config
- [x] Skills content (original 4)

### Phase 2: Landing Page ✅
- [x] ChatGPT-style centered input
- [x] Prep Agent with tool use
- [x] Session creation flow

### Phase 3: Session Page ✅
- [x] Split panel layout
- [x] Router/Summarizer/Answerer agents
- [x] Real-time state updates

### Phase 4: DevRel Persona Update
- [ ] Update skills to CDP-focused
- [ ] Add persona config
- [ ] Inject persona into Claude calls
- [ ] Display persona on frontend
- [ ] Update UI text/labels

---

## UI Design Tokens

### Colors (ChatGPT-inspired)
```css
--bg-primary: #ffffff;
--bg-secondary: #f7f7f8;
--text-primary: #1a1a1a;
--text-secondary: #6b6b6b;
--border: #e5e5e5;
--accent: #10a37f;
```

---

## References

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Context Editing](https://docs.anthropic.com/en/docs/build-with-claude/context-editing)
- [Memory](https://docs.anthropic.com/en/docs/build-with-claude/memory)
