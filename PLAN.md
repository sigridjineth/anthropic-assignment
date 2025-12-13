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

### Day 2: Agents & Robustness 🔄 IN PROGRESS
- [ ] Router cooldown (20s per domain)
- [ ] Skill Fired event log (historical, not just current)
- [ ] Summarizer agent (live summary, key moments, predicted questions)
- [ ] Mock fallback data for API failures
- [ ] Raw JSON view for parse failures

### Day 3: META-SKILL & Polish
- [ ] META-SKILL (Update Proposal Generator)
- [ ] case_studies skill content
- [ ] Suggested Asks (discovery questions for sales)
- [ ] Error replay / graceful degradation

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
| 2 | Router agent (periodic) + Skill Fired UI | ⚠️ Partial |
| 3 | Answerer (dynamic skills attach) + Suggested Answer card | ✅ Done |
| 4 | Ask Copilot input → Answerer | ✅ Done |
| 5 | Without/With comparison mode | ✅ Done |
| 6 | Summarizer (요약/예측 질문) | ❌ Not done |
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

## Day 2 Tasks (Priority Order)

1. **Router cooldown** - Add 20s per-domain cooldown
2. **Skill Fired event log** - Store and display history
3. **Summarizer agent** - Implement incremental summarization
4. **Mock fallback** - Create mock response data
5. **case_studies content** - Add fintech_beta_bank.md

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
| `/api/session/{id}/end-call` | POST | Trigger META | ❌ |
| `/api/session/{id}/events` | GET | Skill fired log | ❌ |

---

## Success Criteria

1. ✅ Demo plays simulated transcript with skill activation
2. ✅ Ask Copilot returns skill-enhanced answers
3. ✅ Without/With comparison shows clear difference
4. ⚠️ Skill Fired log shows activation history
5. ❌ Summarizer provides live context
6. ❌ META-SKILL generates post-call proposals
7. ⚠️ Graceful fallback on errors

---

## References

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Anthropic Blog: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
