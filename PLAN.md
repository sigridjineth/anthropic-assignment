# Interview Copilot — Production Implementation Plan

> **Production-Grade**: No mocks, no simulations. Real Claude API calls only.

## Overview

**Persona**: Sigrid, Anthropic Developer Relations IC

**Goal**: Build a production-ready Interview Copilot that helps DevRel understand customer needs and recommend the right Claude Developer Platform (CDP) features.

- **Pre-call (Landing)**: DevRel describes upcoming call → AI generates session brief, likely topics, recommended skills
- **Live call (Session)**: Real-time transcript via ElevenLabs STT → Dynamic skill activation → AI-powered answers with sources
- **Post-call**: Call notes + skill update proposals → Learning saved to knowledge base

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
| `interview_records` | Interview Records | auto-generated | Full interview archives for reference |

### Skill Structure (with Learnings)

Skills now have two knowledge sources:
1. **Company Knowledge** — Curated docs in `SKILL.md` and `references/`
2. **Interview Learnings** — Auto-captured patterns from past calls in `learnings/`

```
skills/
├── cdp_context_editing/
│   ├── SKILL.md                    # Entry point (Company Knowledge)
│   ├── references/                 # Company Knowledge
│   │   ├── strategies.md
│   │   └── persistent_facts.md
│   └── learnings/                  # Interview Learnings (auto-generated)
│       ├── 2024-12-14_finbot.md
│       └── 2024-12-15_medassist.md
├── cdp_memory/
│   ├── SKILL.md
│   ├── references/
│   │   └── cross_conversation.md
│   └── learnings/
├── cdp_skills/
│   ├── SKILL.md
│   └── learnings/
├── fintech_patterns/
│   ├── SKILL.md
│   ├── references/
│   │   ├── compliance_handling.md
│   │   └── long_conversation_handling.md
│   └── learnings/
├── pricing_guidance/
│   ├── SKILL.md
│   ├── references/
│   │   └── context_editing_roi.md
│   └── learnings/
└── interview_records/              # META-SKILL: Full interview archives
    ├── SKILL.md
    └── learnings/                  # Auto-saved on session end
        ├── 2024-12-14_finbot.md
        └── 2024-12-15_medassist.md
```

### Learning File Format

When a skill update is approved post-call, it's saved with metadata:

```markdown
---
type: add_pattern
skill: cdp_context_editing
source_file: strategies.md
date: 2024-12-14T15:30:00
company: FinBot
---

# Add Pattern

### HIPAA Objection Handling
When customer mentions HIPAA concerns, emphasize...
```

### Interview Record Format (META-SKILL)

When a session ends, the full interview is auto-archived:

```markdown
---
type: interview_record
company: FinBot
date: 2024-12-14T15:30:00
duration_turns: 12
outcome: follow-up scheduled
topics:
  - context_editing
  - token_optimization
skills_used:
  - cdp_context_editing
  - fintech_patterns
---

# Interview: FinBot

## Summary
Discovery call with FinBot's Head of Engineering...

## Pain Points
- Long conversations filling context window
- Token costs scaling rapidly

## Transcript
[Customer] So yeah, we've been using Claude...
[Sales Rep] I hear you. Let me share...

## Skills Activated
- cdp_context_editing: Context management detected

## Follow-up Actions
- Schedule deep-dive on Context Editing
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
│   👤 Sigrid — Anthropic DevRel                           [📘]  │
│   Role: Developer Relations IC                                  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ 📅 Today's Calls (from Google Calendar)                  │  │
│   │                                                          │  │
│   │ 2:00 PM  FinBot        Sarah Chen · Head of Engineering  │  │
│   │ 4:30 PM  MedAssist AI  Dr. Park · CTO                    │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│               ─────── or describe your call ───────             │
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

**📘 Icon** → Links to `/skills` (Knowledge Base)

**After Submit → Session Ready Modal**:
```
┌──────────────────────────────────────────────────────────────┐
│  Session Ready                                           [×]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  BRIEF                                                       │
│  Fintech (Series B) • Head of Engineering • Current user     │
│  Flagged: Long conversations, Token costs                    │
│                                                              │
│  LIKELY TOPICS                                               │
│  [Context window management 95%]                             │
│  [Token cost optimization 90%]                               │
│  [Memory / state persistence 75%]                            │
│                                                              │
│  SKILLS                                                      │
│  ✅ cdp_context_editing  pre-attached                        │
│  ✅ fintech_patterns     pre-attached                        │
│  ○  cdp_memory           ready if needed                     │
│  ○  pricing_guidance     ready if needed                     │
│                                                              │
│  ▸ Discovery Questions (expand)                              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                              [Back]  [Enter Session →]       │
└──────────────────────────────────────────────────────────────┘
```

**Skill Pre-attachment Logic**:
- Claude's PrepAgent returns `recommended_skills` ordered by relevance
- First 2 → "pre-attached" (automatically used)
- Rest → "ready if needed" (activated dynamically)

### Page 2: Session (Live Copilot)

**URL**: `/session/{id}`

**Purpose**: Real-time assistance during the call with ElevenLabs STT

**UI Layout**:
```
┌────────────────────────────────────────────────────────────────┐
│  👤 Sigrid | Session: FinBot                    [ End Call ]   │
├──────────────────────────────┬─────────────────────────────────┤
│      TRANSCRIPT              │  COPILOT      [Claude thinking] │
│                              │                                  │
│  Speaker: [Customer ▼]       │  🧠 Live Summary                 │
│  ┌────────────────────────┐  │  ─────────────────────────────  │
│  │ 🎤 Listening...        │  │  Topics: Context management,    │
│  │ (Real-time from mic)   │  │  token costs, compliance        │
│  └────────────────────────┘  │                                  │
│                              │  ⚡ Skills Active                │
│  ─────────────────────────── │  cdp_context_editing             │
│                              │  fintech_patterns                │
│  [Customer] 14:32            │                                  │
│  So yeah, we've been using   │  💡 Suggested Response           │
│  Claude for about six months │  "This is exactly what Context   │
│  ...long conversations...    │  Editing is designed for..."     │
│                              │                                  │
│  [Sales Rep] 14:33           │  📄 Sources:                     │
│  I hear you. Let me share    │  • cdp_context_editing/SKILL.md  │
│  how Context Editing helps   │  • fintech_patterns/...          │
│                              │                                  │
└──────────────────────────────┴─────────────────────────────────┘
```

**STT Features** (ElevenLabs Realtime):
- WebSocket connection to ElevenLabs Scribe API
- Voice Activity Detection (VAD) auto-commits on silence
- Local fallback timer (2s) if VAD doesn't commit
- Yellow bubble shows real-time partial transcript
- Committed text moves to transcript list

### Page 3: Summary (Post-call)

**URL**: `/session/{id}/summary`

**Purpose**: Review call and approve skill learnings

**UI Layout**:
```
┌────────────────────────────────────────────────────────────────┐
│  👤 Sigrid | Post-call: FinBot    [View Skills] [New Session]  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CALL SUMMARY                                                   │
│  Discovery call with FinBot's Head of Engineering about        │
│  context window and token cost challenges in their chatbot.    │
│                                                                 │
│  Outcome: [Follow-up scheduled]                                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  TOPICS COVERED          │  CUSTOMER PAIN POINTS                │
│  • Context management    │  • Long conversations (20+ turns)    │
│  • Token optimization    │  • Token costs scaling rapidly       │
│  • Compliance concerns   │  • Context window filling up         │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  SUGGESTED SKILL UPDATES                                        │
│  New patterns detected that could improve future calls          │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ cdp_context_editing  [add_pattern]                          │ │
│  │ compliance_handling.md                                       │ │
│  │                                                              │ │
│  │ ### Fintech Compliance Pattern                               │ │
│  │ When customer mentions SOX compliance, emphasize that...     │ │
│  │                                                              │ │
│  │ Rationale: Effective pattern from FinBot call                │ │
│  │                                                              │ │
│  │                              [Approve]  [Dismiss]            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**Approve** → Saves to `skills/{skill_id}/learnings/{date}_{company}.md`

### Page 4: Skills (Knowledge Base)

**URL**: `/skills`

**Purpose**: View and manage company knowledge vs interview learnings

**UI Layout**:
```
┌────────────────────────────────────────────────────────────────┐
│  👤 Sigrid | Skills Management                [Back to Home]   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Knowledge Base                                                 │
│  Company knowledge and learnings from previous interviews       │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ▼ cdp-context-editing                         📘 3  💡 2   │ │
│  │                                                             │ │
│  │   COMPANY KNOWLEDGE                                         │ │
│  │   📘 SKILL.md                                               │ │
│  │   📄 references/strategies.md                               │ │
│  │   📄 references/persistent_facts.md                         │ │
│  │                                                             │ │
│  │   INTERVIEW LEARNINGS                                       │ │
│  │   💡 FinBot · add pattern · Dec 14, 2024                    │ │
│  │   💡 MedAssist · add example · Dec 15, 2024                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ▸ fintech_patterns                            📘 3  💡 0   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**📘** = Company Knowledge count, **💡** = Interview Learnings count

---

## Architecture

### Agent System

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
│  [ElevenLabs STT] → [Transcript Entry]                     │
│                            │                                │
│                            ▼                                │
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
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     POST-CALL                               │
│                                                             │
│  [End Session] → [PostCall Agent] → [Call Summary]         │
│                                      [Skill Update Proposals]│
│                                             │               │
│                                             ▼               │
│                  [Approve] → [Save to learnings/]          │
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

### Model Configuration

```python
# src/config.py
model_name: str = "claude-haiku-4-5-20251001"  # Fast, cost-effective
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page (with persona display) |
| `/session/{id}` | GET | Session page |
| `/session/{id}/summary` | GET | Post-call summary page |
| `/skills` | GET | Skills management page |
| `/api/prep` | POST | Generate session brief |
| `/api/session` | POST | Create new session |
| `/api/session/{id}/transcript` | POST | Add transcript entry |
| `/api/session/{id}/ask` | POST | Direct question |
| `/api/session/{id}/state` | GET | Current session state |
| `/api/session/{id}/end` | POST | End session, generate summary |
| `/api/stt/token` | GET | Get ElevenLabs STT token |
| `/api/skills` | GET | List all skills with knowledge/learnings |
| `/api/skills/update` | POST | Apply skill update (save learning) |

---

## Implementation Status

### P0: Core Demo Flow ✅
- [x] Project setup, data models, config
- [x] Landing page (ChatGPT-style input, Prep Agent)
- [x] Session page (transcript + copilot, 3-agent system)
- [x] DevRel persona (Sigrid) + CDP-focused skills
- [x] Skills API with fallback to prompt injection

### P0.5: Calendar Integration (Mock) ✅
- [x] Mock Google Calendar upcoming interviews on landing page
- [x] Click interview card → auto-fill context → prepare session
- [x] Show "Today's Calls" section with FinBot/MedAssist demo data
- [x] Visual: Calendar icon, time, company, attendee info

### P1: Post-call Features ✅
- [x] End session → Post-call page (`/session/{id}/summary`)
- [x] Auto-generated call notes (topics covered, outcome)
- [x] Skill update proposals (patterns detected → suggest edits)
- [x] Review/Approve/Dismiss workflow for updates
- [x] Learnings saved to `learnings/` subdirectory with metadata
- [x] **NEW**: Interview Records skill — full interview auto-archived on session end

### P2: Real-time STT ✅
- [x] ~~Browser Web Speech API~~ → **ElevenLabs Realtime STT**
- [x] WebSocket connection with single-use token auth
- [x] Voice Activity Detection (VAD) auto-commit
- [x] Local fallback timer (2 seconds)
- [x] Real-time partial transcript display (yellow bubble)
- [x] Transcript preserved during Claude processing

### P2.5: Skills Management ✅
- [x] `/skills` page to view knowledge base
- [x] Company Knowledge vs Interview Learnings distinction
- [x] Expandable skill cards with file listings
- [x] Learning metadata display (company, date, type)
- [x] Navigation links from Landing and Summary pages

### P3: Polish & Enhancements
- [ ] Streaming responses for better UX
- [ ] Session persistence (database)
- [ ] Export call notes (PDF/Markdown)
- [ ] Skill version history
- [ ] Learning search/filter

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI + Python 3.12 |
| AI | Claude API (Haiku 4.5) |
| STT | ElevenLabs Realtime Scribe |
| Frontend | Jinja2 + Alpine.js |
| Package Manager | uv |
| Styling | Custom CSS (ChatGPT-inspired) |

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

## Environment Variables

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=sk_...
```

---

## References

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Context Editing](https://docs.anthropic.com/en/docs/build-with-claude/context-editing)
- [Memory](https://docs.anthropic.com/en/docs/build-with-claude/memory)
- [ElevenLabs Realtime STT](https://elevenlabs.io/docs/speech-to-text/realtime-transcription)
