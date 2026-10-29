# ADR-001: Use a Modular Monolith for CDC

## Context

CDC is a production hardware-shop service for Slovakia, operated by one shop with merchant employees. It must support all 25 user stories in [CDC.txt](../data/CDC.txt): customer registration, authentication, profiles, carts, product browsing/search/sorting, checkout, order/package information, employee product management, About Us, and contacting the shop. The discussion extended the scope to stock tracking, protected cart prices, refunds, cancellations, partial shipments, and support through a contact form, displayed email, and staffed call center. An AI chatbot is deferred and is outside the current scope.

Expected scale is several thousand products, up to 1,000 users, and 30,000 requests per day. Peak traffic and concurrent-user counts remain unspecified. A small team using managed infrastructure is a planning assumption, not a confirmed staffing or hosting commitment.

The main architectural priority is correct handling of stock, orders, and payments. Concurrent purchases must not oversell stock, and catalogue price changes must not alter prices already held in carts or orders. We should use established relational DBMS transaction and constraint mechanisms while explicitly implementing business invariants and retry behavior.

Other requirements are:

- **Security:** two-factor authentication, customer ownership checks, employee permissions, secure handling of customer data, and auditable sensitive changes. The authentication mechanism is deferred.
- **Performance:** p95 API response time at most 200 ms. Peak-load conditions and whether asynchronous acceptance is sufficient for external operations still require agreement and testing.
- **Availability:** at least 99.9% availability measured over each calendar month. This replaces the earlier daily target and separate 30-minute monthly downtime limit. Unaffected functions should remain usable during external-provider outages.
- **Durability:** no loss of acknowledged saved changes after an individual database server failure or the failure of one availability zone (RPO = 0 for these scenarios). This includes saved carts, orders, stock changes, and recorded payment/refund outcomes. Use synchronous database replication across independent availability zones within one hosting region, with safe failover. Protection against failure of the entire hosting region is outside the required scope because its additional cost and complexity are disproportionate to this service.

## Decision

**Use a modular monolith with a shared ACID relational database, replicated application instances, and separate background workers, because it keeps CDC's core stock and order changes within one transaction boundary while minimizing implementation and operational complexity at the expected scale.**

Maintain internal boundaries for identity/profile, catalogue, carts, inventory/orders, payments/refunds, shipments, and support. In a short checkout transaction, reserve stock atomically, create the order using stored cart prices, and persist pending work in an outbox. Workers contact external providers after commit; idempotent requests, verified callbacks, and reconciliation handle payment uncertainty. External payment is not part of the local database transaction.

Deploy redundant application instances across independent availability zones within one region. Use a highly available database with synchronous replication across those zones: acknowledge a successful write only after the required durable copies have been recorded. Safe failover must preserve acknowledged writes and prevent the former primary from continuing to accept writes after a replacement is promoted. If the required replication or safe failover cannot be established, temporarily reject or pause writes rather than acknowledge changes without the agreed protection. Select and test a topology that supports recovery from a single-zone failure within the monthly availability target; entire-region protection is not required.

Isolate slow integrations from API capacity. Validate latency, security, failover, and recovery before claiming the non-functional targets. The architecture is accepted; the following implementation stack is a concrete recommendation for discussion. The hosting provider remains unspecified.

### Implementation proposal

Proposed stack:

| Component | Technology | Purpose |
| --- | --- | --- |
| Frontend | React SPA + TypeScript | Customer and employee interfaces |
| Backend | FastAPI | Modular API and business logic |
| Database | PostgreSQL | Persistent data and ACID transactions |
| Database tooling | SQLAlchemy + Alembic | Database access and schema migrations |
| Background jobs | Python worker + database outbox | Payment, shipping, and email processing |
| Deployment | API replicas + PostgreSQL across availability zones | Redundancy, synchronous replication, and safe failover |

## Alternatives Considered

### Option A ✓: Modular monolith with background workers

One modular backend release uses a shared transactional database, with multiple runtime replicas and separate workers.

**Pros:** straightforward core transactions, short internal call paths, simpler deployment, testing, and auditing.

**Cons:** shared releases and database resources can affect several modules, modules cannot be independently scaled, and boundaries require discipline to prevent coupling. High availability and external-payment recovery still require deliberate engineering.

This option best matches the agreed priority of correctness and manageable complexity.

### Option B: Domain microservices

Independently deployed catalogue, cart, inventory, order, payment, shipment, and support services own their data.

**Pros:** independent scaling and releases, finer service-level isolation.

**Cons:** cross-service checkout needs coordinated recovery and compensation, with more network calls, event contracts, access policies, and operational tooling. Local ACID transactions remain possible, but cross-service business consistency is harder to implement and verify.

These costs are not justified by CDC's current scale or team assumptions.

### Option C: Serverless APIs and managed workflows with a shared transactional database

Functions handle requests and managed workflows coordinate external operations.

**Pros:** preserves local ACID transactions, provides elastic compute, and reduces server administration.

**Cons:** initialization latency, concurrency limits, database connection management, workflow retries, and platform-specific configuration complicate predictable performance and troubleshooting.

It is a viable alternative, but offers less benefit for CDC than the simpler selected deployment.

## Score Matrix

Scores from the Task 1 discussion: **1 = poor fit / high effort; 5 = excellent fit / low effort**. Higher is better for every criterion. Weights reflect CDC's emphasis on transaction correctness. These are architectural judgments for the assumed small team, not measured results.

| Criterion | Weight | A: Monolith | B: Microservices | C: Serverless + shared DB |
| --- | ---: | ---: | ---: | ---: |
| Ease of ensuring transaction correctness | 30% | 5 | 2 | 5 |
| Predictable API performance | 15% | 5 | 3 | 4 |
| Deployment simplicity | 10% | 5 | 2 | 4 |
| Implementation simplicity | 15% | 5 | 2 | 4 |
| Maintenance and operational simplicity | 10% | 4 | 2 | 3 |
| Ease of securing and auditing | 10% | 4 | 3 | 4 |
| Availability and recovery feasibility | 10% | 4 | 4 | 4 |
| **Weighted score / 5** | **100%** | **4.70** | **2.45** | **4.20** |

Weighted score = sum of each score multiplied by its percentage weight, divided by 100. Security, availability, and durability remain mandatory acceptance criteria regardless of the total. The modular monolith ranks highest because it combines a shared transaction boundary with the lowest implementation and operational complexity for CDC.
