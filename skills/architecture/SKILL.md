# Architecture Skill

## When to Use
- Questions about how the system works
- Data flow and processing questions
- Technical implementation details
- Performance and scalability questions
- Integration architecture questions

## Response Guidelines
1. **Start high-level, then go deeper**: Begin with a simple overview before technical details
2. **Use the 3-stage framework**: Ingestion → Processing → Delivery
3. **Be honest about constraints**: Don't oversell capabilities
4. **Provide context-appropriate depth**: Match technical depth to the audience

## Architecture Overview Template

"Our system works in three main stages:

1. **Ingestion**: Your data comes in via [method] and is immediately [processed/validated/encrypted]

2. **Processing**: We [analyze/transform/enrich] the data using [approach], with [key benefit]

3. **Delivery**: Results are [delivered via method] with [latency/frequency/format]"

## Key Technical Points
- All data encrypted in transit (TLS 1.3) and at rest (AES-256)
- Horizontal scaling with auto-scaling groups
- Multi-region availability (upon request)
- 99.9% uptime SLA for enterprise
