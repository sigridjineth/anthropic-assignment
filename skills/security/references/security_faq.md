# Security FAQ

## Data Handling

### Q: What data do you collect and store?
**Collected:**
- Documents uploaded for processing
- API request metadata (timestamps, endpoints)
- User account information

**Stored:**
- Documents: Retained for processing only, deleted within 24 hours (configurable)
- Results: Available for 30 days, then deleted
- Logs: 90 days for operational purposes

**Enterprise Option:** Zero-retention mode available (documents deleted immediately after processing)

### Q: Where is my data stored?
- **US Region**: AWS us-east-1 (N. Virginia)
- **EU Region**: AWS eu-west-1 (Ireland) - GDPR compliant
- **Backups**: Same region, different availability zone

Data never leaves your selected region.

### Q: Do you use customer data for training?
**No.** Customer documents are never used for:
- Model training
- Analytics
- Any purpose beyond processing the specific request

This is contractually guaranteed in our DPA.

## Access Control

### Q: Who can access my data?
- **Your team**: Based on roles you configure
- **Our team**: Only authorized engineers, for support purposes, with audit logging
- **Third parties**: None, unless explicitly authorized

### Q: What access controls are available?
- **SSO**: SAML 2.0, OIDC (Enterprise)
- **MFA**: Required for all accounts
- **RBAC**: Admin, Editor, Viewer roles
- **IP Allowlisting**: Enterprise tier
- **API Key Scoping**: Limit keys to specific operations

## Infrastructure Security

### Q: How is the infrastructure secured?
- **Network**: VPC isolation, WAF, DDoS protection
- **Compute**: Hardened containers, no persistent storage
- **Secrets**: HashiCorp Vault, rotated regularly
- **Monitoring**: 24/7 SOC, automated threat detection

### Q: Do you perform penetration testing?
Yes, annually by third-party firms:
- **Last test**: October 2024
- **Result**: No critical or high findings
- **Summary**: Available under NDA

### Q: What's your incident response process?
1. **Detection**: Automated monitoring + 24/7 SOC
2. **Response**: <1 hour for critical issues
3. **Notification**: Within 24 hours per DPA
4. **Resolution**: RCA provided within 5 business days

## Vendor Security Questionnaires

We maintain pre-completed responses for:
- SIG Lite / SIG Core
- CAIQ (Cloud Security Alliance)
- VSA (Vendor Security Alliance)
- Custom questionnaires (allow 5 business days)

Access via trust portal or request from your account team.
