---
name: architecture
description: Explains system architecture, technical implementation, algorithms, performance characteristics, and infrastructure details. Use when customers ask how things work under the hood or have technical deep-dive questions.
---

# Architecture Skill

## Purpose
Provide accurate technical explanations of system architecture, algorithms, and performance characteristics.

## When to Use
- "How does X work?"
- "What's the architecture?"
- "How do you handle [technical concern]?"
- Performance and scalability questions
- Infrastructure and reliability questions
- Algorithm or processing details

## Answer Guidelines

### Technical Depth
- Match the customer's technical level
- Start high-level, offer to go deeper
- Use diagrams/analogies when helpful

### Key Topics to Cover
1. **High-level architecture**: How components interact
2. **Processing pipeline**: Step-by-step flow
3. **Performance characteristics**: Latency, throughput
4. **Scalability approach**: How we handle growth
5. **Reliability measures**: Redundancy, failover

### Example Response Format
"Our processing pipeline works in three stages: First, documents are ingested and queued. Then, our ML models extract structured data. Finally, results are validated and returned via webhook or API. Average processing time is under 5 seconds for standard documents."

## Available References
- `references/system_overview.md` - High-level architecture
- `references/algorithm_faq.md` - ML and processing details
- `references/perf_limits.md` - Performance specifications

## Do NOT
- Share internal implementation details that could be security risks
- Reveal proprietary algorithm specifics
- Make performance guarantees beyond documented SLAs
