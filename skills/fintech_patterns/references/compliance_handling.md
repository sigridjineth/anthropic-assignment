# Compliance Handling for Fintech

## The "Compliance Pause" Pattern

85% of fintech customers raise compliance concerns. The pattern:

1. **Initial interest**: "This sounds great..."
2. **Pause**: "[awkward pause]"
3. **Concern reveal**: "...but we're in fintech, so compliance..."
4. **Hidden fear**: "Our compliance team would kill me"

**Best response**: Don't wait for them to articulate. Lead with:
> "I know compliance is critical in fintech. Let me share how Acme Wealth handled this..."

## Key Compliance Topics

### SOC2 Audit
**Customer worry**: "Can we pass audit with AI?"
**Answer**: Yes. Pattern:
- Log all AI inputs and outputs
- Use persistent facts for audit trail
- Document constraint handling

**Success story**: Acme Wealth passed SOC2 with Context Editing

### GDPR / Data Privacy
**Customer worry**: "Where does data go?"
**Answer**:
- Data stays in your Claude API calls
- No training on customer data
- Enterprise: discuss data residency options

### Financial Regulation (SEC, FINRA, etc.)
**Customer worry**: "AI can't give financial advice"
**Answer**:
- Claude provides information, not advice
- Build guardrails in your app
- Use Skills to enforce compliance language

## Compliance-Safe Patterns

### Constraint Preservation
Never "forget" compliance-critical user statements:
```
User: "Don't recommend fossil fuels - we have ESG policy"
→ Extract to persistent facts
→ Never summarized away
→ Audit trail maintained
```

### Disclosure Templates
Build disclosures into Skills:
```
Every response about investments includes:
"This is informational only, not financial advice.
Consult a licensed advisor before making decisions."
```

### Audit Logging
What to log:
- User input (timestamped)
- Claude output (timestamped)
- Skills attached
- Constraints applied
