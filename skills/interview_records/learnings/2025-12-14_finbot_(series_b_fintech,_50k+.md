---
type: interview_record
company: FinBot (Series B fintech, 50K+ users) has been usi
date: 2025-12-14T12:39:02.216694
duration_turns: 2
outcome: Needs internal discussion / Solution evaluation (customer actively seeking alternatives to current implementation)
topics:
  - Token cost optimization
  - Long conversation management
  - Context window exhaustion
  - Information persistence across turns
  - Compliance and user preference tracking
skills_used:
  - pricing_guidance
---

# Interview: FinBot (Series B fintech, 50K+ users) has been usi

## Summary

FinBot, a Series B fintech with 50K+ users, has been using Claude API for 6 months but is hitting critical scaling limits. Their AI financial advisor chatbot experiences context loss by turn 15 in multi-turn conversations and faces unsustainable token costs on 20-50 turn conversations, with compliance gaps around managing user investment preferences and restrictions.

## Outcome

Needs internal discussion / Solution evaluation (customer actively seeking alternatives to current implementation)

## Pain Points

- Token exhaustion on 20-50 turn conversations
- Context loss by turn 15 (forgetting earlier conversation details)
- Unsustainable token costs ('burning through tokens')
- Inability to maintain compliance-critical state (investment restrictions, user preferences)

## Requirements

- Maintain conversation quality across 20-50 turn conversations without context loss
- Reduce token costs on long multi-turn conversations
- Preserve compliance-critical user preferences and investment restrictions across conversation turns
- Scale solution to 50K+ user base without budget breaking

## Transcript

[Customer] So yeah, we've been using cloud for six months now and it's been great for the most part, but like cloud just kind of loses track. Like by Masters 15, it's forgotten what we talked about in Masters 3 and we're burning through tokens like crazy. Is there any better way to handle this?

[Sigrid] foreign

## Skills Activated

- cdp_context_editing, cdp_memory: Customer is experiencing two critical issues: (1) token exhaustion across long conversations ('burning through tokens'), indicating they need context window optimization strategies, and (2) information loss across turns ('loses track by Masters 15'), indicating they need state persistence. Both skills are directly applicable. cdp_context_editing is highest priority because token cost is the immediate pain point, followed by memory for cross-turn context retention."
- pricing_guidance: Customer explicitly reports context loss at message 15 and high token consumption. Both cdp_context_editing (for handling long conversations and token optimization) and cdp_memory (for cross-session persistence to prevent forgetting) are directly applicable. Pricing guidance is relevant given their concern about 'burning through tokens like crazy' - they may benefit from understanding token costs and optimization ROI."

## Follow-up Actions

- Demo Memory API for storing investment restrictions and user preferences across turns
- Calculate token cost reduction ROI for FinBot's typical 20-50 turn conversation pattern
- Provide Context Editing guidance for optimizing long financial advisor conversations (turn 15+ challenge)
- Discuss compliance best practices for managing regulatory-critical state with Memory API
- Schedule follow-up with Sarah Chen and technical team to prototype on their financial advisor chatbot
