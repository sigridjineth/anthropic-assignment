# Context Editing ROI Calculator

## Base Assumptions

- Average tokens per turn: 200 (user + assistant)
- Sonnet pricing: $3/1M input, $15/1M output
- Conversation distribution: 60% short (<10 turns), 30% medium (10-30), 10% long (30+)

## Without Context Editing

### Token Growth (Cumulative)

| Turn | Context Size | Cumulative Input | Cumulative Output |
|------|-------------|------------------|-------------------|
| 5 | 1,000 | 2,500 | 500 |
| 10 | 2,000 | 10,000 | 1,000 |
| 20 | 4,000 | 40,000 | 2,000 |
| 30 | 6,000 | 90,000 | 3,000 |
| 50 | 10,000 | 250,000 | 5,000 |

### Cost per Conversation (Sonnet)

| Turn | Input Cost | Output Cost | Total |
|------|-----------|-------------|-------|
| 10 | $0.03 | $0.015 | $0.045 |
| 20 | $0.12 | $0.03 | $0.15 |
| 30 | $0.27 | $0.045 | $0.315 |
| 50 | $0.75 | $0.075 | $0.825 |

## With Context Editing

### Compressed Context (Typical)

| Turn | Raw Size | Compressed | Savings |
|------|----------|------------|---------|
| 10 | 2,000 | 1,400 | 30% |
| 20 | 4,000 | 2,000 | 50% |
| 30 | 6,000 | 2,400 | 60% |
| 50 | 10,000 | 3,000 | 70% |

### Cost per Conversation (with CE)

| Turn | Input Cost | Output Cost | Total | Savings |
|------|-----------|-------------|-------|---------|
| 10 | $0.021 | $0.015 | $0.036 | 20% |
| 20 | $0.06 | $0.03 | $0.09 | 40% |
| 30 | $0.108 | $0.045 | $0.153 | 51% |
| 50 | $0.225 | $0.075 | $0.30 | 64% |

## Monthly Cost Impact

### Scenario: 50K MAU, 10 conversations each

**Without Context Editing**:
- Conversations: 500,000
- Avg cost/conv: $0.15 (assuming 20 avg turns)
- Monthly: **$75,000**

**With Context Editing**:
- Avg cost/conv: $0.09
- Monthly: **$45,000**
- **Savings: $30,000/month**

## Break-Even Analysis

Context Editing implementation cost:
- Engineering time: ~40 hours
- At $200/hr: $8,000

Break-even: Less than 1 month at scale

## Summary for Sales Conversations

> "For a 50-turn conversation, you're looking at roughly 64% token savings.
> That's about $0.82 down to $0.30 per conversation at Sonnet pricing.
>
> For 50,000 monthly active users with 10 conversations each —
> that's going from $75K to $45K monthly. $30K savings.
>
> The implementation typically pays for itself in the first month."
