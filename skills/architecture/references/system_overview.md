# System Architecture Overview

## High-Level Architecture

```
                    ┌─────────────────────────────────────────────┐
                    │              Load Balancer (Global)          │
                    └─────────────────────┬───────────────────────┘
                                          │
                    ┌─────────────────────┴───────────────────────┐
                    │              API Gateway Layer               │
                    │    (Authentication, Rate Limiting, Routing)  │
                    └─────────────────────┬───────────────────────┘
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
          ▼                               ▼                               ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│  Document       │            │  Processing     │            │  Results        │
│  Ingestion      │───────────▶│  Pipeline       │───────────▶│  Delivery       │
│  Service        │            │  Service        │            │  Service        │
└─────────────────┘            └─────────────────┘            └─────────────────┘
          │                               │                               │
          ▼                               ▼                               ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│  Object Storage │            │  ML Model       │            │  Webhook        │
│  (Documents)    │            │  Cluster (GPU)  │            │  Dispatcher     │
└─────────────────┘            └─────────────────┘            └─────────────────┘
```

## Component Details

### API Gateway
- **Technology**: Kong/AWS API Gateway
- **Functions**:
  - JWT authentication
  - Rate limiting (configurable per tier)
  - Request routing
  - SSL termination

### Document Ingestion Service
- **Function**: Receives documents, validates format, queues for processing
- **Supported Formats**: PDF, PNG, JPG, TIFF, DOCX
- **Max File Size**: 50MB (Enterprise: 200MB)
- **Storage**: S3-compatible object storage with encryption at rest

### Processing Pipeline
- **Architecture**: Microservices with message queue (Kafka)
- **ML Infrastructure**: GPU clusters (NVIDIA A100)
- **Models**:
  - Document classification (proprietary CNN)
  - OCR (enhanced Tesseract + custom models)
  - Table extraction (transformer-based)
  - Entity extraction (fine-tuned LLM)

### Results Delivery
- **Synchronous**: API response (for small documents)
- **Asynchronous**: Webhook delivery (recommended for production)
- **Formats**: JSON, CSV, XML

## Infrastructure

### Cloud Providers
- Primary: AWS (us-east-1, eu-west-1, ap-northeast-1)
- DR: GCP (multi-region backup)

### Availability
- **SLA**: 99.9% uptime
- **Redundancy**: Multi-AZ deployment
- **Failover**: Automatic with <30s switchover

### Data Residency
- US region: Data stays in US
- EU region: Data stays in EU (GDPR compliant)
- APAC region: Coming Q2 2025
