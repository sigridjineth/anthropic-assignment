# Technical Sales Copilot — Production Implementation Plan

> **Production-Grade**: No mocks, no simulations. Real Claude API calls only.

## Overview

**Goal**: Build a production-ready Technical Sales Copilot that:
- **Pre-call (Landing)**: Sales rep inputs customer context → AI generates session brief, likely topics, discovery questions, recommended skills
- **Live call (Session)**: Real-time transcript input → Dynamic skill activation → AI-powered answers with sources
- **Post-call**: Case notes + skill update proposals

**Key Value**: "Curated, versioned playbooks" — "Knowledge that flows to the field"

---

## Design Principles

### 1. Production-Grade
- **NO mocks** — All responses from real Claude API
- **NO simulations** — User inputs real transcript text
- **NO fallbacks** — Graceful error handling with user feedback
- Real-time streaming responses where applicable

### 2. Clean White UI (ChatGPT-style)
- White/light gray background
- Clean typography (Inter or system font)
- Subtle shadows and borders
- Smooth transitions and animations
- Mobile-responsive design

### 3. Minimalism
- Only build what's needed
- Simple, clear interfaces
- No unnecessary complexity

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12+ | Modern, async support |
| Package Manager | `uv` | Fast, reliable |
| Backend | FastAPI | Async, lightweight, production-ready |
| Frontend | HTML + Alpine.js + Tailwind CSS | Minimal, reactive, beautiful |
| AI | Claude API (anthropic SDK) | Latest features |
| State | In-memory (dict) | Demo simplicity |

---

## UX Flow

### Page 1: Landing (Pre-call Setup)

**URL**: `/`

**Purpose**: Sales rep describes upcoming call in natural language

**UI Layout** (ChatGPT-style centered input):
```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│                          [Logo]                                 │
│                                                                 │
│               What's on the agenda today?                       │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │ Meeting with Acme Payments (Fintech), Head of            │ │
│   │ Engineering. Technical discovery. Concerned about        │ │
│   │ compliance and on-prem options.                          │ │
│   ├──────────────────────────────────────────────────────────┤ │
│   │ [🕐 Light thinking ▼]                              [→]  │ │
│   └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│                  Press Ctrl+Enter to start                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**After Submit → Modal Shows**:
```
┌──────────────────────────────────────────────────────────────┐
│  Session Ready                                          [×]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  BRIEF                                                       │
│  Fintech (Series B) • Head of Engineering • Tech Discovery   │
│  Flagged: On-premise, Compliance                             │
│                                                              │
│  LIKELY TOPICS                                               │
│  [System architecture (90%)] [On-prem options (85%)]         │
│  [Security certifications (80%)]                             │
│                                                              │
│  SKILLS                                                      │
│  ✅ architecture  (pre-attached)                             │
│  ✅ security      (pre-attached)                             │
│  ✅ roadmap       (pre-attached)                             │
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

**UI Layout** (Split panel, white background):
```
┌────────────────────────────────────────────────────────────────┐
│  Sales Copilot | Session: Acme Corp          [ End Call ]     │
├──────────────────────────────┬─────────────────────────────────┤
│      TRANSCRIPT              │         COPILOT                 │
│                              │                                  │
│  ┌────────────────────────┐  │  📊 Live Summary                │
│  │ Add transcript entry   │  │  ─────────────────────────────  │
│  │                        │  │  CTO exploring data solutions   │
│  │ Speaker:               │  │  for fintech platform.          │
│  │ [Prospect ▼]           │  │                                  │
│  │                        │  │  ⚡ Skill Fired                  │
│  │ Text:                  │  │  architecture (0.92)             │
│  │ ┌──────────────────┐   │  │  "data flow" detected            │
│  │ │                  │   │  │                                  │
│  │ │                  │   │  │  🔧 Active Skills                │
│  │ │                  │   │  │  [architecture] attached         │
│  │ └──────────────────┘   │  │  [security] recommended          │
│  │                        │  │                                  │
│  │ [ Add Entry ]          │  │  ─────────────────────────────  │
│  └────────────────────────┘  │                                  │
│                              │  💬 Suggested Answer             │
│  ─────────────────────────── │  "Our system processes data in   │
│                              │   three stages: ingestion via    │
│  [Prospect] 14:32            │   secure APIs, real-time         │
│  So we're looking at how     │   processing with encryption,    │
│  the data flows through      │   and delivery to your           │
│  your system...              │   endpoints..."                  │
│                              │                                  │
│  [Sales] 14:33               │  📚 Sources                      │
│  Great question...           │  • architecture/SKILL.md         │
│                              │  • architecture/data_flow.md     │
│                              │                                  │
│                              │  ⚠️ Caveats                      │
│                              │  • Latency varies by use case    │
│                              │                                  │
│                              │  🎯 Confidence: 92%              │
│                              │                                  │
│                              │  ─────────────────────────────  │
│                              │                                  │
│                              │  💬 Ask Copilot                  │
│                              │  ┌─────────────────────────────┐│
│                              │  │ Type your question...       ││
│                              │  └─────────────────────────────┘│
│                              │  [ Ask ]                         │
│                              │                                  │
└──────────────────────────────┴─────────────────────────────────┘
```

### Page 3: Post-call (Future - P1)

Case notes + skill update proposals.

---

## Architecture

### 3-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                     PRE-CALL                                │
│                                                             │
│  [Landing Input] → [Prep Agent] → [Session Brief]          │
│                                   [Likely Topics]           │
│                                   [Discovery Questions]     │
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
│  │   Router    │ → Decides which skills to activate        │
│  └─────────────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │ Summarizer  │ → Updates live summary, key moments       │
│  └─────────────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │  Answerer   │ → Generates answer with skills attached   │
│  └─────────────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  [Suggested Answer + Sources + Caveats + Confidence]       │
└─────────────────────────────────────────────────────────────┘
```

### Agent Specifications

#### Prep Agent (Landing)
- **Input**: Company, industry, roles, purpose, sensitive topics, competitors
- **Output**:
  - `session_brief`: 3-sentence summary
  - `likely_topics`: Top 3 with reasoning
  - `discovery_questions`: 5 suggested questions
  - `recommended_skills`: List of skill domains

#### Router Agent (Session)
- **Input**: Recent transcript text, current skills, customer context
- **Output**:
  - `needs_skill`: boolean
  - `suggested_skills`: List with confidence scores
  - `trigger_reason`: Why this skill was selected
  - `detected_question`: Extracted customer question (if any)
  - `urgency`: high/medium/low
- **Behavior**: 20s cooldown per domain to prevent thrashing

#### Summarizer Agent (Session)
- **Input**: Previous summary + new transcript chunk
- **Output**:
  - `summary`: Current call summary (2-3 sentences)
  - `key_moments`: Important quotes with context
  - `predicted_questions`: What customer might ask next
  - `customer_profile`: Inferred needs/constraints

#### Answerer Agent (Session)
- **Input**: Question, context, selected skills
- **Output**:
  - `answer`: Conversational response
  - `sources`: Which skill files were used
  - `confidence`: 0.0-1.0
  - `caveats`: Important disclaimers
  - `followups`: Suggested follow-up questions

---

## Skills Package

### Structure
```
skills/
├── roadmap/
│   ├── SKILL.md           # When to use, response guidelines
│   └── references/
│       ├── roadmap.md     # Feature timelines
│       └── messaging.md   # Safe language for timelines
├── architecture/
│   ├── SKILL.md
│   └── references/
│       ├── system_overview.md
│       └── data_flow.md
├── security/
│   ├── SKILL.md
│   └── references/
│       ├── compliance.md
│       └── encryption.md
└── pricing/
    ├── SKILL.md
    └── references/
        └── plans.md
```

### Skill Content Principles
1. **Trigger clarity**: SKILL.md defines when to use
2. **Safe messaging**: Built-in caveats (e.g., "timelines subject to change")
3. **Structured output**: Designed for UI rendering
4. **No overclaims**: Example/illustrative for unverified data

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/api/prep` | POST | Generate session brief (Prep Agent) |
| `/api/session` | POST | Create new session |
| `/session/{id}` | GET | Session page |
| `/api/session/{id}/transcript` | POST | Add transcript entry (triggers Router → Answerer) |
| `/api/session/{id}/ask` | POST | Direct question to Answerer |
| `/api/session/{id}/state` | GET | Current session state |

---

## Data Models

```python
# Landing
class PrepInput(BaseModel):
    company: str
    industry: str
    roles: list[str]
    purpose: str  # discovery | technical | pricing
    sensitive_topics: list[str]
    competitors: str | None

class PrepResult(BaseModel):
    session_brief: str
    likely_topics: list[dict]  # [{topic, reason}]
    discovery_questions: list[str]
    recommended_skills: list[str]

# Session
class TranscriptEntry(BaseModel):
    speaker: str  # prospect | sales | se
    text: str
    timestamp: datetime

class RouterDecision(BaseModel):
    needs_skill: bool
    suggested_skills: list[dict]  # [{domain, confidence}]
    trigger_reason: str
    detected_question: str | None
    urgency: str

class AnswerDraft(BaseModel):
    answer: str
    sources: list[dict]  # [{title, file, excerpt}]
    confidence: float
    caveats: list[str]
    followups: list[str]
    skills_used: list[str]

class SummarizerState(BaseModel):
    summary: str
    key_moments: list[dict]
    predicted_questions: list[dict]
    customer_profile: dict
```

---

## File Structure

```
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── prep.py          # Prep Agent
│   │   ├── router.py        # Router Agent
│   │   ├── summarizer.py    # Summarizer Agent
│   │   └── answerer.py      # Answerer Agent
│   ├── models/
│   │   ├── __init__.py
│   │   ├── prep.py
│   │   ├── transcript.py
│   │   ├── router.py
│   │   ├── answerer.py
│   │   └── summarizer.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orchestrator.py  # Coordinates agents
│   │   └── session.py       # Session state management
│   └── api/
│       ├── __init__.py
│       └── routes.py        # API endpoints
├── skills/
│   ├── roadmap/
│   ├── architecture/
│   ├── security/
│   └── pricing/
├── templates/
│   ├── base.html
│   ├── landing.html
│   └── session.html
└── static/
    └── styles.css           # Tailwind-based white theme
```

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Project setup (pyproject.toml, uv)
- [ ] Data models (all Pydantic models)
- [ ] Config (settings, API key handling)
- [ ] Skills content (4 skills with references)

### Phase 2: Landing Page
- [ ] Landing template (white ChatGPT-style)
- [ ] Prep Agent implementation
- [ ] `/api/prep` endpoint
- [ ] Session creation flow

### Phase 3: Session Page
- [ ] Session template (split panel)
- [ ] Transcript input UI
- [ ] Router Agent implementation
- [ ] Summarizer Agent implementation
- [ ] Answerer Agent implementation
- [ ] Orchestrator (coordinates agents)
- [ ] Real-time state updates

### Phase 4: Polish
- [ ] Error handling (graceful, user-friendly)
- [ ] Loading states
- [ ] Animations/transitions
- [ ] Mobile responsiveness

---

## UI Design Tokens

### Colors (ChatGPT-inspired white theme)
```css
--bg-primary: #ffffff;
--bg-secondary: #f7f7f8;
--text-primary: #1a1a1a;
--text-secondary: #6b6b6b;
--border: #e5e5e5;
--accent: #10a37f;  /* Green accent */
--accent-hover: #0d8a6a;
```

### Typography
```css
--font-sans: 'Inter', -apple-system, system-ui, sans-serif;
--font-mono: 'SF Mono', monospace;
```

### Spacing
```css
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-6: 1.5rem;
--space-8: 2rem;
```

---

## Success Criteria

1. Landing page generates useful session brief via real Claude API
2. Session page accepts transcript input and provides real-time assistance
3. Skills are dynamically activated based on conversation context
4. Sources and caveats are clearly displayed
5. UI is clean, white, professional (ChatGPT-style)
6. No mocks, no simulations — 100% production code

---

## References

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic Blog: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
