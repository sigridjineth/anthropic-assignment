---
type: add_pattern
skill: cdp_memory
source_file: cdp_memory.md
date: 2025-12-15T13:40:38.720530
company: FinBot (Series B fintech) is scaling an AI financi
---

# Add Pattern

**Multi-session Financial Advisory Pattern**: For consumer finance/investment advisory products with sessions spanning days or longer, use CDP Memory to persist user preferences, investment goals, risk profiles, and compliance-critical exclusion rules. This prevents context window overflow on 20-50+ turn conversations while ensuring compliance rules aren't lost through context truncation. Token cost reduction of ~30-40% achievable vs. naive context management.
