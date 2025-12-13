# Important

- **NO MOCKS, NO SIMULATIONS** — This is a real, production-grade app. All responses must come from real Claude API calls.
- Read https://platform.claude.com/docs/en/home for each implementation.
- Use the latest features like Skills, Context Editing, Memory, etc.
- Implement Plan correctly.
- I love minimality. Write the code if and only if they are needed. Otherwise, consider removing it or simplifying it.
- Write in Python using `uv` package manager.
- **UI**: Clean white theme like ChatGPT (white background, subtle borders, green accent).

# Plan Summary

See `PLAN.md` for full details.

## Core Concept

**Interview Copilot** — helps sales reps during customer calls by:
1. **Pre-call (Landing)**: User describes call → Claude infers context → generates brief, topics, skills
2. **Live call (Session)**: Dynamic skill activation, real-time answers with sources
3. **Post-call**: Case notes + skill update proposals (P1)

## Key Principles

### Production-Grade
- Real Claude API calls only
- User inputs real transcript text
- Graceful error handling (not fallbacks)

### Clean White UI
- White/light gray backgrounds
- Inter font, subtle shadows
- Green accent (#10a37f)
- ChatGPT-inspired design

### 3-Agent Architecture
1. **Router** — Decides which skills to activate
2. **Summarizer** — Updates live summary, key moments
3. **Answerer** — Generates answers with skills attached

### Skills (4 domains)
- `roadmap` — ETA, timelines, safe messaging
- `architecture` — System design, data flow
- `security` — SOC2, compliance, encryption
- `pricing` — Plans, costs

## Implementation Phases

### Phase 1: Foundation
- Project setup (pyproject.toml)
- Data models (Pydantic)
- Config (settings)
- Skills content

### Phase 2: Landing Page
- ChatGPT-style centered input (natural language description)
- Claude infers context (no rule-based parsing)
- Prep Agent generates brief, likely topics, recommended skills
- Modal shows "Session Ready" → Enter Session

### Phase 3: Session Page
- Split panel (transcript + copilot)
- Router → Summarizer → Answerer flow
- Real-time state updates

### Phase 4: Polish
- Error handling
- Loading states
- Animations

## Reference Links

- [Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Context Editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
