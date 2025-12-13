# Technical Sales Interview Copilot — Implementation Plan v2

> Synced with CLAUDE.md vNext (2024-01)

## Overview

**Goal**: Demonstrate Claude Skills value for Technical Sales by building a copilot that:
- Observes sales call transcripts in real-time
- Dynamically activates Skills when needed ("Observe → Decide → Act")
- Shows "Without Skills vs With Skills" comparison

**Key Message**: "Curated, versioned playbooks" / "Knowledge that flows to the field"

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12+ | Per CLAUDE.md |
| Package Manager | `uv` | Per CLAUDE.md |
| Backend | FastAPI | Async, lightweight |
| Frontend | HTML + HTMX + Alpine.js | Minimal, server-driven |
| Claude SDK | `anthropic` (Python) | Skills beta support |
| State | In-memory | Demo simplicity |

---

## Implementation Status

### Day 1: Foundation ✅ COMPLETE
- [x] Project setup (uv, pyproject.toml)
- [x] Data models (TranscriptEntry, RouterDecision, AnswerDraft, SummarizerState)
- [x] Skills content (roadmap, architecture, security, pricing)
- [x] SkillManager + SkillRegistry
- [x] Basic Router agent (keyword + LLM hybrid)
- [x] Basic Answerer agent (with/without skills)
- [x] Orchestrator (Router → Answerer flow)
- [x] API routes (session, transcript, ask, compare, simulation)
- [x] Frontend UI (transcript panel, copilot panel, ask input)
- [x] Demo scenario (fintech_discovery.json)

### Day 2: Agents & Robustness ✅ COMPLETE
- [x] Router cooldown (20s per domain)
- [x] Skill Fired event log (historical, not just current)
- [x] Summarizer agent (live summary, key moments, predicted questions)
- [x] Mock fallback data for API failures
- [x] case_studies skill content

### Day 3: META-SKILL & Polish
- [ ] META-SKILL (Update Proposal Generator)
- [ ] Raw JSON view for parse failures
- [ ] Error replay / graceful degradation
- [ ] UI polish (animations, transitions)

### Day 4: Testing & Demo Prep
- [ ] Unit tests (Router, Answerer, Orchestrator)
- [ ] End-to-end simulation test
- [ ] Second scenario (enterprise_security.json)
- [ ] Demo script / walkthrough

---

## P0 Implementation Checklist (from CLAUDE.md vNext)

| # | Task | Status |
|---|------|--------|
| 1 | Transcript simulation + UI skeleton | ✅ Done |
| 2 | Router agent (periodic) + Skill Fired UI | ✅ Done |
| 3 | Answerer (dynamic skills attach) + Suggested Answer card | ✅ Done |
| 4 | Ask Copilot input → Answerer | ✅ Done |
| 5 | Without/With comparison mode | ✅ Done |
| 6 | Summarizer (요약/예측 질문) | ✅ Done |
| 7 | META-SKILL (case note + diff/PR draft) | ❌ Not done |

---

## Architecture: 3-Agent + META-SKILL

```
┌─────────────────────────────────────────────────────────────────┐
│                    LIVE CALL FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Transcript Stream]                                            │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   Router    │───▶│  Summarizer  │───▶│    Answerer     │    │
│  │ (skill sel) │    │ (context)    │    │ (skills attach) │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│         │                   │                    │              │
│         ▼                   ▼                    ▼              │
│  [Skill Fired Log]  [Live Summary]      [Suggested Answer]     │
│                     [Key Moments]        [Sources/Confidence]   │
│                     [Predicted Q's]      [Follow-ups]           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    POST-CALL FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Call Complete]                                                │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    META-SKILL                            │   │
│  │            (Update Proposal Generator)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  [Case Note Generated]  [Diff/PR Draft Proposed]               │
│  (past_interviews/...)  ("Needs review" status)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Specifications

### Router Agent

**Input**:
- Recent 30-60s transcript chunk
- Current active skills
- (optional) Customer profile from Summarizer

**Output** (`RouterDecision`):
```python
{
    "needs_skill": bool,
    "suggested_skills": [{"domain": str, "confidence": float}],  # top 3
    "trigger_reason": str,
    "urgency": "high" | "medium" | "low",
    "detected_question": str | None
}
```

**Behavior**:
- Rule-based keyword matching first (fast)
- LLM fallback for ambiguous cases
- **Cooldown**: 20s per domain to prevent thrashing
- If confidence < threshold → suggest clarifying question instead

### Summarizer Agent

**Input**:
- Previous summary + recent transcript chunk (incremental)

**Output** (`SummarizerState`):
```python
{
    "customer_profile": {...},
    "goals": [...],
    "constraints": [...],
    "key_moments": [{"quote": str, "why_important": str, "importance": str}],
    "predicted_questions": [{"question": str, "probability": float, "domain": str}],
    "suggested_asks": [...],  # Discovery questions for sales
    "similar_cases": [...]    # If case_studies skill available
}
```

**Trigger**: Every 45-60s or on topic shift

### Answerer Agent

**Input**:
- Question (from Router or Ask Copilot)
- Summarizer state (context)
- Selected skills (from Router)

**Output** (`AnswerDraft`):
```python
{
    "answer": str,
    "sources": [{"title": str, "file": str, "excerpt": str}],
    "confidence": float,
    "caveats": [...],
    "followups": [...],
    "escalation_action": {"type": str, "draft_message": str} | None
}
```

**Behavior**:
- Attach skills via `container.skills`
- If uncertain → "확인 필요" + Slack draft
- Handle `pause_turn` for long operations

### META-SKILL Agent

**Trigger**: Post-call (manual or auto)

**Output**:
1. Case note file (`past_interviews/{company}_{date}.md`)
2. Skill update proposal (diff format, "Needs review")

**UI Display**:
- "✅ Draft PR created"
- "Suggested update to roadmap skill"
- NOT auto-applied (human review required)

---

## Skills Package

### Minimum Required (P0)

| Skill | Purpose | Status |
|-------|---------|--------|
| `roadmap` | ETA, GA status, timeline caveats | ✅ Done |
| `architecture` | How it works, performance, constraints | ✅ Done |
| `security` | SOC2, encryption, data residency | ✅ Done |

### Recommended (P1)

| Skill | Purpose | Status |
|-------|---------|--------|
| `pricing` | Plans, costs, enterprise options | ✅ Done |
| `case_studies` | Customer references, success stories | ⚠️ SKILL.md only |
| `competitive` | Positioning vs alternatives | ❌ Not done |

### Skill Content Principles

1. **Trigger clarity**: SKILL.md defines when to use
2. **Answer templates**: Structured for UI rendering
3. **No overclaims**: "example/illustrative" for unverified numbers
4. **Caveats built-in**: "Timelines subject to change"

---

## UI Components

### Left Panel: Transcript
- Real-time stream (simulation or STT)
- Speaker badges (prospect/sales/se)
- Recent 60s highlight
- Question markers (?)

### Right Panel: Copilot

| Component | Description | Priority |
|-----------|-------------|----------|
| **Skill Fired Log** | "⚡ roadmap (0.86) - 'when available'" | P0 |
| **Active Skills** | Attached (blue) vs Recommended (gray) | P0 |
| **Suggested Answer** | Answer + sources + confidence + caveats | P0 |
| **Live Summary** | 1-3 line summary of call so far | P1 |
| **Key Moments** | Important quotes with reasons | P1 |
| **Predicted Questions** | Next likely questions + domains | P1 |
| **Suggested Asks** | Discovery questions for sales | P1 |

### Bottom: Ask Copilot
- Text input → Answerer
- Compare toggle (Without/With)

---

## Demo Scenarios

### fintech_discovery.json ✅
Triggers: roadmap, architecture, security, pricing, case_studies

### enterprise_security.json (TODO)
Triggers: security (deep), deployment, compliance

---

## Fallback & Error Handling

| Failure Mode | Mitigation |
|--------------|------------|
| API timeout | Mock replay with cached responses |
| JSON parse error | Raw JSON view + minimal render |
| Skill not found | Graceful degradation, log warning |
| Router thrashing | 20s cooldown per domain |

---

## Day 2 Implementation Details

### 2.1 Router Cooldown (20s per domain)

**Problem**: Router can fire same skill multiple times in quick succession, causing UI thrashing.

**Solution**:
```python
# In Orchestrator
last_skill_fire: dict[str, float] = {}  # domain -> timestamp
COOLDOWN_SEC = 20.0

def should_fire_skill(domain: str) -> bool:
    now = time.time()
    if domain in last_skill_fire:
        if now - last_skill_fire[domain] < COOLDOWN_SEC:
            return False
    last_skill_fire[domain] = now
    return True
```

**Files to modify**:
- `src/services/orchestrator.py` - Add cooldown tracking

---

### 2.2 Skill Fired Event Log

**Problem**: No historical record of skill activations, only current state.

**Solution**:
```python
# New model in src/models/events.py
class SkillFiredEvent(BaseModel):
    timestamp: float
    domains: list[str]
    trigger_reason: str
    confidence: float
    detected_question: str | None
    urgency: str

# In Orchestrator
skill_fired_log: list[SkillFiredEvent] = []
```

**Files to create/modify**:
- `src/models/events.py` (NEW) - SkillFiredEvent model
- `src/services/orchestrator.py` - Store events in log
- `src/api/routes.py` - Add GET `/api/session/{id}/events` endpoint
- Update CopilotState to include `skill_fired_log`

---

### 2.3 Summarizer Agent

**Problem**: No live context extraction from conversation.

**Solution**:
```python
# New agent: src/agents/summarizer.py
class SummarizerAgent:
    async def summarize(
        self,
        previous_state: SummarizerState | None,
        recent_transcript: str,
        full_transcript: str
    ) -> SummarizerState:
        # LLM call to extract:
        # - customer_profile
        # - goals, constraints
        # - key_moments
        # - predicted_questions
        # - suggested_asks
```

**Trigger Logic**:
- Every 45-60 seconds of new transcript
- OR when topic shift detected by Router

**Files to create/modify**:
- `src/agents/summarizer.py` (NEW) - SummarizerAgent class
- `src/agents/__init__.py` - Export new agent
- `src/services/orchestrator.py` - Integrate Summarizer
- `src/api/routes.py` - Include summarizer_state in CopilotState

---

### 2.4 Mock Fallback Data

**Problem**: Demo breaks when API fails.

**Solution**:
```python
# New file: src/fallback.py
MOCK_ROUTER_DECISIONS = {
    "roadmap": RouterDecision(needs_skill=True, ...),
    "architecture": RouterDecision(needs_skill=True, ...),
}

MOCK_ANSWERS = {
    "roadmap": AnswerDraft(answer="Based on our current roadmap...", ...),
    "architecture": AnswerDraft(answer="Our architecture uses...", ...),
}
```

**Integration**:
- Wrap API calls in try/except
- On exception, lookup mock data by detected domain
- Log warning: "Using fallback data"

**Files to create/modify**:
- `src/fallback.py` (NEW) - Mock data definitions
- `src/agents/router.py` - Fallback on API error
- `src/agents/answerer.py` - Fallback on API error

---

### 2.5 case_studies Skill Content

**Problem**: case_studies skill is referenced but content is minimal.

**Solution**: Create rich content for fintech case study.

**Files to create**:
- `skills/case_studies/SKILL.md` - Enhanced skill definition
- `skills/case_studies/references/fintech_beta_bank.md` - Detailed case study
- `skills/case_studies/references/healthcare_pilot.md` - Second example

---

### 2.6 Day 2 Tasks Checklist

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 1 | Router cooldown | orchestrator.py | ✅ |
| 2 | SkillFiredEvent model | models/events.py | ✅ |
| 3 | Event log storage | orchestrator.py | ✅ |
| 4 | Events API endpoint | api/routes.py | ✅ |
| 5 | SummarizerAgent | agents/summarizer.py | ✅ |
| 6 | Summarizer integration | orchestrator.py | ✅ |
| 7 | Mock fallback data | fallback.py | ✅ |
| 8 | Fallback integration | router.py, answerer.py | ✅ |
| 9 | case_studies content | skills/case_studies/ | ✅ |
| 10 | Frontend updates | templates/, static/ | ✅ |

---

## Day 3 Tasks

1. **META-SKILL** - Post-call case note + proposal generator
2. **Suggested Asks** - Discovery questions in Summarizer
3. **Raw JSON view** - For debugging parse failures
4. **UI polish** - Skill Fired animations, transitions

---

## Day 4 Tasks

1. **Tests** - Router, Answerer, Orchestrator, E2E
2. **Second scenario** - enterprise_security.json
3. **Demo walkthrough** - Script for presenting
4. **Documentation** - Update README with demo instructions

---

## API Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/session` | POST | Create session | ✅ |
| `/api/session/{id}/transcript` | POST | Add entry | ✅ |
| `/api/session/{id}/state` | GET | Get full state | ✅ |
| `/api/session/{id}/ask` | POST | Ask copilot | ✅ |
| `/api/session/{id}/compare` | POST | With/Without | ✅ |
| `/api/session/{id}/simulation/start` | POST | Start demo | ✅ |
| `/api/session/{id}/simulation/step` | POST | Next entry | ✅ |
| `/api/session/{id}/events` | GET | Skill fired log | ✅ |
| `/api/session/{id}/end-call` | POST | Trigger META | ❌ |

---

## Success Criteria

1. ✅ Demo plays simulated transcript with skill activation
2. ✅ Ask Copilot returns skill-enhanced answers
3. ✅ Without/With comparison shows clear difference
4. ✅ Skill Fired log shows activation history
5. ✅ Summarizer provides live context
6. ❌ META-SKILL generates post-call proposals
7. ✅ Graceful fallback on errors

---

## References

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Anthropic Blog: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
