---
type: interview_record
company: FinBot (Series B fintech) has 50K+ retail investor
date: 2025-12-15T12:57:33.476965
duration_turns: 1
outcome: Follow-up required to scope CDP Memory implementation and ROI analysis
topics:
  - Multi-session conversation persistence
  - Token cost optimization
  - Context window management
  - User preference retention
  - Compliance-critical state preservation
  - Cross-session continuity
skills_used:
  - cdp_memory
  - cdp_context_editing
---

# Interview: FinBot (Series B fintech) has 50K+ retail investor

## Summary

FinBot, a Series B fintech with 50K+ retail investors, is experiencing scaling challenges with their Claude-powered AI financial advisor chatbot. Long conversations (20-50 turns) are driving up token costs, context window exhaustion, and critical compliance data loss—users report the AI forgets preferences and constraints like stock exclusion filters across sessions.

## Outcome

Follow-up required to scope CDP Memory implementation and ROI analysis

## Pain Points

- Long conversations (20-50 turns) driving rapid token cost increases
- Context window exhaustion after extended use
- Information loss across sessions—users expect AI to remember preferences the next day
- Critical compliance constraints forgotten (e.g., stock exclusion filters)
- No current mechanism for persistent user state management

## Requirements

- Cross-session memory for user preferences and constraints
- Cost-effective solution that doesn't proportionally increase token spend
- Preservation of compliance-critical state (exclusion filters, investment rules)
- Seamless continuity—users should not need to re-explain context
- Scalability for 50K+ retail investor base

## Transcript

[Customer] Our conversations get really long and users come back the next day expecting Claude to remember what they said. Is there a way to handle that?

## Skills Activated

- cdp_memory, cdp_context_editing: Customer explicitly asked about Claude remembering information across sessions (next day). This is a direct CDP Memory use case - persistent state management across conversation sessions. Context Editing is secondary since it could help compress long conversations, but Memory is the primary solution for cross-session persistence.

## Follow-up Actions

- 1. Send CDP Memory technical overview + fintech use case example (e.g., FinBot scenario) to confirm Memory solves their cross-session persistence need
- 2. Scope Memory implementation: estimate compressed state size for 50K users (user prefs + constraints) and discuss storage backend options
- 3. ROI analysis: model token savings by session length (with/without Memory) and calculate payback period for integration effort
- 4. Compliance deep-dive: confirm how Memory will be architected to ensure FINRA/SEC compliance for investment exclusion rules and audit trails
- 5. Schedule technical architecture call with FinBot's engineering team to discuss Memory API integration, state serialization (JSON format for user prefs), and fallback handling
