---
type: interview_record
company: FinBot (Series B fintech, 50K+ users) has built an
date: 2025-12-15T12:47:19.656727
duration_turns: 1
outcome: Discovery conversation - CDP Memory and Context Editing solutions introduced as potential fit for customer's core use case
topics:
  - Cross-session memory persistence
  - Multi-day conversation continuity
  - Token cost optimization
  - Context management in long conversations
  - Compliance constraints in financial advisory
skills_used:
  - cdp_memory
  - cdp_context_editing
---

# Interview: FinBot (Series B fintech, 50K+ users) has built an

## Summary

FinBot, a Series B fintech with 50K+ users, is struggling with token cost inflation and context loss in 20-50 turn conversations. Sarah (Head of Eng, ex-Stripe) needs a solution to preserve conversation memory across sessions (including multi-day gaps) while maintaining compliance constraints without naive truncation.

## Outcome

Discovery conversation - CDP Memory and Context Editing solutions introduced as potential fit for customer's core use case

## Pain Points

- Exploding token costs from long conversations
- Context loss between sessions
- Users expect continuity across days without naive truncation
- Need to preserve compliance constraints while managing token efficiency

## Requirements

- Cross-session memory persistence (multi-day)
- Cost-effective conversation management
- Compliance-aware context handling
- Support for 20-50 turn conversations with minimal token waste

## Transcript

[Customer] Our conversations get really long, and users come back the next day expecting Cloud to remember what they said. Is there a way to handle that?

## Skills Activated

- cdp_memory, cdp_context_editing: Customer has a direct question about cross-session persistence and user state management across multiple days. This is the core use case for CDP Memory. Context Editing is secondary since they may also need to manage token costs if summarizing long conversations.

## Follow-up Actions

- Send Memory API documentation with fintech-specific multi-session persistence examples
- Provide token cost comparison: 20-50 turn conversation with/without Memory API
- Schedule technical deep-dive with Sarah to design compliance-aware memory schema
- Share case study or reference customer (if available) of fintech using CDP Memory for similar use case
- Discuss pricing/ROI: quantify token savings at 50K user scale
