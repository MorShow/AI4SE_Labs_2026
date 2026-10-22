# PINES Management Processes and Reporting Requirements

Reporting and management tools for library staff, managers, and administrators, including collection, capacity, patron, transaction, and financial analysis and related operational capabilities. Day-to-day patron-facing OPAC and circulation functions are outside this scope. The supplied Galecia draft and Evergreen reference are treated as context and input to refinement, not as automatic approval of every proposal they contain.

## Priority Scale

Business priority is shown next to every requirement:

- **High:** essential/core operation, an explicit critical request, or a source-supported mandatory constraint.
- **Medium:** important improvement with a viable workaround.
- **Low:** optional convenience or enhancement.

**Overall priority** combines business priority with the developer perspective on feasibility, complexity, technical risk and readiness:

- **High:** warrants strong development focus given business value and technical impact.
- **Medium:** worthwhile development work, with moderate overall urgency or readiness.
- **Low:** optional or deferrable work with limited overall urgency.

Priority levels do not prescribe an implementation sequence.

## Functional Requirements

<a id="fr-001"></a>

### FR-001 — Material volume reporting

**Business priority:** High · **Overall priority:** High

Provide material-volume reports for a selected library and point in time. Cover new acquisitions, items on the shelf (checked in), and items out in circulation (checked out); the discussion requests the three counts separately as well as a total. Allow breakdowns including total items, holds, adult fiction, board books, and other customizable categories. The sources do not specify the historical-data mechanism or the full category list.

**Business priority rationale:** Inferred High: multiple stakeholders identify this as a key reporting need for board reporting, assessment, and collection management.

**Overall priority rationale:** Retaining High is justified: multiple stakeholder sources explicitly identify material-volume reporting at a given time (acquisitions, shelf, and in-circulation) with key category breakdowns as a core board/collection-management need. Implementation is non-trivial due to historical snapshot requirements, but the business value and explicitness support High focus.

<a id="fr-002"></a>

### FR-002 — Branch capacity overview and analysis

**Business priority:** High · **Overall priority:** High

Provide an overview of capacity across all branches, with the ability to drill down to an individual branch, sort and filter by region, library type, and current load, show growth or shrink trends, and export capacity information to CSV. The source does not define the measures that constitute capacity, the trend period, or export fields; the capacity measure remains an open specification decision and must not be assumed by this requirement.

**Business priority rationale:** Inferred High: managers describe cross-branch capacity visibility as needed for moving items and allocating resources.

**Overall priority rationale:** Retaining High is justified: the sources call for an organization-wide capacity overview with drill-down, sorting/filtering, trends, and CSV export, and they explicitly note that capacity metrics need to be decided before building. This is operationally critical for allocating resources across branches, despite some open specification details.

<a id="fr-004"></a>

### FR-004 — Shelf-space and collection-use report

**Business priority:** High · **Overall priority:** High

For each material genre and format, compare the percentage of total circulations, percentage of the collection, and percentage of total shelf space. Make the report available per library and per system, support filtering by date range, and provide a side-by-side library comparison view. Shelf space is not directly tracked; the sources mention dimensions or item count as possible estimation approaches but do not choose one.

**Business priority rationale:** Inferred High: stakeholders describe the report as important for collection management, resource allocation, and quarterly review.

**Overall priority rationale:** Retaining High is justified: stakeholders explicitly request a shelf-space vs. circulation vs. collection-percentage comparison with filtering and side-by-side library comparisons, and it is framed as important for collection/resource decisions. The main technical risk is that “shelf space” is not directly tracked, but the business impact supports High.

<a id="fr-005"></a>

### FR-005 — Batch item transfers

**Business priority:** High · **Overall priority:** High

Provide a utility to transfer batches of items between branches and temporary destinations such as mobile libraries, outreach programs, warehouses, special programs, book sales, or events. Support querying candidate materials, saving queries for reuse, manually selecting titles from query results, and changing selected items' locations to the destination. The examples of query criteria and destinations illustrate use and do not restrict the utility's scope.

**Business priority rationale:** Inferred High: cataloging staff describe batch transfers as crucial and recurring, with collection balancing and special programs as use cases.

**Overall priority rationale:** Retaining High is justified: batch transfers (including candidate querying, saved queries, manual selection, and location changes) are described as crucial and recurring for staff workflows. Technical risk is moderate, but the operational importance and explicit scope support High.

<a id="fr-006"></a>

### FR-006 — Transfer materials and labels

**Business priority:** Medium · **Overall priority:** Medium

Support transfer preparation by generating pull lists and printable transit labels, including printable barcodes as an example. The sources do not specify label content, format, or pull-list layout.

**Business priority rationale:** Inferred Medium: these are useful operational aids to the requested transfer workflow, with other ways of coordinating a transfer available.

**Overall priority rationale:** Keeping Medium aligns with the source framing: pull lists and printable transit labels are requested as part of the transfer preparation workflow, but they are not positioned as the core mechanism compared to the overall batch transfer capability. There are practical alternatives, supporting Medium.

<a id="fr-007"></a>

### FR-007 — Revert temporary item transfers

**Business priority:** Medium · **Overall priority:** Medium

Support returning transferred items to their original location after a set period or when another criterion is met. Discussed examples include time-based return after a book sale or event and status-based reversion; the source does not define a universal period or complete set of criteria. The proposed behavior for items checked out at the destination conflicts within the discussion and is not resolved here.

**Business priority rationale:** Inferred Medium: temporary transfers need a return mechanism, but the required triggers and handling of checked-out items need clarification.

**Overall priority rationale:** Keeping Medium matches the evidence: reversion of temporary transfers is requested, but the sources contain unresolved conflicts/uncertainty (e.g., checked-out items at the destination). Because the required triggers/handling are not settled, it is important but not essential until clarified.

<a id="fr-008"></a>

### FR-008 — Transfer preview, undo, permissions, and history

**Business priority:** High · **Overall priority:** High

Before applying a transfer, show a preview that identifies the proposed item count and source and destination locations, and provide an undo function for accidental actions. Restrict transfer capability to authorized roles; managers, administrators, and transfer coordinators are examples, not a definitive role list. Track transfer history so users can review an item's transfers, including counts over a period; retention and detailed history fields are unspecified.

**Business priority rationale:** Inferred High: the preview, authorization, and history requests support safe, accountable changes; undo was requested to correct mistakes.

**Overall priority rationale:** Retaining High is justified: preview, authorization/role restriction, undo support, and transfer history are explicitly requested to make batch/location changes safe and auditable. Even with implementation complexity (history/undo/permissions), the safety/accountability value supports High.

<a id="fr-009"></a>

### FR-009 — Transfer delay alerts

**Business priority:** Low · **Overall priority:** Low

Notify the requester when a transfer is delayed or has issues. The sources do not specify the alert channel, timing, or detailed recipient rules.

**Business priority rationale:** Inferred Low: alerts are an optional convenience; the core transfer workflow can operate without them.

**Overall priority rationale:** Keeping Low is reasonable: transfer-delay alerts are described as helpful/optional convenience rather than a prerequisite for completing transfers. The core workflow remains usable without them, so limited urgency supports Low.

<a id="fr-010"></a>

### FR-010 — Missing and damaged item report

**Business priority:** High · **Overall priority:** High

Provide reports of missing and damaged items per branch for inventory audits, collection management, and accountability. Include item condition notes, such as water damage or vandalism, when available to help users understand causes.

**Business priority rationale:** Inferred High: multiple stakeholders identify this report as needed for monthly audits, collection management, and branch accountability.

**Overall priority rationale:** Retaining High is justified: missing and damaged item reporting per branch is repeatedly identified as necessary for inventory audits, collection management, and accountability, with condition notes (e.g., water damage/vandalism) when available. The reporting is operationally critical despite some data-availability variability.

<a id="fr-011"></a>

### FR-011 — Long-running in-transit report

**Business priority:** High · **Overall priority:** High

Generate one report combining transit-to and transit-from items that have been in transit longer than a configurable number of days. Support per-branch and per-system views and sorting by due date so staff can pursue the oldest items first. Seven days was suggested as a possible default, but the consolidated request does not confirm a default.

**Business priority rationale:** Inferred High: stakeholders describe the report as critical for delivery coordination and for investigating lost items.

**Overall priority rationale:** Retaining High is justified: a long-running in-transit report (merging transit-to and transit-from beyond configurable days) is positioned as critical for delivery coordination and finding potentially lost items, with sorting by due date. Complexity is manageable, but the business urgency is strong.

<a id="fr-012"></a>

### FR-012 — Purge candidate identification and status conversion

**Business priority:** High · **Overall priority:** High

Provide reports and a utility to identify item records for purging using customizable, combinable criteria, including status, time in status, and time since last circulation. Examples include missing, discard/weed, and damaged statuses and specified inactivity periods; these example thresholds are not fixed defaults. Also provide a report or associated capability to assist with batch conversion from one item status to another.

**Business priority rationale:** Inferred High: cataloging staff describe weeding and batch status conversion as frequent, time-consuming work.

**Overall priority rationale:** Retaining High is justified: weeding/purging candidate identification with customizable combinable criteria (status duration, time since last circulation, etc.) and assistance for batch status conversion is described as frequent and time-consuming. High priority fits the operational burden and the explicit functional scope.

<a id="fr-013"></a>

### FR-013 — Safeguards for purging

**Business priority:** High · **Overall priority:** High

Keep purge-candidate reports read-only, require a separate confirmation step before actual deletions, and maintain an audit trail for all purges that records who purged what and when. The sources do not settle whether candidate-identification and deletion operations can be scheduled.

**Business priority rationale:** Inferred High: stakeholders explicitly request safeguards to prevent accidental deletion and for accountability and troubleshooting.

**Overall priority rationale:** Retaining High is justified: safeguards for purging (read-only candidate reports, explicit confirmation before deletion, and an audit trail recording who/what/when) are explicitly requested to prevent accidental data loss and support accountability. These are safety-critical constraints.

<a id="fr-014"></a>

### FR-014 — Last-copy reports by scope

**Business priority:** High · **Overall priority:** High

Provide a last-copy report that flags items that are the only copy within a selected scope, with both per-library and system-wide views. The system-wide view is specifically needed to avoid deleting the consortium's last copy. Support catalogers' WorldCat update work; the sources request reports to assist that work, not a WorldCat integration.

**Business priority rationale:** Explicit High: stakeholders call the last-copy report critical and describe the risk of accidentally deleting a rare book's only copy.

**Overall priority rationale:** Retaining High is justified: the last-copy report is described as critical to avoid the severe risk of deleting the consortium’s only copy of a rare book, including both per-library and system-wide views. This is a clear core safety requirement.

<a id="fr-015"></a>

### FR-015 — Cleanup of orphaned records

**Business priority:** Medium · **Overall priority:** Medium

Provide a method to delete volume entries together with their copy entries and to delete records with no attached items. The source asks for a quick, effective method but does not decide whether the cleanup is manual or automated.

**Business priority rationale:** Inferred Medium: catalogers identify the cleanup as necessary and time-consuming, but it is subordinate to the core reporting and last-copy safeguards.

**Overall priority rationale:** Keeping Medium is appropriate: orphaned-record cleanup is described as a quick/effective method but is subordinate to the more critical last-copy safeguards and core purging/reporting protections. Open choices (manual vs automated) further support Medium.

<a id="fr-016"></a>

### FR-016 — Track and report deletions

**Business priority:** High · **Overall priority:** High

Count and track successful record deletions, including item, patron, and bibliographic records where applicable, per location and per system. Retain record type, deletion time, deleting user, and the user's location, and provide reports that can aggregate by date range, user, and record type, including totals by period, type, and location and users with the most deletions. The source mentions deletion reason or prior status only tentatively, so it is not required here.

**Business priority rationale:** Inferred High: stakeholders identify deletion tracking as important for audits, accountability, troubleshooting, and retention reporting.

**Overall priority rationale:** Retaining High is justified: tracking deletions with counts and detailed audit fields (record type, timestamp, deleting user, location) supports audits, accountability, and troubleshooting. The functional scope is broad but directly tied to compliance and operational correctness.

<a id="fr-017"></a>

### FR-017 — Report denied deletion attempts

**Business priority:** Low · **Overall priority:** Low

Support tracking denied deletion attempts as a helpful capability for compliance and troubleshooting. The source raises this as a request and calls it helpful, rather than establishing it as a mandatory part of successful-deletion logging.

**Business priority rationale:** Inferred Low: the source describes this as helpful, and it is supplementary to tracking completed deletions.

**Overall priority rationale:** Keeping Low fits the source: denied-deletion attempt tracking is described as “helpful” for compliance/troubleshooting, but it is supplementary to tracking successful deletions. With limited explicit mandate, Low is the correct overall focus.

<a id="fr-018"></a>

### FR-018 — Patron characteristic reporting

**Business priority:** High · **Overall priority:** High

Allow patron queries and reports to be limited and grouped by age range, ZIP code, county of residence, home branch, patron type, and preferred language. Support combining filters with AND and OR logic, configuring age brackets per report, and including records with missing values as nulls rather than silently excluding them. More generally, report results must preserve null values and blank fields, including when fields are filtered or displayed; the sources do not prescribe how such values should be grouped or formatted.

**Business priority rationale:** Inferred High: stakeholders describe demographic reports as essential for program planning and collection decisions, and complete results help avoid misleading reports.

**Overall priority rationale:** Retaining High is justified: patron demographic reporting with grouped/limited queries, AND/OR filter logic, configurable age brackets, and explicit inclusion of null/missing values is framed as essential for program planning and avoiding misleading reports. Preserving nulls adds implementation care but supports High.

<a id="fr-019"></a>

### FR-019 — Inactive patron report

**Business priority:** High · **Overall priority:** High

Generate a list of patrons with no circulation or specified electronic activity during a configurable number of days. Treat OPAC or patron-account login, online hold placement, and online renewal as electronic activity; include access to digital collections only when integrated and logged. Support system, home-library, county, and other needed scopes; include current mailing addresses; distinguish inactive patrons with outstanding fines; allow exclusion of selected patrons such as staff or communication opt-outs; and provide CSV export. A 365-day period is commonly used but is not confirmed as a default.

**Business priority rationale:** Inferred High: stakeholders use this report for database cleanup and outreach, and the source lists multiple required filters and handling conditions.

**Overall priority rationale:** Retaining High is justified: the inactive patron report includes multiple required scopes and conditions (no circulation/electronic activity, electronic activity definition, fines distinctions, exclusions, mailing addresses, and CSV export). The breadth of required correct filtering/handling makes it high-value and high priority.

<a id="fr-020"></a>

### FR-020 — Uncataloged material inventory and circulation

**Business priority:** Medium · **Overall priority:** Medium

Support inventory tracking for uncataloged material, including paperback books and children's board books, without requiring individual catalog records. Support quick distribution with minimal branch labor, identify how the material is used, and count its transactions in circulation statistics and reports.

**Business priority rationale:** Inferred Medium: the need is specific to uncataloged material workflows, but the source does not establish it as a system-wide critical operation.

**Overall priority rationale:** Keeping Medium is consistent with the evidence: uncataloged material inventory/circulation is operationally important for specific workflows (paperback/board books without individual catalog records) but not presented as a system-wide core operation compared to the more explicitly mandatory reporting/safety capabilities.

<a id="fr-021"></a>

### FR-021 — Transaction and circulation activity reports

**Business priority:** High · **Overall priority:** High

Provide transaction reports that can group activity by hour, terminal, branch, and system, and report totals per patron, library, group of libraries, system, and county where specified. Count check-ins separately and cumulatively by book drop, terminal, and user or self-service; count check-outs and renewals by the staff, self-service, online, and OPAC types identified in the survey; and report holds placed and filled with their placement channel (staff desk, public computer, or remote). The source does not specify additional report families or detailed definitions beyond these stated dimensions and types.

**Business priority rationale:** Inferred High: survey respondents report frequent use of circulation reports and identify specific transaction breakdowns and scopes needed for operations.

**Overall priority rationale:** Retaining High is justified: transaction/circulation activity reports are repeatedly emphasized as frequently used, with explicit breakdowns (time/hour, terminal, branch/system, check-in/out/renewal types, holds placement/fill channels, and patron/library scope). This aligns closely with core operations monitoring.

<a id="fr-022"></a>

### FR-022 — Patron behavior and material-use statistics

**Business priority:** Medium · **Overall priority:** Medium

Provide statistics that help users understand patron behavior and use of materials. Source examples include average return time for a particular book, likelihood of renewal, the share of branch check-outs that are renewals, and renewal rates; no prediction method or accuracy target is specified.

**Business priority rationale:** Inferred Medium: useful for collection and service planning, but the sources do not establish predictive measures or thresholds as core operations.

**Overall priority rationale:** Keeping Medium matches the source: the report set is described as helpful for understanding behavior/use with example metrics (return time, renewal likelihood/rates), but the sources do not define prediction methods or accuracy targets as core operational requirements. Useful, but not clearly essential or fully specified.

<a id="fr-023"></a>

### FR-023 — Financial and item-value reporting

**Business priority:** High · **Overall priority:** High

Provide reports of item values based on item-record data for the entire collection or a portion, including examples such as longoverdue items and children's DVDs. Provide financial reports for patron balances by patron, home library, and system; accrued fines and charges by time period and charge type; waived fines by period and branch; and payments by period, collecting library, collection channel, and tender type. Allow staff to query accounts above a specified balance threshold and join relevant patron and item financial data. The source describes reflecting front-desk payments immediately and tracking financial information as requested capabilities.

**Business priority rationale:** Inferred High: finance stakeholders request reporting for reconciliation and budget oversight; the sources identify specific report dimensions and a payment-update need.

**Overall priority rationale:** Retaining High is justified: finance reporting (item values, patron balances, fines/charges, waived fines, payments by period/method/tender, and threshold queries) is explicitly oriented to reconciliation and budget oversight, with additional correctness needs (e.g., front-desk payments reflected immediately). Strong business impact supports High.

<a id="fr-024"></a>

### FR-024 — Payment-to-charge ledger

**Business priority:** High · **Overall priority:** High

Maintain a ledger of patron payments that identifies the specific charge or charges to which each payment was applied, to support account reconciliation. The source identifies this audit trail as critical but does not specify retention periods or a detailed ledger format.

**Business priority rationale:** Explicit High: a finance stakeholder calls the payment audit trail critical and says reconciliation depends on tracing payments to charges.

**Overall priority rationale:** Retaining High is justified: the payment-to-charge ledger is explicitly described as critical for reconciliation via traceability of each payment to the specific charges applied. This is an audit-grade accounting integrity requirement.

<a id="fr-025"></a>

### FR-025 — Report templates and query tools

**Business priority:** High · **Overall priority:** High

Provide a user-friendly query-design interface for the record types named in the sources, allowing field selection, picklist values, regular-expression selection, and Boolean operators, with administrators controlling access to tables and fields. Allow administrators to create templates for staff to run as-is or modify, limit which filters and display fields can be changed, and support cloning an existing template into a separate variant. Preserve the intended accuracy and consistency of templates; the sources do not define a quantitative accuracy measure.

**Business priority rationale:** Inferred High: the survey ranks templates and query features prominently, and stakeholders request reusable, controlled reporting.

**Overall priority rationale:** Retaining High is justified: query/design tools with templates (field selection, picklists, regex selection, Boolean logic, administrator-controlled access, and cloning/variants) are requested as reusable controlled reporting infrastructure. This has significant usability/compliance implications and is indicated as prominent in the sources.

<a id="fr-026"></a>

### FR-026 — Report permissions and shared access

**Business priority:** High · **Overall priority:** High

Provide fine-grained, easily administered permissions governing who can create, clone, and run reports and who can run ad hoc reports against specified data sets. Support shared folders or equivalent report access groupings and administer permissions through roles so that role changes update report permissions. Transfer permissions are covered separately.

**Business priority rationale:** Inferred High: permissions are repeatedly described as essential to controlling access to reports and data.

**Overall priority rationale:** Retaining High is justified: fine-grained permissions and shared access for creating/cloning/running reports and running ad hoc reports are explicitly needed for access control. The ability for role changes to update permissions is also directly supported by the sources, making High appropriate.

<a id="fr-027"></a>

### FR-027 — Staff authentication options

**Business priority:** Medium · **Overall priority:** Medium

Support individual username-and-password login and an optional streamlined staff login method, such as employee-ID card swipe. The streamlined method must not be required, and every method must identify and authenticate the individual staff member for audit purposes.

**Business priority rationale:** Inferred Medium: faster staff access is a requested improvement, while preserving traditional login and individual accountability are explicit conditions.

**Overall priority rationale:** Keeping Medium is appropriate: staff authentication options (username/password plus optional streamlined card swipe) are an improvement for usability and speed, while the sources explicitly require individual accountability and non-bypass authentication. Because it is not framed as core reporting functionality, Medium fits.

<a id="fr-028"></a>

### FR-028 — Predefined board and executive reports

**Business priority:** High · **Overall priority:** High

Provide predefined reports for library boards and other external consumers, including basic statistics associated in the source with Georgia Annual Report requirements. Activity reports should include check-outs, check-ins, holds placed, and holds filled, with the cross-tabulation dimensions specified in FR-021. The named reports are examples; the sources do not supply their complete detailed specifications.

**Business priority rationale:** Inferred High: stakeholders identify board and executive reporting as needed for formal reporting and planning.

**Overall priority rationale:** Retaining High is justified: predefined board/executive reports are explicitly requested, including activity reports (check-outs/check-ins/holds placed/filled) and associated basic statistics. These are formal reporting obligations and thus high business value.

<a id="fr-029"></a>

### FR-029 — Report queue visibility and prioritization

**Business priority:** Medium · **Overall priority:** Medium

Allow staff to see whether a report is queued, how many reports are ahead of it, its submission time, and its status as waiting, running, completed, or failed. Support prioritizing important reports so they can move ahead of lower-priority work; no specific priority levels or policy are defined.

**Business priority rationale:** Inferred Medium: queue visibility addresses staff confusion and support calls; prioritization is requested for important reports but has no defined policy.

**Overall priority rationale:** Keeping Medium is consistent: queue visibility and prioritization address operational pain points (staff confusion/support calls) but are not described as a critical correctness/safety dependency. Prioritization policy is unspecified, supporting Medium.

<a id="fr-030"></a>

### FR-030 — Report scheduling, cancellation, and delivery

**Business priority:** Medium · **Overall priority:** Medium

Support running reports immediately or scheduling them on available recurring intervals, including hourly, daily, weekly, monthly, and yearly where applicable. Allow cancellation of scheduled or running reports. Support Excel, HTML, and CSV output and report delivery by email. The sources do not require every report to support every interval or define email delivery details.

**Business priority rationale:** Inferred Medium: scheduling, cancellation, and delivery are useful workflow improvements, while manual report execution remains a workaround.

**Overall priority rationale:** Keeping Medium aligns with the sources: scheduling/cancellation and multi-format delivery (including email) are workflow improvements, with manual execution acting as a workable alternative. The sources do not require every interval detail for every report, supporting Medium urgency.

<a id="fr-031"></a>

### FR-031 — Historical and real-time reporting

**Business priority:** Medium · **Overall priority:** Medium

Support reporting on current data where needed and reporting on data as of a specified past date or date range, including historical bills and values that may have changed since that date. The sources do not specify retention duration, a timeliness threshold for real-time reporting, or a mandatory storage architecture.

**Business priority rationale:** Inferred Medium: stakeholders request historical comparisons and some current-state reports, but no time or retention thresholds are established.

**Overall priority rationale:** Keeping Medium is appropriate: historical and real-time reporting is requested (past-date snapshots, current-state, and historical bill values), but the sources do not provide retention/timeliness thresholds or mandatory architecture. Value is clear, but uncertainty and lack of quantified constraints keep priority at Medium.

<a id="fr-032"></a>

### FR-032 — Report criteria and context

**Business priority:** Medium · **Overall priority:** Medium

Show the query selections or criteria used to generate results. For reports with date selection, include the selected date criteria and report name with the results. The sources do not prescribe exact placement or presentation beyond identifying that users should be able to see the criteria.

**Business priority rationale:** Inferred Medium: showing criteria improves interpretability and reproducibility, while it does not prevent a report from running.

**Overall priority rationale:** Keeping Medium is appropriate: showing report criteria/context improves interpretability and reproducibility, but it is not described as mission-critical to accomplishing reporting objectives. Medium matches its supportive nature.

<a id="fr-033"></a>

### FR-033 — Survey-requested report presentation details

**Business priority:** Medium · **Overall priority:** Medium

Address the survey-reported need to avoid excessive duplicate rows in Excel exports, make fields that users expect available for report filtering, present requested MARC fields together when they are otherwise spread across rows, and provide pivot-table output. The sources identify these needs but do not specify deduplication rules, the complete field list, or a detailed output contract.

**Business priority rationale:** Inferred Medium: these capabilities address reported difficulties with report use and output, but the sources do not identify them as essential operations.

**Overall priority rationale:** Keeping Medium is justified: presentation details such as reducing duplicate rows in Excel exports, ensuring expected filter fields, MARC field grouping, and pivot-table output are driven by reported usability issues. However, sources do not characterize them as essential core operations, so Medium fits.

<a id="fr-034"></a>

### FR-034 — Item date reporting distinctions

**Business priority:** Medium · **Overall priority:** Medium

Support displaying the last circulation date on item reports and distinguish check-in date/time from renewals. Reports should also show an item's last edit date as an item edit date, not as a date updated by its last circulation. The sources do not specify additional item report families or a detailed date-field format.

**Business priority rationale:** Inferred Medium: these distinctions support collection and item analysis, but no source states a critical priority or a measurable performance target.

**Overall priority rationale:** Keeping Medium is reasonable: distinguishing last circulation date, check-in vs renewals, and last edit date improves data analysis correctness, but the sources do not establish a criticality level or measurable performance target. Medium is consistent with the evidence.

<a id="fr-036"></a>

### FR-036 — Online help and error feedback

**Business priority:** Medium · **Overall priority:** Medium

Provide online, hierarchical, cross-linked HTML help that describes and illustrates system functions and is searchable and easy to navigate. Provide high-level error reporting and feedback, plus low-level query-specific feedback for Local and Global System Administrators; when a report fails, useful details include the table, field, and kind of error rather than only a generic failure message.

**Business priority rationale:** Inferred Medium: help and actionable errors reduce staff dependence on support, but the sources do not state these as core business operations.

**Overall priority rationale:** Keeping Medium aligns with source framing: online hierarchical cross-linked help and actionable error feedback for administrators reduce support dependency, but the sources do not position these as core business operations. Medium fits the improvement/enablement nature.

## Non-Functional Requirements

<a id="nfr-001"></a>

### NFR-001 — Non-disruptive operation at consortium scale

**Business priority:** High · **Overall priority:** High

Support the stated consortium scale of 286 locations, 17 million annual circulations, and purchasing and processing over 900,000 items per year. Searches and reports should be processable during open hours without disrupting other system functions, including circulation and OPAC access. Background processing or queuing and read-only reporting replicas are discussed as alternatives, not as simultaneous mandatory implementation choices; no response-time threshold is specified.

**Business priority rationale:** Inferred High: the scale is an explicit system constraint and the sources identify disruption of live library operations as a major concern.

**Overall priority rationale:** Retaining High is justified: consortium scale is an explicit system constraint, and the sources stress non-disruption of live circulation/OPAC access during open hours. This is a major technical risk area, making High appropriate.

<a id="nfr-002"></a>

### NFR-002 — Relational data compatibility

**Business priority:** Medium · **Overall priority:** Medium

Use and work with a fully relational database structure. The sources identify PostgreSQL as the current database, but do not require that product specifically. A technical participant recommends against denormalization and prefers keeping data in the main database; that preference does not establish a prohibition on a separate reporting store.

**Business priority rationale:** Inferred Medium: relational compatibility is an explicit technical constraint, but the sources do not designate a particular database product.

**Overall priority rationale:** Keeping Medium is appropriate: relational data compatibility is explicitly required (fully relational backend; PostgreSQL identified as current) but does not mandate a specific separate reporting store, and some recommendations (e.g., against denormalization) are not absolute prohibitions. Medium reflects constraint importance without over-specifying technology.

<a id="nfr-003"></a>

### NFR-003 — Accessible reporting and assistive technology

**Business priority:** High · **Overall priority:** High

Make the reporting system accessible to screen readers, screen-magnification software, and other assistive technologies. The sysadmin interview calls Section 508 compliance non-negotiable and names JAWS, NVDA, and ZoomText as examples; the source does not specify a conformance testing method.

**Business priority rationale:** Explicit High: the sysadmin interview describes accessibility as a non-negotiable legal requirement for a public institution.

**Overall priority rationale:** Retaining High is justified: accessibility for screen readers and related assistive technologies is described as a non-negotiable legal requirement, with examples like JAWS/NVDA/ZoomText. This is both explicit and high-impact.

<a id="nfr-004"></a>

### NFR-004 — Standards-compliant HTML

**Business priority:** High · **Overall priority:** High

Produce standards-compliant HTML for web-based interfaces, help, and report output. The technical notes call for validation against W3C standards and identify semantic HTML, alt text, and ARIA labels as accessibility-related examples; the named details are grounded in the sysadmin interview and should not be interpreted as a complete conformance specification.

**Business priority rationale:** Inferred High: compliant HTML is stated as a system constraint and supports browser compatibility and accessibility.

**Overall priority rationale:** Retaining High is justified: standards-compliant HTML (including semantic structure, alt text, and ARIA labels) and validation against standards are stated as system constraints with accessibility relevance. This is important and directly tied to NFR-003.

<a id="nfr-005"></a>

### NFR-005 — Protect OPAC availability

**Business priority:** High · **Overall priority:** High

Management reporting must not constrain OPAC functionality or slow down patron access to the public catalog. This is a separate protection for the existing OPAC; it does not add day-to-day patron-facing functions to the reporting system.

**Business priority rationale:** Inferred High: the sources explicitly state that reporting must not affect patron access or OPAC functionality.

**Overall priority rationale:** Retaining High is justified: protecting OPAC availability and ensuring report execution does not slow patron access is explicitly required. This is a safety/non-disruption constraint for the public-facing service, supporting High priority.

<a id="nfr-006"></a>

### NFR-006 — Supported server operating systems

**Business priority:** Medium · **Overall priority:** Medium

Operate on Linux or Solaris servers. The sources identify these as supported server environments but do not establish a requirement for particular hardware or operating-system versions.

**Business priority rationale:** Inferred Medium: these are explicit deployment constraints needed to support the stated library environment.

**Overall priority rationale:** Keeping Medium is appropriate: supported server OS environments (Linux or Solaris) are explicit deployment constraints, but no version-level detail or broad business mandate beyond compatibility is provided. Medium fits as a necessary but not user-visible operational feature.

<a id="nfr-007"></a>

### NFR-007 — Safe training environment

**Business priority:** Medium · **Overall priority:** Medium

The training environment must allow staff to practice and experiment without risking production data. The source does not specify how environment separation or data isolation must be implemented.

**Business priority rationale:** Inferred Medium: the sysadmin identifies training safety as needed to prevent staff mistakes, while it is not part of everyday reporting behavior.

**Overall priority rationale:** Keeping Medium is reasonable: a safe training environment is described as needed to prevent staff mistakes and enable practice without risking production data, but it is not part of day-to-day reporting functionality. Medium supports it as important but deferrable relative to core operational requirements.

<a id="nfr-008"></a>

### NFR-008 — Anonymized demographic statistics

**Business priority:** High · **Overall priority:** High

When producing demographic statistics, include analysis such as transactions by geographic region and age range while removing information that could identify a patron from the data used. The sources do not define a specific anonymization technique or re-identification threshold.

**Business priority rationale:** Inferred High: the draft and survey explicitly require anonymization to protect patron privacy while retaining useful statistics.

**Overall priority rationale:** Retaining High is justified: anonymized demographic statistics are explicitly required to protect patron privacy while still enabling useful analysis by geography and age range. Privacy risk and compliance implications justify High.

## Interface Requirements

<a id="ir-001"></a>

### IR-001 — User access channels

**Business priority:** Medium · **Overall priority:** Medium

Make Management Processes accessible either through a web browser or a Windows-compatible client. If a browser-based channel is used, support Internet Explorer 6.0 or later and Firefox 2.0 or later as specified in the source. These are access obligations; they do not prescribe a particular user-interface design.

**Business priority rationale:** Inferred Medium: access through the stated channels is needed for the library environments represented in the sources.

**Overall priority rationale:** Keeping Medium is appropriate: access via web browser or Windows-compatible client with specific browser minimum versions is an integration/interface obligation, but it is not inherently more valuable than other reporting functions. Medium fits as necessary compatibility rather than core value.

<a id="ir-002"></a>

### IR-002 — Vendor data exchange

**Business priority:** Medium · **Overall priority:** Medium

Where vendor data exchange is used, support interfaces with vendor websites through published APIs and/or automated transfer of standard-format data files; USMARC21 and EDIFACT are examples given by the source. Vendor data may not be available at every library, and no specific vendor, API contract, or file exchange details are supplied.

**Business priority rationale:** Inferred Medium: the source describes vendor data exchange as a dependency for some libraries, but does not establish universal availability or a specific contract.

**Overall priority rationale:** Keeping Medium is reasonable: vendor data exchange interfaces (APIs/standard files like USMARC21/EDIFACT) are a dependency for some libraries, with no universal availability or specific contract. Medium matches the conditional nature.

<a id="ir-003"></a>

### IR-003 — Report output and export formats

**Business priority:** Medium · **Overall priority:** Medium

Allow report output in Excel, HTML, and CSV formats. Enable CSV export where specifically requested for capacity and inactive-patron reporting. The sources do not specify a formatting contract, and an address book for regularly used email recipients was mentioned as desirable rather than mandatory.

**Business priority rationale:** Inferred Medium: multiple sources request these output formats for staff and director use, with CSV especially identified for export.

**Overall priority rationale:** Keeping Medium is justified: Excel/HTML/CSV output and CSV export where specifically requested are important usability/export requirements, but no conformance contract is described beyond these examples. Medium reflects value without clear evidence of being core correctness/safety.

## Additional Requirements (Operational, Legal and Deployment)

<a id="ar-001"></a>

### AR-001 — Development, training, and production environments

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Deployment

Provide separate development and training environments, with production kept distinct. Allow configurations developed in development or training to be migrated to production through export and import, including report templates, permission settings, saved queries, and other configuration. The sources do not prescribe environment count beyond these named environments or a migration mechanism beyond export/import.

**Business priority rationale:** Inferred Medium: sysadmin and meeting sources state the environments and configuration migration are needed, but do not identify them as core user-facing operations.

**Overall priority rationale:** Keeping Medium matches the evidence: separate development/training environments and config migration to production (via export/import of templates/permissions/saved queries) are operationally important for delivery quality but not a user-facing reporting capability; sources support it as a supporting obligation.

<a id="ar-002"></a>

### AR-002 — Management-process documentation

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Operational

Provide complete data specifications for authority, bibliographic, order, item, hold/request, and other records maintained or accessed by Management Processes. Also provide high-level descriptions of major processes, including bibliographic import and export, validation against internal and external authority sources, and standard reports. These are documentation obligations; they do not establish that the reporting system itself performs acquisitions, cataloging, or authority validation.

**Business priority rationale:** Inferred Medium: staff need the documentation to understand data and processes, but it is not a direct reporting operation.

**Overall priority rationale:** Keeping Medium is appropriate: management-process documentation and complete data specifications/process descriptions support correct understanding and operations, but they are not direct runtime reporting functions. Medium priority fits supporting but non-core behavior.

<a id="ar-003"></a>

### AR-003 — Management-process scope and interfaces

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Other

Keep Management Processes focused on reports and analysis for library staff, managers, and administrators; day-to-day patron-facing OPAC and circulation functions remain outside this scope. The sources describe reliance on the enterprise library automation system, read access to its data, and possible vendor data exchange through published APIs or standard-format files such as USMARC21 or EDIFACT. Vendor data may not be available at every library, and no specific vendor contract is supplied.

**Business priority rationale:** Inferred Medium: this records the project boundary and relevant dependencies rather than a core user-facing feature.

**Overall priority rationale:** Keeping Medium aligns with source framing: management-process scope and interface boundaries (focus on reports/analysis; day-to-day patron-facing functions remain outside scope; reliance on enterprise ILS data) are important for project boundaries, but they primarily constrain scope rather than add core reporting value.

<a id="ar-004"></a>

### AR-004 — Reporting service deployment

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Deployment

The source describes Management Processes as centrally consolidated and serving multiple locations. It also calls for separating reporting from production operations, but does not choose an architecture or resolve whether a separate reporting database, replica, or another approach will be used. Preserve this as a deployment obligation and open design decision rather than assuming a specific implementation.

**Business priority rationale:** Inferred Medium: multi-location service and separation from production are important operating constraints, but the sources leave the deployment approach open.

**Overall priority rationale:** Keeping Medium is justified: reporting service deployment is described as centralized/multi-location with separation from production, but the mechanism is explicitly left open. This reduces certainty and makes it important but not the highest business priority.

<a id="ar-005"></a>

### AR-005 — Accounting and audit compliance

**Business priority:** High · **Overall priority:** High

**Type:** Legal

Reports and data archiving must comply with standard accounting practice and applicable state, county, and municipal auditing requirements. The source does not identify specific practices or jurisdictional rules; it also says some data may need seven-year retention but does not identify which data or establish that duration for all data.

**Business priority rationale:** Inferred High: the sources state a mandatory compliance constraint for financial reports and archiving, although the applicable detailed rules remain unspecified.

**Overall priority rationale:** Retaining High is justified: accounting/audit compliance for reports and data archiving is explicitly mandated, with some retention duration discussed. Even though jurisdictional details are not fully specified, compliance is high business impact.

<a id="ar-006"></a>

### AR-006 — Privacy-preserving transaction retention

**Business priority:** High · **Overall priority:** High

**Type:** Legal

Archive transaction data for the retention period required by applicable law while protecting patron privacy and retaining useful demographic statistics. The sources describe the legal period as “X years” in one discussion and mention seven years for some unspecified audit data in another; they do not establish one universal period or a specific anonymization method. Monthly and annual aggregate retention indefinitely and configurable transaction-history retention are addressed separately in AR-007.

**Business priority rationale:** Inferred High: sources identify legal retention and patron privacy obligations, but the duration and records covered require clarification.

**Overall priority rationale:** Retaining High is justified: legal transaction retention while protecting patron privacy is explicitly described, even though duration/covered records are not fully settled. Privacy and legal compliance risks justify High.

<a id="ar-007"></a>

### AR-007 — Transaction history and aggregate retention

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Operational

Maintain transaction history for a configurable number of days and retain monthly and annual aggregate information indefinitely. The sources do not specify the configurable history duration. This operational retention behavior is separate from applicable legal retention and privacy obligations, whose duration and covered records remain unresolved.

**Business priority rationale:** Inferred Medium: the survey summary identifies this as a key requirement, but the configurable history duration is unspecified and the sources provide no explicit business priority.

**Overall priority rationale:** Keeping Medium is consistent: transaction-history configurable retention and indefinite monthly/annual aggregates are specified, but the configurable history duration is unresolved and the sources do not establish strong business priority beyond the survey framing. Medium is appropriate.

## Overall Priority List

| Requirement | Business priority | Overall priority | Developer rationale |
| --- | --- | --- | --- |
| [FR-001](#fr-001) | High | High | Retaining High is justified: multiple stakeholder sources explicitly identify material-volume reporting at a given time (acquisitions, shelf, and in-circulation) with key category breakdowns as a core board/collection-management need. Implementation is non-trivial due to historical snapshot requirements, but the business value and explicitness support High focus. |
| [FR-002](#fr-002) | High | High | Retaining High is justified: the sources call for an organization-wide capacity overview with drill-down, sorting/filtering, trends, and CSV export, and they explicitly note that capacity metrics need to be decided before building. This is operationally critical for allocating resources across branches, despite some open specification details. |
| [FR-004](#fr-004) | High | High | Retaining High is justified: stakeholders explicitly request a shelf-space vs. circulation vs. collection-percentage comparison with filtering and side-by-side library comparisons, and it is framed as important for collection/resource decisions. The main technical risk is that “shelf space” is not directly tracked, but the business impact supports High. |
| [FR-005](#fr-005) | High | High | Retaining High is justified: batch transfers (including candidate querying, saved queries, manual selection, and location changes) are described as crucial and recurring for staff workflows. Technical risk is moderate, but the operational importance and explicit scope support High. |
| [FR-006](#fr-006) | Medium | Medium | Keeping Medium aligns with the source framing: pull lists and printable transit labels are requested as part of the transfer preparation workflow, but they are not positioned as the core mechanism compared to the overall batch transfer capability. There are practical alternatives, supporting Medium. |
| [FR-007](#fr-007) | Medium | Medium | Keeping Medium matches the evidence: reversion of temporary transfers is requested, but the sources contain unresolved conflicts/uncertainty (e.g., checked-out items at the destination). Because the required triggers/handling are not settled, it is important but not essential until clarified. |
| [FR-008](#fr-008) | High | High | Retaining High is justified: preview, authorization/role restriction, undo support, and transfer history are explicitly requested to make batch/location changes safe and auditable. Even with implementation complexity (history/undo/permissions), the safety/accountability value supports High. |
| [FR-009](#fr-009) | Low | Low | Keeping Low is reasonable: transfer-delay alerts are described as helpful/optional convenience rather than a prerequisite for completing transfers. The core workflow remains usable without them, so limited urgency supports Low. |
| [FR-010](#fr-010) | High | High | Retaining High is justified: missing and damaged item reporting per branch is repeatedly identified as necessary for inventory audits, collection management, and accountability, with condition notes (e.g., water damage/vandalism) when available. The reporting is operationally critical despite some data-availability variability. |
| [FR-011](#fr-011) | High | High | Retaining High is justified: a long-running in-transit report (merging transit-to and transit-from beyond configurable days) is positioned as critical for delivery coordination and finding potentially lost items, with sorting by due date. Complexity is manageable, but the business urgency is strong. |
| [FR-012](#fr-012) | High | High | Retaining High is justified: weeding/purging candidate identification with customizable combinable criteria (status duration, time since last circulation, etc.) and assistance for batch status conversion is described as frequent and time-consuming. High priority fits the operational burden and the explicit functional scope. |
| [FR-013](#fr-013) | High | High | Retaining High is justified: safeguards for purging (read-only candidate reports, explicit confirmation before deletion, and an audit trail recording who/what/when) are explicitly requested to prevent accidental data loss and support accountability. These are safety-critical constraints. |
| [FR-014](#fr-014) | High | High | Retaining High is justified: the last-copy report is described as critical to avoid the severe risk of deleting the consortium’s only copy of a rare book, including both per-library and system-wide views. This is a clear core safety requirement. |
| [FR-015](#fr-015) | Medium | Medium | Keeping Medium is appropriate: orphaned-record cleanup is described as a quick/effective method but is subordinate to the more critical last-copy safeguards and core purging/reporting protections. Open choices (manual vs automated) further support Medium. |
| [FR-016](#fr-016) | High | High | Retaining High is justified: tracking deletions with counts and detailed audit fields (record type, timestamp, deleting user, location) supports audits, accountability, and troubleshooting. The functional scope is broad but directly tied to compliance and operational correctness. |
| [FR-017](#fr-017) | Low | Low | Keeping Low fits the source: denied-deletion attempt tracking is described as “helpful” for compliance/troubleshooting, but it is supplementary to tracking successful deletions. With limited explicit mandate, Low is the correct overall focus. |
| [FR-018](#fr-018) | High | High | Retaining High is justified: patron demographic reporting with grouped/limited queries, AND/OR filter logic, configurable age brackets, and explicit inclusion of null/missing values is framed as essential for program planning and avoiding misleading reports. Preserving nulls adds implementation care but supports High. |
| [FR-019](#fr-019) | High | High | Retaining High is justified: the inactive patron report includes multiple required scopes and conditions (no circulation/electronic activity, electronic activity definition, fines distinctions, exclusions, mailing addresses, and CSV export). The breadth of required correct filtering/handling makes it high-value and high priority. |
| [FR-020](#fr-020) | Medium | Medium | Keeping Medium is consistent with the evidence: uncataloged material inventory/circulation is operationally important for specific workflows (paperback/board books without individual catalog records) but not presented as a system-wide core operation compared to the more explicitly mandatory reporting/safety capabilities. |
| [FR-021](#fr-021) | High | High | Retaining High is justified: transaction/circulation activity reports are repeatedly emphasized as frequently used, with explicit breakdowns (time/hour, terminal, branch/system, check-in/out/renewal types, holds placement/fill channels, and patron/library scope). This aligns closely with core operations monitoring. |
| [FR-022](#fr-022) | Medium | Medium | Keeping Medium matches the source: the report set is described as helpful for understanding behavior/use with example metrics (return time, renewal likelihood/rates), but the sources do not define prediction methods or accuracy targets as core operational requirements. Useful, but not clearly essential or fully specified. |
| [FR-023](#fr-023) | High | High | Retaining High is justified: finance reporting (item values, patron balances, fines/charges, waived fines, payments by period/method/tender, and threshold queries) is explicitly oriented to reconciliation and budget oversight, with additional correctness needs (e.g., front-desk payments reflected immediately). Strong business impact supports High. |
| [FR-024](#fr-024) | High | High | Retaining High is justified: the payment-to-charge ledger is explicitly described as critical for reconciliation via traceability of each payment to the specific charges applied. This is an audit-grade accounting integrity requirement. |
| [FR-025](#fr-025) | High | High | Retaining High is justified: query/design tools with templates (field selection, picklists, regex selection, Boolean logic, administrator-controlled access, and cloning/variants) are requested as reusable controlled reporting infrastructure. This has significant usability/compliance implications and is indicated as prominent in the sources. |
| [FR-026](#fr-026) | High | High | Retaining High is justified: fine-grained permissions and shared access for creating/cloning/running reports and running ad hoc reports are explicitly needed for access control. The ability for role changes to update permissions is also directly supported by the sources, making High appropriate. |
| [FR-027](#fr-027) | Medium | Medium | Keeping Medium is appropriate: staff authentication options (username/password plus optional streamlined card swipe) are an improvement for usability and speed, while the sources explicitly require individual accountability and non-bypass authentication. Because it is not framed as core reporting functionality, Medium fits. |
| [FR-028](#fr-028) | High | High | Retaining High is justified: predefined board/executive reports are explicitly requested, including activity reports (check-outs/check-ins/holds placed/filled) and associated basic statistics. These are formal reporting obligations and thus high business value. |
| [FR-029](#fr-029) | Medium | Medium | Keeping Medium is consistent: queue visibility and prioritization address operational pain points (staff confusion/support calls) but are not described as a critical correctness/safety dependency. Prioritization policy is unspecified, supporting Medium. |
| [FR-030](#fr-030) | Medium | Medium | Keeping Medium aligns with the sources: scheduling/cancellation and multi-format delivery (including email) are workflow improvements, with manual execution acting as a workable alternative. The sources do not require every interval detail for every report, supporting Medium urgency. |
| [FR-031](#fr-031) | Medium | Medium | Keeping Medium is appropriate: historical and real-time reporting is requested (past-date snapshots, current-state, and historical bill values), but the sources do not provide retention/timeliness thresholds or mandatory architecture. Value is clear, but uncertainty and lack of quantified constraints keep priority at Medium. |
| [FR-032](#fr-032) | Medium | Medium | Keeping Medium is appropriate: showing report criteria/context improves interpretability and reproducibility, but it is not described as mission-critical to accomplishing reporting objectives. Medium matches its supportive nature. |
| [FR-033](#fr-033) | Medium | Medium | Keeping Medium is justified: presentation details such as reducing duplicate rows in Excel exports, ensuring expected filter fields, MARC field grouping, and pivot-table output are driven by reported usability issues. However, sources do not characterize them as essential core operations, so Medium fits. |
| [FR-034](#fr-034) | Medium | Medium | Keeping Medium is reasonable: distinguishing last circulation date, check-in vs renewals, and last edit date improves data analysis correctness, but the sources do not establish a criticality level or measurable performance target. Medium is consistent with the evidence. |
| [FR-036](#fr-036) | Medium | Medium | Keeping Medium aligns with source framing: online hierarchical cross-linked help and actionable error feedback for administrators reduce support dependency, but the sources do not position these as core business operations. Medium fits the improvement/enablement nature. |
| [NFR-001](#nfr-001) | High | High | Retaining High is justified: consortium scale is an explicit system constraint, and the sources stress non-disruption of live circulation/OPAC access during open hours. This is a major technical risk area, making High appropriate. |
| [NFR-002](#nfr-002) | Medium | Medium | Keeping Medium is appropriate: relational data compatibility is explicitly required (fully relational backend; PostgreSQL identified as current) but does not mandate a specific separate reporting store, and some recommendations (e.g., against denormalization) are not absolute prohibitions. Medium reflects constraint importance without over-specifying technology. |
| [NFR-003](#nfr-003) | High | High | Retaining High is justified: accessibility for screen readers and related assistive technologies is described as a non-negotiable legal requirement, with examples like JAWS/NVDA/ZoomText. This is both explicit and high-impact. |
| [NFR-004](#nfr-004) | High | High | Retaining High is justified: standards-compliant HTML (including semantic structure, alt text, and ARIA labels) and validation against standards are stated as system constraints with accessibility relevance. This is important and directly tied to NFR-003. |
| [NFR-005](#nfr-005) | High | High | Retaining High is justified: protecting OPAC availability and ensuring report execution does not slow patron access is explicitly required. This is a safety/non-disruption constraint for the public-facing service, supporting High priority. |
| [NFR-006](#nfr-006) | Medium | Medium | Keeping Medium is appropriate: supported server OS environments (Linux or Solaris) are explicit deployment constraints, but no version-level detail or broad business mandate beyond compatibility is provided. Medium fits as a necessary but not user-visible operational feature. |
| [NFR-007](#nfr-007) | Medium | Medium | Keeping Medium is reasonable: a safe training environment is described as needed to prevent staff mistakes and enable practice without risking production data, but it is not part of day-to-day reporting functionality. Medium supports it as important but deferrable relative to core operational requirements. |
| [NFR-008](#nfr-008) | High | High | Retaining High is justified: anonymized demographic statistics are explicitly required to protect patron privacy while still enabling useful analysis by geography and age range. Privacy risk and compliance implications justify High. |
| [AR-001](#ar-001) | Medium | Medium | Keeping Medium matches the evidence: separate development/training environments and config migration to production (via export/import of templates/permissions/saved queries) are operationally important for delivery quality but not a user-facing reporting capability; sources support it as a supporting obligation. |
| [AR-002](#ar-002) | Medium | Medium | Keeping Medium is appropriate: management-process documentation and complete data specifications/process descriptions support correct understanding and operations, but they are not direct runtime reporting functions. Medium priority fits supporting but non-core behavior. |
| [AR-003](#ar-003) | Medium | Medium | Keeping Medium aligns with source framing: management-process scope and interface boundaries (focus on reports/analysis; day-to-day patron-facing functions remain outside scope; reliance on enterprise ILS data) are important for project boundaries, but they primarily constrain scope rather than add core reporting value. |
| [AR-004](#ar-004) | Medium | Medium | Keeping Medium is justified: reporting service deployment is described as centralized/multi-location with separation from production, but the mechanism is explicitly left open. This reduces certainty and makes it important but not the highest business priority. |
| [AR-005](#ar-005) | High | High | Retaining High is justified: accounting/audit compliance for reports and data archiving is explicitly mandated, with some retention duration discussed. Even though jurisdictional details are not fully specified, compliance is high business impact. |
| [AR-006](#ar-006) | High | High | Retaining High is justified: legal transaction retention while protecting patron privacy is explicitly described, even though duration/covered records are not fully settled. Privacy and legal compliance risks justify High. |
| [AR-007](#ar-007) | Medium | Medium | Keeping Medium is consistent: transaction-history configurable retention and indefinite monthly/annual aggregates are specified, but the configurable history duration is unresolved and the sources do not establish strong business priority beyond the survey framing. Medium is appropriate. |
| [IR-001](#ir-001) | Medium | Medium | Keeping Medium is appropriate: access via web browser or Windows-compatible client with specific browser minimum versions is an integration/interface obligation, but it is not inherently more valuable than other reporting functions. Medium fits as necessary compatibility rather than core value. |
| [IR-002](#ir-002) | Medium | Medium | Keeping Medium is reasonable: vendor data exchange interfaces (APIs/standard files like USMARC21/EDIFACT) are a dependency for some libraries, with no universal availability or specific contract. Medium matches the conditional nature. |
| [IR-003](#ir-003) | Medium | Medium | Keeping Medium is justified: Excel/HTML/CSV output and CSV export where specifically requested are important usability/export requirements, but no conformance contract is described beyond these examples. Medium reflects value without clear evidence of being core correctness/safety. |

## Traceability and Verification

References below point to supplied source documents. Semantic support is checked by Reviewer; related requirement links are supplementary.

| Requirement | Related requirements | Source documents |
| --- | --- | --- |
| [FR-001](#fr-001) | — | [conversations/conv\_pines014\_material\_volume.eml](../../../data/corpus/conversations/conv_pines014_material_volume.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-002](#fr-002) | — | [conversations/conv\_pines015\_capacity\_interface.eml](../../../data/corpus/conversations/conv_pines015_capacity_interface.eml) |
| [FR-004](#fr-004) | [FR-002](#fr-002) | [conversations/conv\_pines016\_shelf\_space.eml](../../../data/corpus/conversations/conv_pines016_shelf_space.eml) |
| [FR-005](#fr-005) | [FR-006](#fr-006), [FR-007](#fr-007), [FR-008](#fr-008) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-006](#fr-006) | [FR-005](#fr-005) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml) |
| [FR-007](#fr-007) | [FR-005](#fr-005) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-008](#fr-008) | [FR-005](#fr-005) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml) |
| [FR-009](#fr-009) | [FR-005](#fr-005) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml) |
| [FR-010](#fr-010) | — | [conversations/conv\_pines019\_020\_missing\_intransit.eml](../../../data/corpus/conversations/conv_pines019_020_missing_intransit.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-011](#fr-011) | [FR-005](#fr-005) | [conversations/conv\_pines019\_020\_missing\_intransit.eml](../../../data/corpus/conversations/conv_pines019_020_missing_intransit.eml) |
| [FR-012](#fr-012) | [FR-013](#fr-013) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-013](#fr-013) | [FR-012](#fr-012) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml) |
| [FR-014](#fr-014) | [FR-015](#fr-015) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-015](#fr-015) | [FR-014](#fr-014) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-016](#fr-016) | [FR-017](#fr-017), [AR-005](#ar-005) | [conversations/conv\_pines022\_deletions.eml](../../../data/corpus/conversations/conv_pines022_deletions.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-017](#fr-017) | [FR-016](#fr-016) | [conversations/conv\_pines022\_deletions.eml](../../../data/corpus/conversations/conv_pines022_deletions.eml) |
| [FR-018](#fr-018) | [FR-019](#fr-019), [NFR-008](#nfr-008) | [conversations/conv\_pines023\_patron\_characteristics.eml](../../../data/corpus/conversations/conv_pines023_patron_characteristics.eml); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [FR-019](#fr-019) | [FR-018](#fr-018), [NFR-008](#nfr-008) | [conversations/conv\_pines024\_inactive\_patrons.eml](../../../data/corpus/conversations/conv_pines024_inactive_patrons.eml) |
| [FR-020](#fr-020) | [FR-021](#fr-021) | [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-021](#fr-021) | [FR-020](#fr-020), [FR-022](#fr-022), [NFR-008](#nfr-008) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-022](#fr-022) | [FR-021](#fr-021), [NFR-008](#nfr-008) | [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-023](#fr-023) | [FR-024](#fr-024), [AR-005](#ar-005) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml) |
| [FR-024](#fr-024) | [FR-023](#fr-023), [AR-005](#ar-005) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml) |
| [FR-025](#fr-025) | [FR-026](#fr-026) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-026](#fr-026) | [FR-025](#fr-025), [FR-027](#fr-027) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [email\_staff\_login.eml](../../../data/corpus/email_staff_login.eml) |
| [FR-027](#fr-027) | [FR-026](#fr-026) | [email\_staff\_login.eml](../../../data/corpus/email_staff_login.eml) |
| [FR-028](#fr-028) | [FR-021](#fr-021) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt) |
| [FR-029](#fr-029) | [NFR-001](#nfr-001) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-030](#fr-030) | [FR-029](#fr-029), [IR-001](#ir-001) | [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-031](#fr-031) | [FR-001](#fr-001), [FR-030](#fr-030), [AR-006](#ar-006), [AR-007](#ar-007) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [FR-032](#fr-032) | [FR-025](#fr-025) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-033](#fr-033) | [FR-025](#fr-025), [FR-030](#fr-030) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-034](#fr-034) | [FR-021](#fr-021) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-036](#fr-036) | [IR-002](#ir-002), [NFR-003](#nfr-003) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [NFR-001](#nfr-001) | [FR-029](#fr-029), [AR-004](#ar-004) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt) |
| [NFR-002](#nfr-002) | [NFR-001](#nfr-001) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [NFR-003](#nfr-003) | [NFR-004](#nfr-004), [IR-002](#ir-002) | [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt); [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt) |
| [NFR-004](#nfr-004) | [NFR-003](#nfr-003) | [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt); [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt) |
| [NFR-005](#nfr-005) | [NFR-001](#nfr-001) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [NFR-006](#nfr-006) | [IR-001](#ir-001) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt) |
| [NFR-007](#nfr-007) | [AR-001](#ar-001) | [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt); [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt) |
| [NFR-008](#nfr-008) | [FR-018](#fr-018), [FR-019](#fr-019) | [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [AR-001](#ar-001) | [NFR-007](#nfr-007), [FR-026](#fr-026) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [AR-002](#ar-002) | [FR-036](#fr-036) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [AR-003](#ar-003) | [NFR-005](#nfr-005), [IR-002](#ir-002) | [meeting\_minutes/meeting\_2009-03-15\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-03-15_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [AR-004](#ar-004) | [NFR-001](#nfr-001), [NFR-005](#nfr-005) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [evergreen\_reference\_2009.txt](../../../data/corpus/evergreen_reference_2009.txt) |
| [AR-005](#ar-005) | [FR-016](#fr-016), [FR-024](#fr-024), [AR-006](#ar-006), [AR-007](#ar-007) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml) |
| [AR-006](#ar-006) | [NFR-008](#nfr-008), [AR-005](#ar-005), [AR-007](#ar-007) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [AR-007](#ar-007) | [FR-031](#fr-031), [AR-005](#ar-005), [AR-006](#ar-006) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [IR-001](#ir-001) | [NFR-006](#nfr-006) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt) |
| [IR-002](#ir-002) | [AR-003](#ar-003) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [IR-003](#ir-003) | [FR-030](#fr-030), [FR-002](#fr-002) | [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt); [conversations/conv\_pines024\_inactive\_patrons.eml](../../../data/corpus/conversations/conv_pines024_inactive_patrons.eml) |

## Blacklist

### BL-001 — Revert transfer when destination checkout occurs

Proposal to automatically return an item to its original location when it is checked out at the destination.

**Reason discarded:** Excluded because the same source message says items checked out at the destination should stay there, while unused items should return. The corpus does not resolve this contradiction; FR-007 therefore retains the general reversion obligation without adopting this specific trigger.

**Sources:** [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml)

## Source Resolution Decisions

- Used category-prefixed IDs FR, NFR, IR, and AR. Merged overlapping candidates into retained requirements while preserving distinct conditions and scopes; candidate IDs remain supporting metadata and are not intended to reproduce every source mention.
- Removed FR-003 as an accepted system requirement. The source only raises competing possible meanings of capacity and says the metric needs to be settled; it does not establish an implemented behavior or select a measure. FR-002 therefore keeps the measurement unresolved and does not imply capacity is already defined.
- Revised FR-021, FR-033, and FR-034 to remove report families and behaviors supported only by the review-stage Galecia draft or the external Evergreen reference. FR-021 retains the transaction report dimensions and types reported in the staff survey; FR-033 retains survey-reported output and filtering problems; FR-034 retains survey and interview-backed item-date distinctions.
- Added AR-007 to represent the survey-supported operational retention behavior: configurable transaction-history duration with monthly and annual aggregates retained indefinitely. The unspecified duration remains explicit and is not conflated with legal retention in AR-006.
- Removed the duplicated IR-002 HTML-output requirement; NFR-004 is the single requirement for standards-compliant HTML. IR-001 remains the primary client-channel requirement, while NFR-006 now covers server operating systems only.
- The Galecia draft is identified in the March meeting as a foundation to adapt, and the July meeting records operating and design requirements as group findings. Draft-only examples and proposals are not treated as approved obligations without supporting stakeholder evidence. The external Evergreen reference describes existing capabilities and gaps, not automatic requests.
- The source corpus gives no confirmed capacity metric, shelf-space estimation method, universal legal retention period, real-time threshold, or transfer reversion rule for destination checkouts. These details remain explicit open points rather than invented decisions.
- The technical preference to keep reporting in the main relational database does not resolve the separate source request to avoid disrupting production operations. AR-004 records the deployment concern and leaves the architecture open; no implementation approach is mandated.
- The suggested capacity color-coding and scheduled purging were not adopted as requirements: the sources present them tentatively and do not confirm them in their summaries. Transfer checkout-trigger reversion is excluded in BL-001 due to a direct unresolved contradiction.
- Business priorities are inferred from the supplied evidence and use the requested scale: High for core or explicitly critical/mandatory obligations, Medium for important capabilities with a workaround or unresolved details, and Low for optional conveniences. No stakeholder priority was fabricated.
- The March meeting defines the project as management reporting and analysis, excluding day-to-day patron-facing OPAC and circulation behavior. Related data access and the requirement not to affect OPAC are retained without expanding product scope.
