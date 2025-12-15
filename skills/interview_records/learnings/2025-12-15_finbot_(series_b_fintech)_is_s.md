---
type: interview_record
company: FinBot (Series B fintech) is scaling an AI financi
date: 2025-12-15T13:40:06.084631
duration_turns: 1
outcome: follow-up scheduled
topics:
  - Multi-session conversation persistence
  - Token cost optimization
  - Context window management
  - User state retention across days
  - Compliance considerations (preference rules, exclusions)
skills_used:
  - cdp_memory
  - pricing_guidance
---

# Interview: FinBot (Series B fintech) is scaling an AI financi

## Summary

FinBot, a Series B fintech serving 50K+ retail investors, is facing token cost and context window constraints on 20-50 turn conversations. Customer needs Claude to persist user state across sessions (users returning the next day expect memory of previous conversations), while maintaining compliance requirements around user preferences and exclusion rules.

## Outcome

follow-up scheduled

## Pain Points

- 20-50 turn conversations causing token cost explosion
- Context window overflow on extended conversations
- Naive truncation breaks user experience and breaks compliance (loses critical exclusion rules and preferences)
- Users expect state persistence across sessions (return next day expecting Claude to remember)

## Requirements

- Cross-session memory/state persistence
- Compliance-aware context management (preserve exclusion rules and preferences)
- Token cost reduction for long-running conversations
- Multi-day conversation continuity without context loss

## Transcript

[Customer] Our conversations get really long, and users come back the next day expecting Claude to remember what they said. Is there a way to handle that

## Skills Activated

- cdp_memory, pricing_guidance: Customer is asking about cross-session persistence and user state management - exactly what CDP Memory is designed for. The mention of 'long conversations' and users returning 'the next day' indicates a multi-session, stateful interaction pattern that requires memory capabilities rather than just context management.

## Follow-up Actions

- Schedule technical deep-dive on CDP Memory implementation with Sarah Chen (engineering lead)
- Prepare ROI analysis showing token cost reduction from naive truncation → CDP Memory approach
- Develop compliance preservation framework showing how Memory handles sensitive preference rules
- Provide fintech-specific reference architecture for multi-session financial advisor pattern
