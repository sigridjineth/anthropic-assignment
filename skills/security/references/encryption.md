# Encryption & Data Protection

## Encryption Standards

### In Transit
- Protocol: TLS 1.3 (TLS 1.2 supported for compatibility)
- Certificate: 2048-bit RSA minimum
- Perfect Forward Secrecy: Enabled
- HSTS: Enforced

### At Rest
- Algorithm: AES-256-GCM
- Key management: AWS KMS
- Key rotation: Automatic (annual)
- Customer-managed keys: Available (Enterprise)

### Application Layer
- Sensitive fields: Additional encryption layer
- Tokenization: Available for PII
- Data masking: Configurable per field

## Key Management

### Default (Platform-managed)
- Keys managed in AWS KMS
- Automatic rotation
- Audit logging

### Customer-Managed Keys (Enterprise)
- Bring your own key (BYOK)
- Customer controls key lifecycle
- Revocation capability

## Data Handling

### Classification
- Public: Marketing materials
- Internal: System logs
- Confidential: Customer data
- Restricted: Authentication credentials

### Deletion
- Soft delete: Immediate
- Hard delete: Within 30 days
- Backup purge: Within 90 days
- Certificate of destruction: Available on request
