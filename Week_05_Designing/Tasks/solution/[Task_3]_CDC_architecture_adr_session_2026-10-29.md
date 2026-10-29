# CDC architecture and ADR discussion

Date: 2026-10-29 (Europe/Bratislava)

This file records actual user and assistant exchanges, with assistant messages summarized. It will be extended as the discussion continues. Proposed assumptions are not accepted requirements or decisions.

## Exchange 1 — Request and initial clarification

### User

> Hi! I need to design an architecture for the following project - Week_05_Designing\Tasks\data\CDC.txt.
>
> Try to use the architecture-adr skill to accomplish the task.
>
> Record our conversation and write it to solutions folder. But do not use Week_05_Designing\Tasks\solution[Task_1]_CDC_architecture_discussion.md and Week_05_Designing\Tasks\solution[Task_2]_CDC_ADR_discussion.md

### Assistant

- Read `../data/CDC.txt`, the task assignments, applicable repository instructions, and `architecture-adr/SKILL.md`.
- Found and applied the requested architecture-adr skill. Used the existing `solution` directory for this new conversation record.
- Did not read or modify the two excluded discussion files. No previous architecture choice was imported into this session.
- Identified CDC as a distributed hardware shop system handling product management, payment, and shipment. The brief specifies 25 user stories but no load, latency, availability, recovery, team, budget, or hosting constraints.
- Explained the next step: clarify decisive constraints, then compare three architectures and their trade-offs using a weighted matrix. The skill requires user acceptance of an option before writing an ADR.
- Asked the four questions reproduced below. No answers have been received yet.

### Initial questions

1. Is this a course prototype or a production shop, and what team size, technology, hosting, or budget constraints should shape the design?
2. What load and responsiveness should we plan for: approximate simultaneous users or peak requests, product count, and any response-time target? Estimates or “choose reasonable assumptions” are sufficient.
3. How much downtime and loss of saved orders are acceptable? Should saved orders survive a server failure, an entire hosting-zone failure, or an entire-region failure?
4. Is this one shop with merchant staff or a marketplace with independent sellers? Should payment and shipping use real external providers or be simulated?

## Confirmed requirement coverage baseline

These groups account for every story in CDC.txt; they are functional areas, not accepted service or deployment boundaries.

| Functional area | Story IDs | Required behavior |
| --- | --- | --- |
| Accounts and profiles | 1, 2, 3, 8, 13, 14, 19 | Customer registration; customer and merchant login, profile access, and logout |
| Product browsing | 5, 6, 11, 12, 17, 18, 21, 22 | List products, view details, search by name, sort by ascending or descending price |
| Product administration | 15, 16 | Merchant changes prices and inserts or removes products |
| Cart and checkout | 4, 7, 24, 25 | View cart, add a product, clear all items, and pay for the cart |
| Order and package information | 9 | Customer checks their order and package information |
| Shop information and contact | 10, 20, 23 | About Us access and a way for customers to contact the shop |

Shipment management appears in the system description, but carrier integration and shipment operations are not detailed in the stories. Inventory quantities, reservations, refunds, guest checkout, and multiple sellers are not explicit requirements and must not be silently treated as confirmed scope.

## Decision state

- Accepted architecture: none.
- Accepted nonfunctional targets: none supplied.
- Architecture alternatives and weighted scores: pending the initial constraints discussion.
- ADR: not yet created. The skill states: “Wait for the user to accept an option before creating an ADR; a recommendation is not acceptance.”
- Next step: use the user's answers, or explicitly authorized assumptions, to present three concrete alternatives with deployment boundaries, data ownership, checkout failure handling, and a weighted comparison.

## Exchange 2 — Production requirements

### User

> 1. IMO it's a hardware shop with merchant employees
> 2. Yes, customer are from one geographical region, we are working in Slovakia. Let's say we need to handle several thousands of products, up to 1000 users, and several dozens of thousands requests
> 3. I mean API response
> 4. Let's say Daily on average. Yes, other services should be available. Available downtime: 30 minutes/month. No data loss is acceptable.
> 5. Of course we must track stock. Prices shouldn'y change while customer is ordering and having the product in a cart. Delays are acceptable. Refunds etc. are in scope
> 6. Two-factor authentication is needed, but I won't tell you enough about the implementation details for now. Contact the shop = contact form + ability to write an email to some displayed address, or communicate to AI chatbot/call center (if workers are available)
> 7. We consider porudction service. Suggest a reasonable assumption
> 8. Survive a whole hosting-zone failure

### Assistant

- Identified checkout correctness and recovery from one hosting-zone failure as central design drivers.
- Asked whether cart prices remain fixed indefinitely or may expire after 24 hours with explicit customer acceptance of a new price. Stated that the unlimited guarantee would be preserved unless the user chose a limit.
- Asked whether the initial comparison could use 1,000 simultaneous users, 50,000 API requests/day, a provisional peak of 100 requests/second, and p95 API responses within 500 ms for ordinary reads and writes, with payment/shipping completion measured separately.
- Explained the provisional preference for a replicated modular monolith with separate workers, while also comparing a service-based architecture and finer-grained microservices. Explained that backups alone do not meet zero acknowledged data loss across a zone failure.

## Exchange 3 — Price guarantee and corrected workload

### User

In response to the cart-price question:

> Fixed while it remains in the cart

In response to the proposed workload and response-time targets:

> p95 200 ms, 30000 requests/day, up to 1000 users/day

### Assistant

Confirmed the corrected targets in chat and separated unknown peak traffic from daily averages. Presented the three alternatives and weighted comparison summarized below. These remain proposals; the user has not selected an architecture.

### Current requirements and assumptions

| Item | Current state |
| --- | --- |
| Business | Confirmed: one hardware shop, merchant employees, customers in Slovakia, production service |
| Catalog and usage | Confirmed: several thousand products, 30,000 requests/day on average, up to 1,000 users/day. Daily users are not simultaneous users. Average request rate is approximately 0.35/second; peak rate and concurrent sessions remain unknown. |
| Latency | Confirmed: API p95 of 200 ms. Proposed measurement: API ingress to response, separately for each ordinary read/write endpoint under the agreed load; include checkout acceptance and synchronous durable writes, but measure external payment/shipping completion separately. This boundary is not an exclusion for slow ordinary writes. |
| Availability | Confirmed: at most 30 minutes downtime/month; unrelated services remain available when a dependency fails. In a 30-day month, 30 minutes corresponds to approximately 99.9306%. The explicit monthly downtime cap remains authoritative. Proposed measurement: each critical customer journey, including degraded-operation checks. |
| Durability | Confirmed: no acknowledged business-data loss on loss of one entire hosting zone, including saved carts, locked prices, stock changes, orders, refund records, and accepted contact submissions. Zero-loss recovery from an entire-region failure is not required by the agreed failure scope. |
| Commerce | Confirmed additions: stock tracking, price fixed while an item remains in a cart and during ordering, refunds. Delays are acceptable. Return/cancellation details still need business rules; they are not assumed to be exhaustively specified by “etc.” |
| Security | Confirmed: two-factor authentication. Implementation details deferred by user. Proposed baseline: customer/merchant permissions, resource ownership checks, audited staff changes, encrypted transport/storage, secrets management, no raw card storage. |
| Contact | Confirmed: contact form and displayed email, with AI chatbot/call-center contact as described by the user. Proposed support boundary accommodates both channels; exact channel combination and staffing/handoff behavior remain open. |
| Delivery assumptions | Proposed: four engineers with shared operational responsibility, managed hosting in one European region spanning three zones, real payment and shipping providers, moderate budget. No provider or implementation stack selected. |
| Validation assumptions | Proposed only: initial stress envelope of 100 requests/second, revised from measured traffic; zone failover recovery objective of five minutes, fitting within the cumulative 30-minute monthly budget. Neither is a newly confirmed requirement. |

The 500 ms, 50,000 requests/day, and 1,000 simultaneous-user suggestions were superseded by the user's correction and must not be used as accepted targets.

### Common correctness, resilience, and security design

- Store the server-authoritative unit price with each cart line and copy it into the order; merchant price edits affect new additions, not existing cart lines. Proposed quantity rule: additional units added later form a new price snapshot; existing quantities keep their price. Removal and re-addition uses the current price. This quantity rule is a proposal, not a user decision. Archive removed products so order history remains readable.
- A fixed price does not reserve stock indefinitely. Propose reservation at checkout, with atomic conditional stock updates and an explicit reservation lifecycle. Cart additions must not promise availability. Failed payments release stock; uncertain outcomes require reconciliation before release or shipment. Late payment after release must reacquire stock safely or enter a refund/exception workflow.
- Freeze cart version, quantities, prices, and order totals during checkout. Duplicate submissions reuse the same durable checkout identifier. Prevent concurrent checkout of the same cart version from allocating twice.
- Write order, stock reservation, payment-work intent, and durable outbox entry in one local transaction where boundaries allow. The outbox is a stored list of work committed with the business change. In microservices, each owner commits its own state and outbox; a durable workflow coordinates reservations and compensations.
- Use stable payment/refund operation keys, signed callback verification, an inbox with duplicate detection, valid state transitions, and periodic reconciliation with the provider. Do not claim exactly-once external effects or a database transaction spanning a provider. After the provider's idempotency-retention window, query/reconcile the existing operation rather than blindly repeating a charge.
- Refunds have their own durable state and authorization. Concurrent refunds cannot exceed the paid amount minus already successful or pending refunds. Return acceptance, refund completion, and restocking are distinct actions; stock is not automatically increased just because money is refunded.
- Across all options, place API capacity in multiple zones and require synchronously durable database commits across zones, safe promotion of a node containing committed data, and fencing of the old writer. For queues and accepted work, use equivalent durability or reconstruct from the durable outbox. Never silently downgrade to asynchronous acknowledgement if cross-zone durability is unavailable. Provision enough surviving capacity to tolerate one zone loss.
- Use three-zone placement to support recovery while a zone is absent. Require proof of the selected database deployment's commit and failover semantics; simply labeling it multi-zone is insufficient. Backups with restore exercises additionally address corruption and operator mistakes.
- Timeouts, bounded connection pools, separate worker pools, retry backoff, and circuit breakers keep slow integrations from consuming API capacity. Display payment/shipping pending states honestly. Payment completion cannot be promised while the provider is down; browsing, cart access, and order-status access continue. Identity outages can prevent new login, and database quorum loss can block durable writes; no architecture eliminates these dependencies.
- Enforce two-factor authentication without choosing its implementation yet. Check customer ownership on every cart/order access, restrict merchant operations, and audit stock/price/refund changes. Support AI gets no authority to charge, refund, or change stock; any access to customer data is narrowly authorized. Contact forms persist before acknowledgement; email delivery and chatbot availability are separate downstream concerns.

### Three alternatives presented in chat

#### A — Replicated modular monolith with background workers

One application contains accounts, catalog, cart, stock, orders, payment/refund coordination, shipment tracking, and support modules. Deploy stateless API replicas and separately scaled worker processes across zones. Workers and API share the same application release and one highly available relational database; modules own their tables. External identity, payment, shipping, email, chatbot, and call-center systems remain separate. This is a distributed deployment despite one main application boundary.

Checkout commits the cart version, order snapshot, stock reservation, payment intent, and outbox work in one local transaction. Workers call providers and update status in later transactions. A payment-provider failure leaves a durable pending order and does not hold a database transaction open across the network.

**Pros:** simplest local enforcement of commerce invariants; few internal network hops for the 200 ms API target; straightforward deployment, debugging, and maintenance for the assumed small team. Replicas and isolated worker capacity support zone and provider-failure recovery.

**Cons:** shared database and application releases increase the impact of defects; internal module failures are less isolated than separate services. Requires disciplined module boundaries, safe migrations, resource limits, database operations, and multi-zone baseline spending. Shared-database failure can affect many shop functions.

#### B — Commerce core plus independent integration and support services

Deploy three coarse services: Commerce Core (catalog, carts, stock, orders), Integration Service (payment/refund attempts, provider references, shipments), and Support Service (contact cases and chat/call handoffs). Each owns its database; services communicate through durable events and explicit APIs, with no cross-service table writes. Replicate each critical service and store across zones.

Checkout atomically reserves stock and stores an order plus outbox entry in the Commerce Core. The Integration Service deduplicates the request, calls the provider, and publishes outcomes; the core updates order state. On integration failure, the core retains pending work and retries delivery. Each service keeps its own inbox/outbox. The core authorizes refundable amounts atomically; integrations execute the authorized operations.

**Pros:** preserves local stock/order transactions while isolating support and external-provider code; independent deployment and worker scaling; can suit separate teams or frequently changing integrations.

**Cons:** more databases, deployments, monitoring, event contracts, and reconciliation; order and integration views can temporarily disagree. Shared managed infrastructure can still fail together. Higher implementation, maintenance, and fixed operating cost than A for the assumed team.

#### C — Domain microservices with a durable checkout workflow

Separate Catalog, Cart, Inventory, Order, Payment/Refund, Fulfillment, and Support services own independent stores. Use an API gateway, a durable event broker, and a persistent checkout coordinator; no shared mutable tables. Each critical store and runtime needs zone resilience.

Checkout freezes the cart and price snapshot, requests an idempotent stock reservation from Inventory, records the resulting order state, and then schedules payment. A durable workflow coordinates these local transactions. Failed steps trigger explicit compensation, such as releasing stock or issuing a refund. A local database transaction cannot atomically commit the complete checkout across all services.

**Pros:** strongest deployment and resource isolation; domain teams can evolve independently; suitable if organizational scale or separate subsystem workloads later justify it.

**Cons:** greatest implementation and operational burden; more network paths threaten the 200 ms budget; distributed state machines, tracing, message evolution, and consistency problems increase maintenance. More individual stores and queues must meet zero-loss requirements. Service separation alone does not establish uptime or correctness.

### Functional coverage across the alternatives

| Functional requirement | A | B | C |
| --- | --- | --- | --- |
| Accounts/profile: 1, 2, 3, 8, 13, 14, 19; two-factor authentication | Account module and identity provider | Core account module and identity provider | Account service and identity provider |
| Product browsing: 5, 6, 11, 12, 17, 18, 21, 22; administration: 15, 16 | Catalog module | Commerce Core | Catalog service |
| Cart/checkout: 4, 7, 24, 25; fixed prices and stock | Cart, Stock, Order, Payment modules | Commerce Core and Integration Service | Cart, Inventory, Order, Payment services and coordinator |
| Order/package information: 9; shipment management | Order and Shipment modules | Core order view fed by Integration Service | Order and Fulfillment services |
| About Us: 10, 20 | Static content | Static content | Static content |
| Contact: 23; form, email, AI/call-center channels | Support module with isolated workers | Support Service | Support service |
| Added refunds/returns | Order, Payment, Stock modules | Core authorization; integrations execute refunds | Order/Payment/Inventory workflow |

### Failure scenario used to explain trade-offs

Two customers try to buy the last item. A and B use an atomic stock reservation with order creation in the commerce database; only one succeeds. C makes Inventory the sole authority, with an idempotent reservation and a durable workflow waiting for its result. A cart price guarantee never overrides stock availability.

After successful reservation, the payment provider charges the customer, but the worker crashes before saving the result. Every option must recover the same payment attempt via a stable operation key, callback or provider-status lookup, and reconciliation. Until the outcome is known, retain a pending/unknown state; do not create a new charge, release stock blindly, or ship on the strength of a browser redirect. A commits the recovered outcome and order transition locally; B and C must also deliver and deduplicate the outcome across service boundaries. No option has an atomic transaction with the external provider.

### Weighted comparison presented in chat

Weights are proposed from the user's emphasis on correctness, durability, uptime, and latency, with delivery and maintenance weighted for the assumed small team. Scores are reasoned judgments, not benchmarks: 1 = poor fit/high effort; 5 = excellent fit/low effort. Weighted score = sum(score * percentage weight) / 100.

| Criterion | Weight | A | B | C |
| --- | ---: | ---: | ---: | ---: |
| Stock, locked-price, payment and refund correctness | 30% | 5 | 5 | 3 |
| Zone recovery and zero-loss implementation effort | 20% | 4 | 4 | 3 |
| Implementation and deployment simplicity | 15% | 5 | 3 | 1 |
| Maintenance and operating cost | 15% | 5 | 3 | 2 |
| Failure isolation and independent evolution | 10% | 3 | 4 | 5 |
| Predictable p95 API latency | 10% | 4 | 4 | 3 |
| **Weighted total** | **100%** | **4.50** | **4.00** | **2.75** |

Mandatory security, durability, and availability conditions remain pass/fail gates. A high score does not excuse failure. B retains A's local commerce transactions and improves isolation, but adds distributed integration state. C's low correctness/recovery scores indicate extra engineering effort, not intrinsic impossibility. No architecture's score is a performance or availability guarantee.

### Recommendation, validation, and decision state

Recommend A provisionally: at 30,000 daily requests, distribution into many services is not justified by the average load alone; A preserves strong local commerce transactions and can run across zones. Prefer B if independently deploying integrations/support becomes a firm requirement. Prefer C if independently staffed domain teams and measured scaling needs justify its coordination cost.

Before acceptance of production readiness: measure per-endpoint p95 under realistic bursts, concurrent last-item checkout, cart price edits, and refunds; inject a zone loss immediately after acknowledged writes and verify no lost business records plus recovery within the proposed five minutes; test duplicate/out-of-order callbacks, worker crashes after external success, exhausted retries and reconciliation; test provider outages while measuring unaffected customer journeys; verify ownership/role checks and two-factor enforcement; restore backups. No implementation or performance testing has occurred in this design discussion.

Open details: actual peak traffic, exact API measurement boundary and external-completion service objectives, approved team/budget, added-quantity pricing, reservation/cancellation/return policies, support-channel combination, and provider selection. The agreed zone-loss scope and indefinite existing-cart price guarantee do not need reopening.

The assistant asked whether the user accepts A or prefers B's independent integration/support deployment despite its additional complexity. No architecture is accepted yet. Following `architecture-adr/SKILL.md`, an ADR will be written only after acceptance; this file remains a discussion record.

### Primary documentation consulted

- [PostgreSQL synchronous replication and standby documentation](https://www.postgresql.org/docs/current/warm-standby.html): asynchronous replication can lose acknowledged updates; synchronous durability and appropriate failover need deliberate configuration. This informs the topology requirements; PostgreSQL is not yet a selected implementation.
- [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests): stable keys support retries, but their retention is bounded. A provider's idempotency feature does not remove the need for persistent operation state and reconciliation. Stripe is an example, not a selected provider.
- [Stripe webhook documentation](https://docs.stripe.com/webhooks): supports the proposed callback verification and duplicate/out-of-order event handling. Provider selection remains open.

## Exchange 4 — Architecture acceptance and scope changes

### User

> Okay, I agree with you. Option A seems to be the best one!
>
> Some notes:
>
> - AI chatbot section could be left out for now. We do not need this for now
> - 99.9% calendar-month availability target

### Assistant

Confirmed that an ADR would be written for accepted option A, with AI chatbot excluded from current scope. Explained that 99.9% permits 43.2 minutes downtime in a 30-day month and asked whether this target replaces the earlier 30-minute cap or whether both should apply. Continued preparing the architecture record while awaiting that clarification.

## Exchange 5 — Availability clarification and ADR delivery

### User

In response to whether 99.9% should replace the earlier downtime cap:

> Replace the 30-minute cap with 99.9%

### Assistant

Confirmed that 99.9% calendar-month availability replaces the 30-minute cap. Created [ADR-002: Replicated modular monolith for CDC shop](CDC_ADR-002_replicated_modular_monolith.md), using the next unused ADR identifier based on existing filenames. The previous ADR and excluded discussion files were not read or modified.

The ADR records accepted option A, its deployment and transaction boundaries, a diagram, coverage of all 25 original stories, added stock/price/refund/security requirements, alternatives A/B/C in their original order, and the weighted comparison. AI chatbot is explicitly out of scope; contact form, displayed email, and staffed contact remain. The selected architecture is distinguished from proposed implementation assumptions and production validation work.

### Current decision state — supersedes earlier provisional state

- Architecture: **A accepted** by the user.
- Availability: **99.9% per calendar month**; the earlier 30-minute cap is superseded, not an additional constraint.
- AI chatbot: **out of current scope**.
- Retained requirements: p95 API response time 200 ms; 30,000 requests/day; up to 1,000 users/day; several thousand products; no acknowledged business-data loss after one hosting-zone failure; indefinite existing-cart price guarantee; stock, refunds, two-factor authentication, shipment tracking, and non-chatbot contact channels.
- Open implementation details: peak traffic, measurement boundaries, provider choices, precise deployment topology, budget/team assumptions, added-quantity pricing and reservation/return/cancellation policies.
- Artifact: accepted architecture ADR written; no application implemented or production readiness claimed.
- Historical exchanges above retain the assumptions and requirements that applied at the time; the current ADR uses the corrected scope and availability target.

Document checks confirmed coverage of all 25 original story IDs, weights totaling 100%, weighted totals A = 4.50 / B = 4.00 / C = 2.75, valid local source/discussion links, and both requested scope corrections. These were document consistency checks, not application or infrastructure tests.

## Exchange 6 — User's Task 3 report

### User

Asked to translate their supplied Russian evaluation into English and write it to `[Task_3]_report.md`, preserving their wording and opinions with only light paragraph formatting. Their evaluation praises the requirements discussion, three alternatives, Mermaid diagram, and requirement mapping; notes the missing implementation libraries; and expresses a slight preference for the earlier ADR and a desire to shorten the additional Decision subsections.

### Assistant

Translated the supplied evaluation into four English paragraphs and wrote it to [the Task 3 report](%5BTask_3%5D_report.md). Preserved the user's subjective assessment without independently comparing the excluded discussions or changing the ADR or skill.
