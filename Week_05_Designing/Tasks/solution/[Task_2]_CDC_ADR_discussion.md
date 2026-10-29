# Task 2: CDC Architecture Decision Record Discussion

Date started: 2026-10-28

## Purpose

Record the conversation and ADR revisions required by [Task 2](../Task_2.md). These are discussion notes rather than a verbatim transcript. The Task 1 record is retained unchanged.

ADR artifact: [ADR-001: Use a Modular Monolith for CDC](%5BTask_2%5D_ADR-001.md).

Prior discussion: [Task 1 architecture discussion](%5BTask_1%5D_CDC_architecture_discussion.md).

## Round 1: requested structure and first draft

### User request

- Stop adding to the Task 1 discussion file.
- Start a new discussion based on Task_2.md and record it in a new file in the solution folder.
- First create ADR-001 with exactly these main sections: Context, Decision, and Alternatives Considered.
- Describe three alternatives, with Option C marked as the winning choice.

### Assistant response and work

The assistant read Task_2.md and the conclusion of the existing Task 1 record. Task 2 calls for both a conversation record and an ADR, followed by user inspection and iterative refinement.

The assistant created the separate ADR and this discussion record. The initial ADR preserves the user's selected modular monolith architecture and confirmed traffic of 30,000 requests/day. It summarizes the original functional scope, added business requirements, and security, performance, availability, and durability targets.

The Decision section gives one explicit architecture decision and explains the core transaction boundary, background processing, and production redundancy. The alternatives cover microservices, serverless with a shared transactional database, and the selected modular monolith. Their labels were reordered from Task 1 so that the winning monolith is Option C, as requested; the architecture choice itself did not change.

Unresolved details remain visibly unresolved: peak traffic, concurrency, exact availability measurement, regional disaster scope, asynchronous completion semantics, and vendor/authentication choices. The draft does not imply that performance or availability has already been verified.

The assistant used the requested three-section structure without adding a score matrix, diagram, or additional ADR sections. The Task 1 discussion file was not edited.

### Review status

Initial ADR draft created for user inspection. The architecture direction was already selected in Task 1; the user has not yet reviewed or approved this ADR's wording and level of detail. No revision requests or approvals have been invented. Future Task 2 discussion and changes will be recorded here.

## Round 2: restore the original alternative order

The user clarified that the alternatives should retain the order from Task 1: Monolith (accepted), Microservices, Serverless. This clarification supersedes the first draft's interpretation of the example template placing the winner under Option C.

The assistant reordered and relabeled the ADR alternatives as follows:

- **Option A ✓:** Modular monolith with background workers (accepted).
- **Option B:** Domain microservices.
- **Option C:** Serverless APIs and managed workflows with a shared transactional database.

The descriptions, trade-offs, and architecture decision are unchanged. The Task 1 record was not edited. The ADR remains open to further user review.

## Round 3: support scope, monthly availability, and durability clarification

### User feedback

- An AI chatbot is not needed for now.
- Change availability to 99.9% measured over a calendar month.
- Explain what still needs to be agreed about durability; the previous wording was unclear.

### Changes made

The assistant deferred the AI chatbot and removed it from the current implementation scope. The contact form, displayed email address, and staffed call center remain in scope.

The ADR now specifies at least 99.9% availability in each calendar month. This replaces both the earlier daily measurement and the separate 30-minute monthly cap. Under a time-based calculation, a 30-day month permits 43 minutes 12 seconds of downtime at 99.9%; the allowance changes with the month's duration.

The durability requirement was rewritten in plain language: a saved change acknowledged by the service must survive a failure. The user's zero-data-loss requirement has not been relaxed.

### Explanation provided

The unresolved issue is the set of disasters the system must survive, not whether losing orders is acceptable. A confirmed order must remain recorded after a database server crashes. Preserving it if every hosting location in a region is destroyed additionally requires a durable copy outside that region before acknowledging the save. A temporary regional outage can instead leave data intact but unavailable; availability and durability are different properties.

Synchronous replication waits for the required replica acknowledgement; asynchronous replication can leave a window in which recent changes have not reached the surviving copy. See [PostgreSQL replication documentation](https://www.postgresql.org/docs/current/warm-standby.html). Geographic placement, failover safety, cost, and write latency therefore depend on the protected failure scenarios. Backups also help recover accidental deletion, which can propagate to live replicas.

The assistant asked whether protection must include losing every hosting location in the chosen region, or server/single-location failures. No answer or narrowing of the zero-data-loss scope is assumed. The selected architecture remains a modular monolith; the deployment and recovery design will depend on this clarification. The Task 1 record remains unchanged.

## Round 4: agreed durability scope and replication strategy

The user chose protection against individual server and availability-zone failures, using synchronous database replication across independent availability zones with safe failover. Entire hosting-region failure is excluded from the required protection because the additional complexity and expense are not justified for CDC.

The assistant updated the ADR's Context and Decision sections accordingly. The durability scope is now resolved: RPO = 0 means no acknowledged saved changes may be lost under the agreed server or single-zone failure scenarios. The deployment uses one region with multiple independent availability zones; the exact provider and topology remain implementation choices.

The Decision section makes safe failover concrete: preserve acknowledged writes and prevent the old primary from accepting writes after another primary is promoted. If the required replication or safe failover is unavailable, writes must pause or fail rather than silently lose their durability protection. The topology and failover process must be tested against the 99.9% calendar-month availability target; this editing task does not establish that the target has been achieved.

The assistant recorded the user's cost and complexity rationale. The modular monolith remains the accepted architecture, the AI chatbot remains deferred, and the original Task 1 record was not edited. The ADR is updated for further review; this clarification does not imply blanket approval of all remaining details.

## Round 5: concrete implementation section and stack recommendation

### User request and clarification

The user questioned keeping the ADR entirely independent of frameworks and database choices. They suggested React SPA + FastAPI + PostgreSQL as an example and requested help choosing suitable technologies. When asked whether they wanted an ADR implementation section or a runnable prototype, the user explicitly selected **an implementation section in the ADR**. Application-code implementation is therefore outside this turn's scope.

### Assistant recommendation and changes

The assistant added an Implementation proposal subsection under Decision, preserving the three main ADR sections and the architecture-alternative order: Monolith (accepted), Microservices, Serverless. The previous blanket statement that no framework or DBMS choice was made was replaced with an explicit distinction between the accepted architecture and the proposed stack.

The concrete proposal is React + TypeScript with Vite, FastAPI, PostgreSQL, SQLAlchemy, Alembic, and a separate Python worker processing a durable PostgreSQL outbox. It assumes team familiarity with Python and JavaScript/TypeScript, which has not been confirmed. No technology choice is represented as user-approved. The section maps components to responsibilities and follows one checkout through authentication, cart ownership/idempotency checks, stock reservation, order creation, outbox insertion, payment processing, and status retrieval.

The assistant compared the proposal with Django + PostgreSQL, explaining Django's built-in ORM, employee admin, and account/session/permission facilities. Django could reduce custom administrative implementation; FastAPI is a reasonable choice for an explicit API and custom React screens. Neither framework automatically provides the application's transaction correctness or all required security controls. Exact MFA implementation remains deferred.

A client-only SPA is also a provisional frontend choice. The section recommends evaluating server rendering or static generation if product discoverability and initial rendering matter. React frontend deployment does not imply backend microservices.

The section also explains durable worker recovery, bounded database connections, server-authoritative prices, exact monetary representation, security responsibilities, and the difference between local containers and production cross-zone HA. The API may acknowledge a checkout as pending, but the earlier open question about this response contract remains unresolved.

Official React, FastAPI, SQLAlchemy, Alembic, and Django documentation supports the technology comparison and is linked in the ADR. No benchmark or prototype was run, and the 200 ms and availability targets are not claimed as achieved. The Task 1 record was not changed.

## Round 6: shorten the implementation section

The user clarified that the implementation section should be much smaller. The assistant replaced the lengthy proposal with one compact paragraph naming React SPA with TypeScript, FastAPI, PostgreSQL, SQLAlchemy, Alembic, and a separate worker using a durable database outbox. The detailed table, walkthrough, framework comparison, and documentation links were removed from that section. The proposed status of the stack and the rest of the ADR remain unchanged.

## Round 7: present the compact implementation proposal as a table

The user preferred a table. The assistant converted the compact paragraph into a six-row table listing component, technology, and purpose, preserving the short scope and proposed technology choices.

## Round 8: separate alternative paragraphs and add the score matrix

The user requested separate paragraphs for the alternatives' descriptions, pros, and cons, and a Score Matrix section immediately after Alternatives Considered.

The assistant gave each alternative its own subheading and separated its description, pros, cons, and assessment into paragraphs. The original order and accepted monolith were preserved. A Score Matrix section was added using the Task 1 criteria, weights, and scores: monolith 4.70/5, microservices 2.45/5, and serverless with a shared database 4.20/5. The section explains the scoring scale and weighted calculation and distinguishes judgments from measurements. Security, availability, and durability remain mandatory regardless of the score.

The compact implementation table and the Task 1 record were left unchanged.
