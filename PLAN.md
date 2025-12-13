# Technical Sales Interview Copilot — Implementation Plan

## Overview

This document outlines the implementation tasks for building a **Technical Sales Interview Copilot** that demonstrates Claude's **Skills** feature value. The demo showcases how Skills enable "progressive disclosure" of domain knowledge during sales calls.

**Core Demo Value**: Show "Without Skills vs With Skills" comparison — identical prompt/model, only `container.skills` differs.

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12+ | Per CLAUDE.md requirement |
| Package Manager | `uv` | Per CLAUDE.md requirement |
| Backend Framework | FastAPI | Async, lightweight, OpenAPI docs |
| Frontend | HTML + HTMX + Alpine.js | Minimal JS, server-driven UI |
| Claude SDK | `anthropic` (Python) | Official SDK with Skills beta support |
| State | In-memory (dict) | Demo simplicity |

---

## API Requirements (from Claude Docs)

```python
# Required betas for Skills
betas = ["code-execution-2025-08-25", "skills-2025-10-02"]

# Required tool for Skills execution
tools = [{"type": "code_execution_20250825", "name": "code_execution"}]

# Skills in container (max 8 per request)
container = {
    "skills": [
        {"type": "custom", "skill_id": "skill_01...", "version": "latest"}
    ]
}
```

---

## Project Structure

```
anthropic-assignment/
├── pyproject.toml              # uv project config
├── CLAUDE.md                   # Spec (existing)
├── PLAN.md                     # This file
├── README.md                   # Usage instructions
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Settings (API keys, etc.)
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router.py           # Router Agent (skill selector)
│   │   ├── summarizer.py       # Summarizer Agent (context builder)
│   │   └── answerer.py         # Answerer Agent (skill executor)
│   │
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── manager.py          # Skill upload/retrieval
│   │   └── registry.py         # Domain → skill_id mapping
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transcript.py       # TranscriptEntry, Speaker
│   │   ├── router.py           # RouterDecision
│   │   ├── summarizer.py       # SummarizerState
│   │   └── answerer.py         # AnswerDraft
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orchestrator.py     # Coordinates agents
│   │   ├── transcript.py       # Transcript store
│   │   └── simulation.py       # Demo transcript playback
│   │
│   └── api/
│       ├── __init__.py
│       ├── routes.py           # FastAPI routes
│       └── websocket.py        # Real-time updates (optional)
│
├── skills/                     # Skill packages (uploaded to Claude)
│   ├── roadmap/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── roadmap.md
│   │       └── messaging.md
│   ├── architecture/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── system_overview.md
│   │       └── algorithm_faq.md
│   ├── security/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── compliance_matrix.md
│   │       └── security_faq.md
│   ├── pricing/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── pricing_faq.md
│   ├── case_studies/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── fintech_beta_bank.md
│   │       └── saas_gamma_payments.md
│   ├── competitive/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── battlecards.md
│   ├── integration/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── sdk_guide.md
│   └── deployment/
│       ├── SKILL.md
│       └── references/
│           └── deployment_options.md
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html              # Main copilot UI
│   └── components/
│       ├── transcript.html
│       ├── copilot_panel.html
│       ├── ask_input.html
│       └── compare_toggle.html
│
├── static/
│   ├── styles.css
│   └── app.js                  # Minimal Alpine.js logic
│
├── scenarios/                  # Demo transcript scenarios
│   ├── fintech_discovery.json
│   └── enterprise_security.json
│
└── tests/
    ├── __init__.py
    ├── test_router.py
    ├── test_answerer.py
    └── test_orchestrator.py
```

---

## Implementation Tasks

### Phase 0: Project Setup

| Task | Description | Priority |
|------|-------------|----------|
| 0.1 | Initialize `uv` project with `pyproject.toml` | P0 |
| 0.2 | Add dependencies: `anthropic`, `fastapi`, `uvicorn`, `jinja2`, `pydantic` | P0 |
| 0.3 | Create `src/config.py` with settings (ANTHROPIC_API_KEY from env) | P0 |
| 0.4 | Create basic FastAPI app in `src/main.py` | P0 |

### Phase 1: Data Models (Pydantic)

| Task | Description | Priority |
|------|-------------|----------|
| 1.1 | `TranscriptEntry` model (id, ts_ms, offset_sec, speaker, text) | P0 |
| 1.2 | `RouterDecision` model (needs_skill, suggested_skills, urgency, detected_question) | P0 |
| 1.3 | `SummarizerState` model (customer_profile, goals, key_moments, predicted_questions) | P1 |
| 1.4 | `AnswerDraft` model (answer, sources, confidence, caveats, followups) | P0 |

### Phase 2: Skills Content

| Task | Description | Priority |
|------|-------------|----------|
| 2.1 | Create `roadmap/SKILL.md` with trigger conditions + answer style guide | P0 |
| 2.2 | Create `roadmap/references/roadmap.md` with fictional product roadmap | P0 |
| 2.3 | Create `architecture/SKILL.md` + references | P0 |
| 2.4 | Create `security/SKILL.md` + `compliance_matrix.md` | P0 |
| 2.5 | Create `pricing/SKILL.md` + `pricing_faq.md` | P0 |
| 2.6 | Create `case_studies/SKILL.md` + 2 fictional case study files | P1 |
| 2.7 | Create `competitive/SKILL.md` + battlecard | P1 |
| 2.8 | Create `integration/SKILL.md` + SDK reference | P2 |
| 2.9 | Create `deployment/SKILL.md` + deployment options | P2 |

**SKILL.md Template:**
```markdown
---
name: roadmap
description: Answers questions about product roadmap, release timelines, feature availability, and GA status. Use when customer asks about ETAs, beta features, or upcoming releases.
---

# Roadmap Skill

## When to Use
- Customer asks "when will X be available?"
- Questions about beta/GA status
- Feature timeline inquiries

## Answer Style
- Always include caveat: "Timelines are subject to change"
- Be specific about current status (beta/GA/planned)
- Cite source file when available

## Available References
- `/skills/roadmap/references/roadmap.md` - Current product roadmap
- `/skills/roadmap/references/messaging.md` - Approved messaging guidelines
```

### Phase 3: Skill Management

| Task | Description | Priority |
|------|-------------|----------|
| 3.1 | `SkillManager` class: upload skills via `client.beta.skills.create()` | P0 |
| 3.2 | `SkillRegistry`: map domain names to skill_ids after upload | P0 |
| 3.3 | CLI command to upload all skills: `uv run python -m src.skills.manager upload` | P0 |
| 3.4 | CLI command to list skills: `uv run python -m src.skills.manager list` | P0 |

### Phase 4: Agents

#### 4.1 Router Agent

| Task | Description | Priority |
|------|-------------|----------|
| 4.1.1 | Implement rule-based keyword matching (0차 routing) | P0 |
| 4.1.2 | Implement LLM-based intent classification (1차 routing) | P0 |
| 4.1.3 | Return `RouterDecision` with top 3 suggested skills | P0 |
| 4.1.4 | Optimize for low latency (short prompt, low max_tokens) | P0 |

**Router Prompt Template:**
```
You are a skill router for a sales copilot. Analyze the recent transcript and determine which skills are needed.

Available skills: roadmap, architecture, security, pricing, case_studies, competitive, integration, deployment

Recent transcript (last 60 seconds):
{transcript_chunk}

Output JSON:
{
  "needs_skill": boolean,
  "suggested_skills": [{"domain": "...", "confidence": 0.0-1.0}],
  "urgency": "high|medium|low",
  "detected_question": "..."
}
```

#### 4.2 Summarizer Agent

| Task | Description | Priority |
|------|-------------|----------|
| 4.2.1 | Implement incremental summarization (prev_summary + new_chunk) | P1 |
| 4.2.2 | Extract customer_profile, goals, constraints | P1 |
| 4.2.3 | Generate key_moments with importance ratings | P1 |
| 4.2.4 | Generate predicted_questions with domain mapping | P1 |

#### 4.3 Answerer Agent

| Task | Description | Priority |
|------|-------------|----------|
| 4.3.1 | Implement skill-attached Claude call using `container.skills` | P0 |
| 4.3.2 | Handle "Without Skills" mode (same prompt, no skills) | P0 |
| 4.3.3 | Parse response into `AnswerDraft` | P0 |
| 4.3.4 | Handle uncertainty gracefully (escalation_action) | P0 |
| 4.3.5 | Handle `pause_turn` for long operations | P1 |

**Answerer API Call:**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "custom", "skill_id": skill_id, "version": "latest"}
            for skill_id in selected_skill_ids
        ]
    } if with_skills else None,
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}] if with_skills else None,
    messages=[{"role": "user", "content": prompt}]
)
```

### Phase 5: Orchestrator

| Task | Description | Priority |
|------|-------------|----------|
| 5.1 | `Orchestrator` class: coordinate Router → Answerer flow | P0 |
| 5.2 | Trigger routing on new transcript entry | P0 |
| 5.3 | Auto-invoke Answerer when urgency=high | P0 |
| 5.4 | Integrate Summarizer on 60s interval or topic shift | P1 |
| 5.5 | Maintain session state (current skills, summary) | P0 |

### Phase 6: API Routes

| Task | Description | Priority |
|------|-------------|----------|
| 6.1 | `POST /session` - Create new demo session | P0 |
| 6.2 | `POST /session/{id}/transcript` - Add transcript entry | P0 |
| 6.3 | `GET /session/{id}/state` - Get current copilot state | P0 |
| 6.4 | `POST /session/{id}/ask` - Ask Copilot directly | P0 |
| 6.5 | `POST /session/{id}/compare` - Run Without/With comparison | P0 |
| 6.6 | `POST /simulation/start` - Start transcript simulation | P0 |
| 6.7 | `POST /simulation/step` - Advance to next transcript line | P0 |

### Phase 7: Frontend UI

| Task | Description | Priority |
|------|-------------|----------|
| 7.1 | Base HTML template with 2-column layout | P0 |
| 7.2 | Transcript panel (left) with speaker badges | P0 |
| 7.3 | Copilot panel (right) with sections | P0 |
| 7.4 | Ask Copilot input (bottom) | P0 |
| 7.5 | Active Skills badge display | P0 |
| 7.6 | Without/With comparison toggle | P0 |
| 7.7 | Live Summary card | P1 |
| 7.8 | Predicted Questions list | P1 |
| 7.9 | Key Moments list | P1 |
| 7.10 | HTMX partial updates (polling or SSE) | P0 |

### Phase 8: Demo Scenarios

| Task | Description | Priority |
|------|-------------|----------|
| 8.1 | Create `fintech_discovery.json` scenario | P0 |
| 8.2 | Include roadmap, architecture, security questions | P0 |
| 8.3 | Include natural "skill trigger" moments | P0 |
| 8.4 | Create `enterprise_security.json` scenario | P1 |

**Scenario Format:**
```json
{
  "name": "Fintech Discovery Call",
  "customer": {
    "company": "Beta Bank",
    "industry": "fintech",
    "size": "500 employees"
  },
  "entries": [
    {
      "offset_sec": 0,
      "speaker": "sales",
      "text": "Thanks for joining today. Can you tell me about your current challenges?"
    },
    {
      "offset_sec": 15,
      "speaker": "prospect",
      "text": "We're looking at AI solutions for document processing. When will your PDF extraction feature be generally available?"
    }
  ]
}
```

### Phase 9: Testing

| Task | Description | Priority |
|------|-------------|----------|
| 9.1 | Test Router keyword matching | P0 |
| 9.2 | Test Answerer with/without skills comparison | P0 |
| 9.3 | Test Orchestrator flow | P0 |
| 9.4 | Test skill upload/retrieval | P0 |
| 9.5 | End-to-end simulation test | P1 |

---

## Implementation Order

### Day 1: Foundation
1. [0.1-0.4] Project setup with uv
2. [1.1, 1.2, 1.4] Core data models
3. [2.1-2.4] Essential skills content (roadmap, architecture, security, pricing)
4. [3.1-3.2] Skill manager and registry

### Day 2: Agents
5. [4.1.1-4.1.4] Router Agent (full implementation)
6. [4.3.1-4.3.4] Answerer Agent (full implementation)
7. [5.1-5.3, 5.5] Orchestrator (core flow)

### Day 3: API & UI
8. [6.1-6.7] API routes
9. [7.1-7.6, 7.10] Essential UI components
10. [8.1-8.3] Demo scenario

### Day 4: Polish
11. [1.3] Summarizer model
12. [4.2.1-4.2.4] Summarizer Agent
13. [5.4] Orchestrator summarizer integration
14. [7.7-7.9] Additional UI components
15. [9.1-9.5] Testing

---

## Key Design Decisions

### 1. Skills Architecture
- **8 domain-specific skills** matching the taxonomy in CLAUDE.md
- Each skill is self-contained with SKILL.md (instructions) + references (knowledge)
- Skills are uploaded once, then referenced by `skill_id` in API calls

### 2. Agent Separation
- **Router**: Fast, minimal context, returns skill recommendations
- **Summarizer**: Periodic, maintains conversation context
- **Answerer**: Slower, high quality, uses selected skills

### 3. Without/With Comparison
- Same prompt, same model, same output format
- Only difference: `container.skills` present or absent
- UI shows side-by-side results

### 4. Frontend Simplicity
- HTMX for server-driven updates (no React complexity)
- Alpine.js for minimal client-side state
- SSE or polling for real-time updates

### 5. Demo-First Design
- Simulation mode as default (reliable)
- Pre-scripted scenarios with clear skill trigger moments
- In-memory state (no database needed)

---

## Success Criteria

1. **Demo Flow**: User can play a simulated transcript and see skills activate automatically
2. **Ask Copilot**: User can type questions and get skill-enhanced answers
3. **Without/With**: Side-by-side comparison clearly shows skill value
4. **Observability**: UI shows which skill was selected and why
5. **Reliability**: No crashes during demo; graceful error handling

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Skills API changes | Pin to specific beta versions, monitor docs |
| Slow API responses | Use haiku for Router, stream Answerer responses |
| Skill content quality | Iterate on SKILL.md prompts, test with real questions |
| UI complexity | Keep it minimal, use HTMX not React |
| Demo instability | Simulation mode by default, no live STT |

---

## References

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Code Execution Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic Engineering Blog: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
