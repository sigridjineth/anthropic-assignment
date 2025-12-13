# Long Conversation Handling in Fintech

## Why Fintech Has Long Conversations

1. **Complex queries**: Portfolio analysis spans many topics
2. **Follow-up questions**: "What about X?" after each answer
3. **Trust building**: Users need back-and-forth before acting
4. **Compliance disclosures**: Add length to every response

**Typical fintech conversation**: 20-50 turns

## The Problem

Without management:
- Turn 50 context: ~25,000 tokens
- Token costs: $7.50+ per conversation
- Lost context: Early turns forgotten
- User experience: "Claude doesn't remember"

## The Solution: Layered Context

```
┌─────────────────────────────────────────────────────────────┐
│  PERSISTENT LAYER (never compressed)                        │
│  • User constraints: "no fossil fuels"                      │
│  • Risk tolerance: "conservative"                           │
│  • Holdings discussed: ["AAPL", "GOOGL"]                    │
├─────────────────────────────────────────────────────────────┤
│  SUMMARY LAYER (compressed older turns)                     │
│  • "Discussed portfolio rebalancing options"                │
│  • "User concerned about tech concentration"                │
├─────────────────────────────────────────────────────────────┤
│  RECENT LAYER (verbatim last 5 turns)                       │
│  • Turn 46: User asked about bonds                          │
│  • Turn 47: Claude explained bond options                   │
│  • Turn 48: User asked about duration                       │
│  • Turn 49: Claude explained duration risk                  │
│  • Turn 50: [current turn]                                  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Steps

1. **Define extractable facts** for your domain
2. **Set compression thresholds** (e.g., summarize after turn 5)
3. **Build extraction prompts** for compliance-critical statements
4. **Test with real conversations** from your users

## Results at Scale

| Metric | Before | After |
|--------|--------|-------|
| Turn 50 context | 25,000 tokens | 7,500 tokens |
| Cost per conversation | $7.50 | $2.25 |
| "Claude forgets" complaints | 40% of users | 5% of users |
| SOC2 audit | Failed | Passed |
