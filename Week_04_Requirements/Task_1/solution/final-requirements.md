# PINES Management Processes and Reporting Requirements

Reporting and management processes used by library staff, managers, and administrators for collection and patron analysis, branch capacity, operational reporting, and financial tracking. Day-to-day patron-facing OPAC and circulation functions are outside this scope. Detailed interface and data-structure specifications remain subject to further refinement. The January draft and supplied reference materials are context; draft-only proposals are not treated as accepted requirements without direct stakeholder or meeting support.

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

Provide a report of material volume for a given library at any point in time, using counts for new acquisitions, items on the shelf (checked in), and items in circulation (checked out), as well as a total. Support breakdowns including total items, holds, adult fiction, and board books, and allow customizable categories for different libraries. The sources do not specify how historical points in time are selected or how categories are configured.

**Business priority rationale:** Inferred High: stakeholders identify this as a key board-report and collection-management need and say it avoids manually combining screens.

**Overall priority rationale:** Retained as High. The sources describe a core board/collection-management volume report (with specific breakdowns like holds and board books) and frame it as avoiding manual screen-combining; despite some unspecified configuration details, the functionality is essential.

<a id="fr-002"></a>

### FR-002 — Capacity sorting, filtering, trends, and export

**Business priority:** Medium · **Overall priority:** Medium

Allow users to sort and filter branch-capacity information, including by region, library type, and current load; show trend information indicating whether a branch is growing or shrinking; and export capacity data to CSV. No sorting fields beyond those requested for filtering, trend period, or export details are specified. Trend data depends on resolving the capacity measure in IR-001.

**Business priority rationale:** Inferred Medium: these are useful planning and spreadsheet features, with other ways to review branch information available as a workaround.

**Overall priority rationale:** Retained as Medium. Sorting/filtering, trends, and CSV export provide meaningful usability, but the sources position these as enhancements and do not indicate a critical dependency beyond clarifying IR-001’s capacity measure.

<a id="fr-003"></a>

### FR-003 — Shelf-space comparison reporting

**Business priority:** High · **Overall priority:** High

For each material genre and format, compare its percentage of total circulations, percentage of the collection, and percentage of total shelf space. Make the report available per library and per system, allow date-range filtering, and provide a side-by-side comparison of libraries that supports comparing each library's breakdown with the system average. Shelf space is not directly tracked according to the discussion; estimating it from item dimensions or using item count as a proxy were proposed, not settled methods, so the calculation method remains to be clarified.

**Business priority rationale:** Inferred High: multiple stakeholders identify this report as important for collection management and resource allocation; the shelf-space calculation remains uncertain.

**Overall priority rationale:** Retained as High. Multiple sources treat the comparative circulation/collection/shelf-space percentage report as important for collection management and side-by-side comparison; uncertainty remains only in how to calculate shelf space.

<a id="fr-004"></a>

### FR-004 — Batch item transfer utility

**Business priority:** High · **Overall priority:** High

Provide a utility to transfer batches of items between branches or temporary destinations such as mobile libraries, outreach programs, warehouses, or event locations. Users must be able to query candidate materials, save queries for repeated use, manually select titles from query results, and change selected items’ location records. Provide pull lists for items to be moved. The source describes changing the location field and generating pull lists as transfer mechanisms.

**Business priority rationale:** Inferred High: cataloging staff describe batch transfers and repeatable queries as a crucial, recurring workflow; the source also identifies transfer use across several programs.

**Overall priority rationale:** Retained as High. The sources describe a crucial batch transfer workflow (query candidates, save queries, move selected items, and generate pull lists) and emphasize its recurring operational use.

<a id="fr-005"></a>

### FR-005 — Revert temporary transfers

**Business priority:** Medium · **Overall priority:** Medium

Allow transferred items to be returned to their original location after a set period or based on other specified criteria. The sources give temporary-event and book-sale examples and mention status changes such as an item being sold or returned. The sources conflict about checkout at the destination: one example lists checkout as a reversion trigger, while its explanation says checked-out items should stay and unused items should return. Do not assume checkout is a reversion trigger until this conflict is clarified.

**Business priority rationale:** Inferred Medium: temporary transfers need a return mechanism, but there are manual-workaround possibilities and the event-trigger details remain uncertain.

**Overall priority rationale:** Retained as Medium. The sources require a mechanism to revert temporary transfers, but they also show conflict/uncertainty about the trigger logic (e.g., checkout at destination), leaving room for workaround until clarified.

<a id="fr-006"></a>

### FR-006 — Transfer safeguards and supporting functions

**Business priority:** Medium · **Overall priority:** Medium

Restrict transfer capability to designated roles, with managers, administrators, and transfer coordinators given as examples. Before a transfer, show a preview identifying the number of items and the origin and destination and request confirmation; provide an undo function; track transfer history; generate printable transit labels; and alert users when transfers are delayed or have issues. The sample item counts and transfer-history count in the messages are illustrative, not thresholds. Transfer logging for audit purposes was proposed by a technical participant but was not explicitly adopted as a separate obligation.

**Business priority rationale:** Inferred Medium: permission control and preview reduce transfer errors, while history, labels, undo, and alerts improve operational handling; the sources do not mark these additions as critical.

**Overall priority rationale:** Retained as Medium. Permission controls, preview/confirmation, undo, labels, and alerts improve safety and reduce errors, but the sources do not mark them as strictly critical compared to the base transfer capability.

<a id="fr-007"></a>

### FR-007 — Uncataloged material inventory and use

**Business priority:** Medium · **Overall priority:** Medium

Support inventory tracking for uncataloged materials such as paperback books and children's board books, including quick distribution with minimal branch labor, identification of how material is used, and counting transactions for circulation statistics and reports. The sources do not give a numerical speed or labor target.

**Business priority rationale:** Inferred Medium: this supports a specific cataloging and distribution workflow and improves statistics, but the sources do not describe it as a universal core operation.

**Overall priority rationale:** Retained as Medium. The sources support a targeted workflow for uncataloged inventory and circulation-stat counting, but they do not present it as a universal core operation.

<a id="fr-008"></a>

### FR-008 — Missing and damaged items reports

**Business priority:** High · **Overall priority:** High

Provide reports of missing and damaged items per branch for inventory auditing and collection management. Include item condition notes, such as water damage or vandalism, to help users understand root causes. The sources do not specify a required date-range filter or a prescribed set of note values.

**Business priority rationale:** Inferred High: stakeholders describe branch-level reporting as crucial for accountability, inventory audits, and collection management.

**Overall priority rationale:** Retained as High. The sources explicitly request per-branch missing/damaged item reporting for audit/accountability, including condition notes, which is operationally important.

<a id="fr-009"></a>

### FR-009 — Combined in-transit items report

**Business priority:** High · **Overall priority:** High

Generate one report listing items that have been in transit for more than a configurable number of days, available per branch and per system, combining transit-to and transit-from items. Allow the report to be sorted by due date so front-line staff can pursue the oldest items first. Seven days was suggested as a probable default, but the consolidated requirement specifies only a configurable threshold, so no default is established.

**Business priority rationale:** Inferred High: interview findings call in-transit reporting critical for delivery coordination and stakeholders report losing items in transit.

**Overall priority rationale:** Retained as High. The sources position in-transit reporting as critical for delivery coordination and item loss recovery, and the consolidation of transit-to/from plus sorting is operationally valuable.

<a id="fr-010"></a>

### FR-010 — Purge candidates and configurable criteria

**Business priority:** High · **Overall priority:** High

Provide reports and a utility to identify item records as purge candidates using customizable status-, time-, and activity-based criteria, including missing status duration, discard/weed status, damaged status, and time since last circulation. Allow criteria to be combined; the sources explicitly give AND combinations as examples. Candidate-identification reports must be read-only, and actual deletions require a separate confirmation step.

**Business priority rationale:** Inferred High: weeding and purging are described as frequently used, and read-only candidates plus confirmation are explicitly consolidated as safety measures.

**Overall priority rationale:** Retained as High. The sources describe purge/weeding as a safety-critical, frequently used process with strong emphasis on read-only candidate identification and separate confirmation for deletion.

<a id="fr-011"></a>

### FR-011 — Batch status conversion and cleanup

**Business priority:** Medium · **Overall priority:** Medium

Provide a report to assist in converting items from one status to another in batch. Also provide a quick, effective method to delete volume entries together with copy entries and to delete records with no items attached. The sources do not settle whether cleanup is automated or manual, and the example batch size is illustrative rather than a limit.

**Business priority rationale:** Inferred Medium: batch conversion and orphan cleanup reduce substantial manual cataloging work, but the sources do not classify them as essential to daily operation.

**Overall priority rationale:** Retained as Medium. Batch status conversion and related cleanup reduce manual work, but the sources do not elevate them to essential daily operations compared to core purge/delete safety flows.

<a id="fr-012"></a>

### FR-012 — Last-copy reporting

**Business priority:** High · **Overall priority:** High

Provide reports that identify last copies within both a library and the system, to help prevent accidental loss and support catalogers' WorldCat updates. A stakeholder explicitly requested both library and system views; later emphasis on system-wide protection reinforces, rather than replaces, the library view. The sources request support for WorldCat updates but do not establish a WorldCat integration or a requirement to report deleted last-copy items.

**Business priority rationale:** Explicitly critical: the interview and request call the last-copy report critical and describe the risk of deleting the only consortium copy.

**Overall priority rationale:** Retained as High. The sources explicitly call the last-copy report critical to prevent accidental deletion of the only consortium copy and to support WorldCat-related maintenance.

<a id="fr-013"></a>

### FR-013 — Record completed deletions and report activity

**Business priority:** High · **Overall priority:** High

Count and track completed record deletions, including item, patron, and bibliographic record types, by location and system. Retain the deletion timestamp, the user who performed the deletion, and that user's location. Provide reports that can aggregate by date range, user, record type, and location and show totals by period, type, and location. Tracking denied deletion attempts was described as helpful, not as an established requirement; the source also raises deletion reason as a possibility without a consolidated decision.

**Business priority rationale:** Inferred High: stakeholders repeatedly identify deletion tracking as necessary for auditing, accountability, troubleshooting, and retention-schedule audits.

**Overall priority rationale:** Retained as High. The sources repeatedly emphasize tracking completed record deletions (who/when/where and types) for auditing, troubleshooting, and accountability.

<a id="fr-014"></a>

### FR-014 — Purge audit trail

**Business priority:** High · **Overall priority:** High

Maintain an audit trail for all purges that identifies who purged what and when, for accountability and troubleshooting. This purge-specific obligation is retained separately from general record-deletion tracking because the sources identify purge operations and record deletions as distinct contexts.

**Business priority rationale:** Inferred High: the consolidated purge safety measures include an audit trail, and a stakeholder explicitly connects it to accountability and troubleshooting.

**Overall priority rationale:** Retained as High. The sources include purge-specific audit trail requirements as a safety/accountability measure distinct from general deletion tracking.

<a id="fr-015"></a>

### FR-015 — Patron characteristic reporting

**Business priority:** High · **Overall priority:** High

Allow patron queries and reports to be filtered and grouped by age range, ZIP code, county of residence, home branch, patron type, and preferred language. Support combining filters with AND and OR logic, allow age brackets to be configured per report, and include records with missing optional values as null rather than silently excluding them.

**Business priority rationale:** Inferred High: stakeholders describe these reports as essential to program planning and collection decisions; the requested dimensions and handling rules are explicit.

**Overall priority rationale:** Retained as High. The sources define explicit patron characteristic dimensions, grouping/filtering logic (AND/OR), configurable age brackets, and inclusion of nulls—positioned as essential for planning and decisions.

<a id="fr-016"></a>

### FR-016 — Inactive-patron reporting

**Business priority:** High · **Overall priority:** High

Generate a list of patrons with no circulation or qualifying electronic activity during a configurable number of days, with results configurable by system, home library, county, and other needed levels. Count OPAC or patron-account logins, online hold placements, online renewals, and access to digital collections when the relevant integration or event data is available. Include current mailing addresses, separately identify inactive patrons with outstanding fines, allow exclusion of selected patrons such as do-not-disturb, VIP, staff, or opted-out patrons, and provide CSV export for outreach. The sources do not specify the handling of digital-resource events when such data is unavailable.

**Business priority rationale:** Inferred High: stakeholders use the report for database cleanup and outreach; its configurable period and scopes are explicit, and CSV export is specified in the consolidated summary.

**Overall priority rationale:** Retained as High. The sources describe inactive-patron reporting with configurable time window/scopes, outreach-support fields, fine handling, exclusions, and CSV export—core to cleanup/outreach workflows.

<a id="fr-017"></a>

### FR-017 — Transaction and circulation reporting

**Business priority:** High · **Overall priority:** High

Support transaction reporting grouped by hour, terminal, branch, and system, with queries over all transactions or by transaction type, including check-ins, check-outs, fines collected, and patron registrations. Count check-in types individually and cumulatively (book-drop, terminal, and user or self-service) and count check-outs and renewals individually and cumulatively (staff checkout, self-checkout, staff renewal, self-checkout renewal, online renewal, and OPAC renewal). Record hold placement method (staff desk, public computer, or remote). Report holds placed, holds filled, and check-outs per patron, library, selected group of libraries, system, or county; show per-patron checkout and placed-hold counts.

**Business priority rationale:** Inferred High: circulation reporting is among the most frequently used report classes in the supplied survey, and the sources define detailed operational counts and scopes.

**Overall priority rationale:** Retained as High. The sources treat transaction/circulation reporting as a key operational/reporting capability with detailed counting and multiple required scopes and dimensions.

<a id="fr-018"></a>

### FR-018 — Transaction history and aggregates

**Business priority:** Medium · **Overall priority:** Medium

Maintain transaction history for a configurable number of days and retain monthly and annual aggregate information indefinitely. The sources do not specify the configurable number of days or further define which transaction fields are retained in the aggregates.

**Business priority rationale:** Inferred Medium: useful for reporting and longitudinal analysis, but the retention duration is deliberately left configurable and no stakeholder marks this as a critical operational feature.

**Overall priority rationale:** Retained as Medium. Transaction history retention and indefinite monthly/annual aggregates are useful for longitudinal analysis, but the configurable retention duration and lack of “critical” framing justify Medium.

<a id="fr-019"></a>

### FR-019 — Patron behavior and demographic statistics

**Business priority:** Medium · **Overall priority:** Medium

Produce statistics to support understanding or prediction of patron behavior and material use, including examples such as average return time, likelihood of renewal, and the share of check-outs that are renewals. Provide demographic statistics including transactions by geographic region and age range. No prediction method or accuracy target is specified; demographic outputs must not contain information that could identify a patron, as detailed in NFR-003.

**Business priority rationale:** Inferred Medium: sources identify these statistics as useful for planning and analysis, but do not define a critical operational dependency or predictive performance target.

**Overall priority rationale:** Retained as Medium. Patron behavior/demographic statistics are valuable for planning/analysis, but the sources do not define predictive targets or make the capability operationally critical.

<a id="fr-020"></a>

### FR-020 — Financial data and reporting

**Business priority:** High · **Overall priority:** High

Associate fines, charges, waivers, and ecommerce transactions with patron and item records, and allow reports to join those data sources. Track waived fines and payments by library, support updates to financial information, and allow staff to query patron accounts with balances greater than a specified amount. A payment made at the front desk must be reflected immediately in the system, as requested; no more precise update-time measure is supplied. Provide reports of account balances by patron, home library, and system; fines and charges by period and charge type; waived fines by period and branch; and payments by period and method. Payment-method examples include staff desk, self-check, OPAC, cash, credit card, and check; these examples are not exhaustive.

**Business priority rationale:** Inferred High: finance stakeholders identify these reports for reconciliation, branch budgets, and accounts needing attention; the payment ledger is separately identified as critical.

**Overall priority rationale:** Retained as High. Financial reporting and real-time reflection of front-desk payments are emphasized for reconciliation and account management; the payment ledger linkage is treated as separately critical.

<a id="fr-021"></a>

### FR-021 — Item value reports

**Business priority:** Medium · **Overall priority:** Medium

Generate reports of item values using item-record data for the entire collection or a selected portion, including examples such as long-overdue items and DVDs in the children's collection. The financial discussion identifies purchase price as data available in item records; no valuation formula beyond item-record data is specified.

**Business priority rationale:** Inferred Medium: this supports collection and financial analysis, but the sources present it as a reporting need rather than a critical operational constraint.

**Overall priority rationale:** Retained as Medium. Item value reporting supports collection/financial analysis, with sources framing it as a reporting need rather than a core operational constraint.

<a id="fr-022"></a>

### FR-022 — Payment-to-charge ledger

**Business priority:** High · **Overall priority:** High

Maintain a ledger of patron payments identifying the specific charge or charges to which each payment was applied, to support reconciliation. The sources do not specify additional ledger fields or a retention period.

**Business priority rationale:** Explicitly critical: a finance stakeholder states that charge-level traceability is critical to reconcile accounts.

**Overall priority rationale:** Retained as High. The sources explicitly state charge-level traceability of payments is critical for reconciliation, making it a core finance correctness requirement.

<a id="fr-023"></a>

### FR-023 — Catalog data-quality reports

**Business priority:** Medium · **Overall priority:** Medium

Provide reports identifying items with invalid item types, items with long call numbers, and bibliographic records with no item records. These specific checks are requested in the cataloging interview; broader report families listed only as draft examples or existing-system gaps are not made mandatory by this requirement.

**Business priority rationale:** Inferred Medium: cataloging staff identify these reports as useful for maintaining data integrity, but the sources do not describe them as core operations.

**Overall priority rationale:** Retained as Medium. The requested data-quality reports target specific integrity checks (invalid types/long call numbers/no items), which are important but not described as core daily operations.

<a id="fr-024"></a>

### FR-024 — Report templates and interfaces

**Business priority:** High · **Overall priority:** High

Allow administrators to create report templates for staff, and allow staff to run them as-is or make controlled modifications that do not compromise result accuracy. Administrators must be able to limit which filters and display fields can be changed; examples permit changing a call-number range or display fields but not altering a template to display deleted items. Allow permitted users to clone a report into a new variant, distinct from modifying the existing template. The sources do not establish canned, on-demand, or open-template interface types, bundled report execution, or permission-based addition of canned reports as accepted obligations.

**Business priority rationale:** Inferred High: survey results show strong interest in templates, and stakeholders emphasize consistent report criteria and controlled modifications.

**Overall priority rationale:** Retained as High. Report templates with controlled modification/cloning are positioned as key for consistent results and usability, indicating strong practical priority.

<a id="fr-025"></a>

### FR-025 — Query design and criteria display

**Business priority:** High · **Overall priority:** High

Provide a user-friendly query-design interface across bibliographic, item, patron, transaction, and financial record types. Support field selection, picklist values, regular expressions selected from a dropdown, and Boolean operators; administrators must control staff access to tables and fields. Display query selections or criteria with results so users can see how the report was generated. The sources do not specify a complete field list or a particular query language.

**Business priority rationale:** Inferred High: stakeholders report difficulty constructing queries and filtering on needed fields, and the draft describes query capability as a general reporting tool.

**Overall priority rationale:** Retained as High. The sources emphasize the need for a query design interface across record types with understandable criteria display and admin-controlled access, reflecting a foundational reporting capability.

<a id="fr-026"></a>

### FR-026 — Report permissions and roles

**Business priority:** High · **Overall priority:** High

Provide fine-grained permissions controlling who may create, clone, run, and modify reports, and who may run ad hoc reports on specified data sets. Administrators must be able to use shared folders to allow or disallow access to specific reports. Permissions should be manageable through roles so that changing a user's role updates the user's report permissions. The sources do not define a complete permission matrix.

**Business priority rationale:** Inferred High: stakeholders identify permission control as essential for protecting report data and the survey reports strong demand for fine-grained permissions.

**Overall priority rationale:** Retained as High. Fine-grained permissions, shared folders, and role-based management are repeatedly framed as essential for protecting report/data access.

<a id="fr-027"></a>

### FR-027 — Staff login and individual identity

**Business priority:** Medium · **Overall priority:** Medium

Support individual staff authentication using username and password and also support, without requiring, a streamlined login method such as employee-card swipe. Regardless of method, the system must identify the individual staff member logged in for audit purposes; streamlined login must not bypass individual identification. The sources do not require a particular card technology.

**Business priority rationale:** Inferred Medium: streamlined login is an optional convenience, while maintaining individual identity supports the stated audit and security need.

**Overall priority rationale:** Retained as Medium. Individual staff identity/auditing is important, but the streamlined login method is optional convenience while identity requirements remain the main necessity.

<a id="fr-028"></a>

### FR-028 — Report queue visibility and priority

**Business priority:** High · **Overall priority:** High

Allow staff to see report queue position, how many reports are ahead, submission time, and status, including waiting, running, completed, and failed. Show report priority and allow selected important reports to move ahead of other queued work; the sources give a director's board report ahead of an ad hoc query as an example but do not specify a complete ordering policy. Allow reports to be canceled when scheduled or while running. The sources do not specify status refresh frequency or cancellation behavior after processing begins.

**Business priority rationale:** Inferred High: survey and meeting findings emphasize queue visibility, and stakeholder requests explicitly include priority and moving important reports ahead in the queue.

**Overall priority rationale:** Retained as High. The sources call for queue visibility with status/priority and the ability to move important reports ahead, plus cancellation—supporting operational transparency and responsiveness.

<a id="fr-029"></a>

### FR-029 — Recurring report scheduling and output formats

**Business priority:** Medium · **Overall priority:** Medium

Allow reports to be scheduled to run recurrently and provide report output in Excel, HTML, and CSV formats. Recurring scheduling and these formats are directly supported by the survey and technical-subcommittee notes. The sources do not establish required scheduling frequencies, email delivery, or comparative-period output as accepted obligations.

**Business priority rationale:** Inferred Medium: recurring reporting and multiple formats are useful and directly supported, while users can run reports manually where scheduling is unavailable.

**Overall priority rationale:** Retained as Medium. Recurring scheduling and Excel/HTML/CSV output formats are directly supported, but the sources do not frame them as critical versus on-demand manual reporting.

<a id="fr-030"></a>

### FR-030 — Board and executive reports

**Business priority:** High · **Overall priority:** High

Provide predefined reports for library boards and other external consumers, including basic statistics identified in the sources as relevant to the Georgia Annual Report and Application for State Aid. Activity reports should cover check-outs, check-ins, holds placed, and holds filled, with cross-tabulation by terminal, branch, library system, hour, patron age range, patron type, and patron location. The detailed contents of the referenced annual-report requirements are not provided and are not expanded here.

**Business priority rationale:** Inferred High: board and executive reporting is an explicit stakeholder need for planning and reporting, and pre-defined board reports were identified in interview findings.

**Overall priority rationale:** Retained as High. Board/executive reporting is explicitly requested with specific activity measures and cross-tabs, indicating a core external reporting need.

<a id="fr-031"></a>

### FR-031 — Historical reporting

**Business priority:** Medium · **Overall priority:** Medium

Allow users to retrieve historical data for a specified date or date range, including what data looked like on a past date even when a value such as shelving location has since changed. The sources also request historical bill snapshots and real-time reporting for some uses, but do not define all report coverage or the latency meaning of “real time.” A reporting warehouse was suggested, not selected as a required implementation.

**Business priority rationale:** Inferred Medium: historical comparisons are useful for planning and audits, but the sources do not specify coverage or a critical operational dependency.

**Overall priority rationale:** Retained as Medium. Historical reporting is valuable, but the sources do not fully define coverage/latency semantics, so urgency is moderate rather than essential.

<a id="fr-032"></a>

### FR-032 — Report result completeness and context

**Business priority:** Medium · **Overall priority:** Medium

Include null and blank fields in report results, including when filtering or displaying data. Show report name and selected date criteria with results. The sources do not state an exception for particular report types or field selections.

**Business priority rationale:** Inferred Medium: this avoids silent omissions and helps users interpret report results, though it is an important reporting-quality improvement rather than a stated core operation.

**Overall priority rationale:** Retained as Medium. Including null/blank fields, and showing report name and selected date criteria improves interpretability, but it is framed as a quality/reporting completeness enhancement.

<a id="fr-033"></a>

### FR-033 — Show item last-edit date

**Business priority:** Medium · **Overall priority:** Medium

Allow item reports to show the date an item was last edited. This date must reflect item edits only and must not include the item's last circulation; the source notes that the current system combines these dates.

**Business priority rationale:** Inferred Medium: cataloging staff explicitly request this distinction for reporting and data-quality work, but no source identifies it as a core operational constraint.

**Overall priority rationale:** Retained as Medium. The distinction between last edit vs last circulation is clearly requested for reporting accuracy, but it does not appear as a core system-wide operational obligation.

<a id="fr-034"></a>

### FR-034 — Online help and error feedback

**Business priority:** Medium · **Overall priority:** Medium

Provide online, hierarchical, cross-linked HTML help describing and illustrating system functions. Provide high-level error reporting and feedback, and low-level query-specific feedback for Local and Global System Administrators from the front end; report failures should give useful details, such as the affected table, field, and error type, rather than only a generic failure message. Searchability and ease of navigation are described in the interview, while specific context-sensitive behavior is not mandated.

**Business priority rationale:** Inferred Medium: help and actionable error feedback reduce reliance on IT and assist report troubleshooting, but are not identified as core reporting outputs.

**Overall priority rationale:** Retained as Medium. Online hierarchical help and actionable error feedback are valuable for reducing reliance on IT and improving troubleshooting, but not presented as core reporting functionality.

## Non-Functional Requirements

<a id="nfr-001"></a>

### NFR-001 — Protect OPAC and operational responsiveness

**Business priority:** High · **Overall priority:** High

Management reporting must not constrain OPAC functionality or slow patron access to the catalog. Searches and reports should be processable during open hours without disrupting other system functions, including the circulation client. Background processing, queuing, or read-only reporting replicas are suggested approaches, not mandated designs; no measurable response-time target is supplied.

**Business priority rationale:** Explicitly critical in the technical interview and meeting discussion: reporting must not disrupt circulation or OPAC access.

**Overall priority rationale:** Retained as High. The sources explicitly require that reporting not disrupt OPAC/circulation and emphasize open-hours responsiveness; this is a core system constraint.

<a id="nfr-002"></a>

### NFR-002 — Consortium operating scale

**Business priority:** High · **Overall priority:** High

Support the consortium scale stated in the draft and meeting minutes: 286 locations, 17 million annual circulations, and purchasing and processing over 900,000 items per year. The transfer discussion separately raises batch-update efficiency and possible database locking for a cited 9.6-million-item environment, but presents smaller batches as a technical suggestion rather than an adopted requirement.

**Business priority rationale:** Inferred High: the supplied meeting minutes state the consortium scale as a must-support environment.

**Overall priority rationale:** Retained as High. The sources state consortium operating scale as a must-support environment, making it a foundational quality/performance context.

<a id="nfr-003"></a>

### NFR-003 — Accessibility and privacy of reporting

**Business priority:** High · **Overall priority:** High

Make Management Processes accessible with screen readers, screen magnification software, and other assistive technology; the technical interview identifies Section 508 as mandatory and names JAWS, NVDA, and ZoomText as examples. Transaction archives and demographic reporting must protect patron privacy and exclude personally identifying information from demographic data while preserving useful statistics. The sources do not specify a retention duration for transaction archives or a detailed privacy method.

**Business priority rationale:** High: the technical interview explicitly calls accessibility a non-negotiable legal requirement; privacy is a source-supported constraint on archived and demographic data.

**Overall priority rationale:** Retained as High. Accessibility is described as non-negotiable (legal requirement language), and privacy constraints are explicitly supported for demographic reporting and archives.

<a id="nfr-004"></a>

### NFR-004 — Relational data compatibility and HTML output

**Business priority:** High · **Overall priority:** High

Use a fully relational database back end and make the reporting system work with the relational structure. Produce standards-compliant HTML for web-based components, report output, and help. The sources record a preference against denormalization but do not make that preference a separate mandatory constraint, and they do not require PostgreSQL specifically.

**Business priority rationale:** The supplied meeting minutes state that a fully relational database back end and standards-compliant HTML shall be used (SRC-5ab1dd8bc97a-001 lines 102-112), which fits the defined High category for a source-supported mandatory system constraint.

**Overall priority rationale:** Retained as High. Meeting minutes require a fully relational database back end and standards-compliant HTML for web components and report/help output.

## Interface Requirements

<a id="ir-001"></a>

### IR-001 — All-branch capacity overview

**Business priority:** High · **Overall priority:** High

Provide an interface showing the capacity of all branches at once and allow users to drill down into an individual branch. The meaning of “capacity” is unresolved: the discussion lists items versus shelf space, items versus a configured limit, and circulation versus processing capacity, but does not select a measure. Clarify the measure before treating capacity values or trends as defined.

**Business priority rationale:** Inferred High: stakeholders describe all-branch capacity visibility as needed for branch allocation decisions, although the measure itself requires clarification.

**Overall priority rationale:** Retained as High. The sources call for an all-branch capacity overview as needed for allocation decisions, with the main risk being only the unresolved definition of “capacity” measure.

<a id="ir-002"></a>

### IR-002 — Staff access options

**Business priority:** High · **Overall priority:** High

Make Management Processes accessible through either a web browser or a Windows-compatible client; the source does not require both modes. If browser-based access is provided, support Internet Explorer 6.0 or later and Firefox 2.0 or later, as specified in the supplied draft and meeting minutes. These are source-stated compatibility conditions, not a claim about current browser suitability.

**Business priority rationale:** The technical interview calls the access requirement critical for differing library environments, and the browser/client alternatives are stated as required operating-environment conditions in SRC-5ab1dd8bc97a-001 lines 82-93.

**Overall priority rationale:** Retained as High. Access via web browser or Windows-compatible client (with explicit browser version conditions when browser access is used) is stated as a required operating-environment requirement.

<a id="ir-003"></a>

### IR-003 — Vendor data interfaces

**Business priority:** Low · **Overall priority:** Low

Where vendor data interfaces are used, support interaction with vendor websites through published APIs and/or automated transfer of standard-format data files; USMARC21 and EDIFACT are examples in the source. The source describes this as a dependency and cautions that vendor data may not be available at every library. It does not define specific vendors, APIs, or file-transfer contracts.

**Business priority rationale:** Inferred Low: the source describes this as a dependency for some vendor data, not a universal feature for every library.

**Overall priority rationale:** Retained as Low. Vendor interface support is described as conditional/dependency-based (not available at every library) rather than universally required.

<a id="ir-004"></a>

### IR-004 — Query OPAC-created data

**Business priority:** High · **Overall priority:** High

Management Processes reporting must be able to query patron data such as holds and circulation created through the OPAC. This is a reporting dependency; the source does not specify an interface contract or authorize changes to OPAC behavior.

**Business priority rationale:** Inferred High: reporting functions require access to OPAC-created holds and circulation data, while OPAC behavior itself remains out of scope.

**Overall priority rationale:** Retained as High. The sources state that reporting must be able to query OPAC-created holds/circulation transactions, making it essential for report correctness.

## Additional Requirements (Operational, Legal and Deployment)

<a id="ar-001"></a>

### AR-001 — Deployment platform compatibility

**Business priority:** High · **Overall priority:** High

**Type:** Deployment

Management Processes must operate on Linux or Solaris server environments. The sources identify use of both platforms in the PINES environment; PostgreSQL and specific server versions are context, not additional platform requirements.

**Business priority rationale:** Operation on Linux or Solaris is stated as a required environment condition, and the technical interview says the system needs to work on both platforms (SRC-b1738fd7a6de-001 lines 31-35; SRC-5ab1dd8bc97a-001 lines 78-80).

**Overall priority rationale:** Retained as High. The sources identify Linux/Solaris server operation as a required environment condition with explicit dual-site expectation.

<a id="ar-002"></a>

### AR-002 — Separate environments and configuration migration

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Deployment

Provide separate development and training environments, and support migration of configurations to production. Identified configurations include report templates, permission settings, saved queries, and other configuration. Training must allow staff to experiment without risking production data. The sources do not specify the technical isolation or migration mechanism beyond export/import being discussed.

**Business priority rationale:** Inferred Medium: the technical interview and meeting describe separate environments and configuration migration as needed for safe development and staff training; the draft marks configuration migration medium priority.

**Overall priority rationale:** Retained as Medium. Separate dev/training environments and configuration migration are important for safe operations, but the sources do not provide certainty about the underlying technical mechanism, supporting Medium priority.

<a id="ar-003"></a>

### AR-003 — Applicable financial and data-retention obligations

**Business priority:** High · **Overall priority:** High

**Type:** Legal

All reports and data archiving must comply with standard accounting practice and applicable state, county, and municipal auditing requirements. Enforce applicable data-retention policies. A participant states that some data must be retained for seven years, while another source describes a state-law retention period of X years; neither specifies which data the period applies to or establishes a universal seven-year policy. Do not infer a specific retention duration until the applicable data and governing requirement are clarified.

**Business priority rationale:** High: the sources state mandatory audit-compliance and retention-policy obligations; the precise retention period remains uncertain.

**Overall priority rationale:** Retained as High. The sources require compliance with auditing and enforce data-retention policies; the exact retention duration is uncertain, but the obligation itself is high-priority.

<a id="ar-004"></a>

### AR-004 — Data specifications and process documentation

**Business priority:** Medium · **Overall priority:** Medium

**Type:** Operational

Provide complete data specifications for authority, bibliographic, order, item, hold/request, and other records maintained or accessed by Management Processes. Also provide high-level descriptions of major processes, including bibliographic record import and export, validation against internal and external authority sources, and standard reports. These are documentation deliverables; the sources do not prescribe a particular document format.

**Business priority rationale:** Inferred Medium: documentation helps staff understand data and processes and supports effective reporting, but does not directly perform a report workflow.

**Overall priority rationale:** Retained as Medium. Documentation/data specifications are necessary for correct operations and maintenance, but are not described as core runtime report/reporting functionality.

## Overall Priority List

| Requirement | Business priority | Overall priority | Developer rationale |
| --- | --- | --- | --- |
| [FR-001](#fr-001) | High | High | Retained as High. The sources describe a core board/collection-management volume report (with specific breakdowns like holds and board books) and frame it as avoiding manual screen-combining; despite some unspecified configuration details, the functionality is essential. |
| [IR-001](#ir-001) | High | High | Retained as High. The sources call for an all-branch capacity overview as needed for allocation decisions, with the main risk being only the unresolved definition of “capacity” measure. |
| [FR-002](#fr-002) | Medium | Medium | Retained as Medium. Sorting/filtering, trends, and CSV export provide meaningful usability, but the sources position these as enhancements and do not indicate a critical dependency beyond clarifying IR-001’s capacity measure. |
| [FR-003](#fr-003) | High | High | Retained as High. Multiple sources treat the comparative circulation/collection/shelf-space percentage report as important for collection management and side-by-side comparison; uncertainty remains only in how to calculate shelf space. |
| [FR-004](#fr-004) | High | High | Retained as High. The sources describe a crucial batch transfer workflow (query candidates, save queries, move selected items, and generate pull lists) and emphasize its recurring operational use. |
| [FR-005](#fr-005) | Medium | Medium | Retained as Medium. The sources require a mechanism to revert temporary transfers, but they also show conflict/uncertainty about the trigger logic (e.g., checkout at destination), leaving room for workaround until clarified. |
| [FR-006](#fr-006) | Medium | Medium | Retained as Medium. Permission controls, preview/confirmation, undo, labels, and alerts improve safety and reduce errors, but the sources do not mark them as strictly critical compared to the base transfer capability. |
| [FR-007](#fr-007) | Medium | Medium | Retained as Medium. The sources support a targeted workflow for uncataloged inventory and circulation-stat counting, but they do not present it as a universal core operation. |
| [FR-008](#fr-008) | High | High | Retained as High. The sources explicitly request per-branch missing/damaged item reporting for audit/accountability, including condition notes, which is operationally important. |
| [FR-009](#fr-009) | High | High | Retained as High. The sources position in-transit reporting as critical for delivery coordination and item loss recovery, and the consolidation of transit-to/from plus sorting is operationally valuable. |
| [FR-010](#fr-010) | High | High | Retained as High. The sources describe purge/weeding as a safety-critical, frequently used process with strong emphasis on read-only candidate identification and separate confirmation for deletion. |
| [FR-011](#fr-011) | Medium | Medium | Retained as Medium. Batch status conversion and related cleanup reduce manual work, but the sources do not elevate them to essential daily operations compared to core purge/delete safety flows. |
| [FR-012](#fr-012) | High | High | Retained as High. The sources explicitly call the last-copy report critical to prevent accidental deletion of the only consortium copy and to support WorldCat-related maintenance. |
| [FR-013](#fr-013) | High | High | Retained as High. The sources repeatedly emphasize tracking completed record deletions (who/when/where and types) for auditing, troubleshooting, and accountability. |
| [FR-014](#fr-014) | High | High | Retained as High. The sources include purge-specific audit trail requirements as a safety/accountability measure distinct from general deletion tracking. |
| [FR-015](#fr-015) | High | High | Retained as High. The sources define explicit patron characteristic dimensions, grouping/filtering logic (AND/OR), configurable age brackets, and inclusion of nulls—positioned as essential for planning and decisions. |
| [FR-016](#fr-016) | High | High | Retained as High. The sources describe inactive-patron reporting with configurable time window/scopes, outreach-support fields, fine handling, exclusions, and CSV export—core to cleanup/outreach workflows. |
| [FR-017](#fr-017) | High | High | Retained as High. The sources treat transaction/circulation reporting as a key operational/reporting capability with detailed counting and multiple required scopes and dimensions. |
| [FR-018](#fr-018) | Medium | Medium | Retained as Medium. Transaction history retention and indefinite monthly/annual aggregates are useful for longitudinal analysis, but the configurable retention duration and lack of “critical” framing justify Medium. |
| [FR-019](#fr-019) | Medium | Medium | Retained as Medium. Patron behavior/demographic statistics are valuable for planning/analysis, but the sources do not define predictive targets or make the capability operationally critical. |
| [FR-020](#fr-020) | High | High | Retained as High. Financial reporting and real-time reflection of front-desk payments are emphasized for reconciliation and account management; the payment ledger linkage is treated as separately critical. |
| [FR-021](#fr-021) | Medium | Medium | Retained as Medium. Item value reporting supports collection/financial analysis, with sources framing it as a reporting need rather than a core operational constraint. |
| [FR-022](#fr-022) | High | High | Retained as High. The sources explicitly state charge-level traceability of payments is critical for reconciliation, making it a core finance correctness requirement. |
| [FR-023](#fr-023) | Medium | Medium | Retained as Medium. The requested data-quality reports target specific integrity checks (invalid types/long call numbers/no items), which are important but not described as core daily operations. |
| [FR-024](#fr-024) | High | High | Retained as High. Report templates with controlled modification/cloning are positioned as key for consistent results and usability, indicating strong practical priority. |
| [FR-025](#fr-025) | High | High | Retained as High. The sources emphasize the need for a query design interface across record types with understandable criteria display and admin-controlled access, reflecting a foundational reporting capability. |
| [FR-026](#fr-026) | High | High | Retained as High. Fine-grained permissions, shared folders, and role-based management are repeatedly framed as essential for protecting report/data access. |
| [FR-027](#fr-027) | Medium | Medium | Retained as Medium. Individual staff identity/auditing is important, but the streamlined login method is optional convenience while identity requirements remain the main necessity. |
| [FR-028](#fr-028) | High | High | Retained as High. The sources call for queue visibility with status/priority and the ability to move important reports ahead, plus cancellation—supporting operational transparency and responsiveness. |
| [FR-029](#fr-029) | Medium | Medium | Retained as Medium. Recurring scheduling and Excel/HTML/CSV output formats are directly supported, but the sources do not frame them as critical versus on-demand manual reporting. |
| [FR-030](#fr-030) | High | High | Retained as High. Board/executive reporting is explicitly requested with specific activity measures and cross-tabs, indicating a core external reporting need. |
| [FR-031](#fr-031) | Medium | Medium | Retained as Medium. Historical reporting is valuable, but the sources do not fully define coverage/latency semantics, so urgency is moderate rather than essential. |
| [FR-032](#fr-032) | Medium | Medium | Retained as Medium. Including null/blank fields, and showing report name and selected date criteria improves interpretability, but it is framed as a quality/reporting completeness enhancement. |
| [FR-033](#fr-033) | Medium | Medium | Retained as Medium. The distinction between last edit vs last circulation is clearly requested for reporting accuracy, but it does not appear as a core system-wide operational obligation. |
| [FR-034](#fr-034) | Medium | Medium | Retained as Medium. Online hierarchical help and actionable error feedback are valuable for reducing reliance on IT and improving troubleshooting, but not presented as core reporting functionality. |
| [IR-002](#ir-002) | High | High | Retained as High. Access via web browser or Windows-compatible client (with explicit browser version conditions when browser access is used) is stated as a required operating-environment requirement. |
| [IR-003](#ir-003) | Low | Low | Retained as Low. Vendor interface support is described as conditional/dependency-based (not available at every library) rather than universally required. |
| [IR-004](#ir-004) | High | High | Retained as High. The sources state that reporting must be able to query OPAC-created holds/circulation transactions, making it essential for report correctness. |
| [NFR-001](#nfr-001) | High | High | Retained as High. The sources explicitly require that reporting not disrupt OPAC/circulation and emphasize open-hours responsiveness; this is a core system constraint. |
| [NFR-002](#nfr-002) | High | High | Retained as High. The sources state consortium operating scale as a must-support environment, making it a foundational quality/performance context. |
| [NFR-003](#nfr-003) | High | High | Retained as High. Accessibility is described as non-negotiable (legal requirement language), and privacy constraints are explicitly supported for demographic reporting and archives. |
| [NFR-004](#nfr-004) | High | High | Retained as High. Meeting minutes require a fully relational database back end and standards-compliant HTML for web components and report/help output. |
| [AR-001](#ar-001) | High | High | Retained as High. The sources identify Linux/Solaris server operation as a required environment condition with explicit dual-site expectation. |
| [AR-002](#ar-002) | Medium | Medium | Retained as Medium. Separate dev/training environments and configuration migration are important for safe operations, but the sources do not provide certainty about the underlying technical mechanism, supporting Medium priority. |
| [AR-003](#ar-003) | High | High | Retained as High. The sources require compliance with auditing and enforce data-retention policies; the exact retention duration is uncertain, but the obligation itself is high-priority. |
| [AR-004](#ar-004) | Medium | Medium | Retained as Medium. Documentation/data specifications are necessary for correct operations and maintenance, but are not described as core runtime report/reporting functionality. |

## Traceability and Verification

References below point to supplied source documents. Semantic support is checked by Reviewer; related requirement links are supplementary.

| Requirement | Related requirements | Source documents |
| --- | --- | --- |
| [FR-001](#fr-001) | [FR-031](#fr-031) | [conversations/conv\_pines014\_material\_volume.eml](../../../data/corpus/conversations/conv_pines014_material_volume.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [IR-001](#ir-001) | [FR-002](#fr-002) | [conversations/conv\_pines015\_capacity\_interface.eml](../../../data/corpus/conversations/conv_pines015_capacity_interface.eml) |
| [FR-002](#fr-002) | [IR-001](#ir-001) | [conversations/conv\_pines015\_capacity\_interface.eml](../../../data/corpus/conversations/conv_pines015_capacity_interface.eml) |
| [FR-003](#fr-003) | — | [conversations/conv\_pines016\_shelf\_space.eml](../../../data/corpus/conversations/conv_pines016_shelf_space.eml) |
| [FR-004](#fr-004) | [FR-005](#fr-005), [FR-006](#fr-006) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-005](#fr-005) | [FR-004](#fr-004) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-006](#fr-006) | [FR-004](#fr-004), [FR-005](#fr-005) | [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml) |
| [FR-007](#fr-007) | [FR-017](#fr-017) | [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-008](#fr-008) | [FR-009](#fr-009) | [conversations/conv\_pines019\_020\_missing\_intransit.eml](../../../data/corpus/conversations/conv_pines019_020_missing_intransit.eml) |
| [FR-009](#fr-009) | [FR-008](#fr-008) | [conversations/conv\_pines019\_020\_missing\_intransit.eml](../../../data/corpus/conversations/conv_pines019_020_missing_intransit.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-010](#fr-010) | [FR-011](#fr-011), [FR-012](#fr-012) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-011](#fr-011) | [FR-010](#fr-010) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-012](#fr-012) | [FR-010](#fr-010), [FR-013](#fr-013) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-013](#fr-013) | [FR-014](#fr-014) | [conversations/conv\_pines022\_deletions.eml](../../../data/corpus/conversations/conv_pines022_deletions.eml); [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-014](#fr-014) | [FR-013](#fr-013) | [conversations/conv\_pines021\_item\_purging.eml](../../../data/corpus/conversations/conv_pines021_item_purging.eml) |
| [FR-015](#fr-015) | [FR-016](#fr-016) | [conversations/conv\_pines023\_patron\_characteristics.eml](../../../data/corpus/conversations/conv_pines023_patron_characteristics.eml) |
| [FR-016](#fr-016) | [FR-015](#fr-015), [NFR-001](#nfr-001) | [conversations/conv\_pines024\_inactive\_patrons.eml](../../../data/corpus/conversations/conv_pines024_inactive_patrons.eml) |
| [FR-017](#fr-017) | [FR-018](#fr-018), [FR-019](#fr-019) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-018](#fr-018) | [AR-003](#ar-003), [NFR-003](#nfr-003) | [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-019](#fr-019) | [NFR-003](#nfr-003) | [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-020](#fr-020) | [FR-021](#fr-021), [AR-003](#ar-003) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-021](#fr-021) | [FR-020](#fr-020) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-022](#fr-022) | [FR-020](#fr-020), [AR-003](#ar-003) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml) |
| [FR-023](#fr-023) | [FR-012](#fr-012) | [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-024](#fr-024) | [FR-025](#fr-025), [FR-026](#fr-026) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt) |
| [FR-025](#fr-025) | [FR-015](#fr-015), [FR-024](#fr-024) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-026](#fr-026) | [FR-024](#fr-024), [FR-027](#fr-027) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [email\_staff\_login.eml](../../../data/corpus/email_staff_login.eml) |
| [FR-027](#fr-027) | [FR-026](#fr-026) | [email\_staff\_login.eml](../../../data/corpus/email_staff_login.eml) |
| [FR-028](#fr-028) | [FR-029](#fr-029), [NFR-001](#nfr-001) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [evergreen\_reference\_2009.txt](../../../data/corpus/evergreen_reference_2009.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-029](#fr-029) | [FR-028](#fr-028) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [FR-030](#fr-030) | [FR-017](#fr-017) | [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-031](#fr-031) | [FR-001](#fr-001), [FR-003](#fr-003), [FR-020](#fr-020) | [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-032](#fr-032) | [FR-025](#fr-025) | [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [FR-033](#fr-033) | [FR-023](#fr-023) | [interview\_cataloging\_2009-05-08.txt](../../../data/corpus/interview_cataloging_2009-05-08.txt) |
| [FR-034](#fr-034) | [NFR-003](#nfr-003) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [IR-002](#ir-002) | [NFR-003](#nfr-003) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [IR-003](#ir-003) | — | [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [IR-004](#ir-004) | [NFR-001](#nfr-001), [FR-017](#fr-017) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt) |
| [NFR-001](#nfr-001) | [FR-028](#fr-028), [NFR-002](#nfr-002) | [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt); [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt) |
| [NFR-002](#nfr-002) | [NFR-001](#nfr-001) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt) |
| [NFR-003](#nfr-003) | [FR-019](#fr-019), [AR-003](#ar-003) | [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt); [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt) |
| [NFR-004](#nfr-004) | [IR-002](#ir-002) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |
| [AR-001](#ar-001) | — | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt) |
| [AR-002](#ar-002) | [FR-024](#fr-024), [FR-026](#fr-026) | [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt); [interview\_sysadmin\_2009-05-10.txt](../../../data/corpus/interview_sysadmin_2009-05-10.txt) |
| [AR-003](#ar-003) | [FR-018](#fr-018), [FR-020](#fr-020), [FR-022](#fr-022), [NFR-003](#nfr-003) | [email\_financial\_reports.eml](../../../data/corpus/email_financial_reports.eml); [email\_report\_features.eml](../../../data/corpus/email_report_features.eml) |
| [AR-004](#ar-004) | [FR-025](#fr-025) | [meeting\_minutes/meeting\_2009-07-20\_minutes.txt](../../../data/corpus/meeting_minutes/meeting_2009-07-20_minutes.txt); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt) |

## Blacklist

### BL-001 — Capacity color coding

A tentative visual suggestion, not a confirmed capacity-interface obligation.

**Reason discarded:** The suggestion was phrased as “Maybe,” was not included in the consolidated interface summary, and depends on a capacity measure that the sources leave unresolved. It is therefore not accepted as a requirement.

**Sources:** [conversations/conv\_pines015\_capacity\_interface.eml](../../../data/corpus/conversations/conv_pines015_capacity_interface.eml)

### BL-002 — Revert transfer on destination checkout

Treating checkout at the destination as a definite automatic reversion trigger.

**Reason discarded:** The discussion gives conflicting meanings: one message lists checkout as an event trigger, but the same discussion explains that checked-out items should stay at the destination and unused items should return. The accepted transfer requirement does not assume this trigger until stakeholders clarify the intended behavior.

**Sources:** [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml)

### BL-003 — Seven-day default for in-transit report

Set the configurable in-transit threshold to a seven-day default.

**Reason discarded:** Seven days was suggested as a probable default, not confirmed. The consolidated clarification requires a configurable threshold but does not establish a default value.

**Sources:** [conversations/conv\_pines019\_020\_missing\_intransit.eml](../../../data/corpus/conversations/conv_pines019_020_missing_intransit.eml)

### BL-004 — Specific database implementation for transfer logging and safety

Mandate database triggers, audit tables, transaction-safety mechanisms, or smaller transfer batches as specified implementation choices.

**Reason discarded:** These were technical suggestions in discussion, not confirmed stakeholder obligations. The accepted transfer requirements retain supported behavior and the general non-disruption constraint without prescribing those designs.

**Sources:** [conversations/conv\_pines018\_item\_transfer.eml](../../../data/corpus/conversations/conv_pines018_item_transfer.eml)

### BL-005 — Date-range filters for missing/damaged report

Make date-range filters mandatory for missing/damaged reports.

**Reason discarded:** Date ranges were proposed as technically feasible and useful, but are not confirmed as a stakeholder obligation in the consolidated report clarification. Item condition notes are retained in FR-008 because they were directly requested and not explicitly rejected.

**Sources:** [conversations/conv\_pines019\_020\_missing\_intransit.eml](../../../data/corpus/conversations/conv_pines019_020_missing_intransit.eml)

### BL-006 — Track denied deletions and mandatory deletion reason

Require tracking denied deletion attempts or recording a deletion reason as standard deletion-log fields.

**Reason discarded:** Denied attempts are described as helpful, and deletion reason is raised as a possibility; neither is included in the consolidated deletion-tracking fields. Completed deletion details are retained in FR-013.

**Sources:** [conversations/conv\_pines022\_deletions.eml](../../../data/corpus/conversations/conv_pines022_deletions.eml)

### BL-007 — Draft-only report interface and scheduling details

Treat the external draft's canned, on-demand, and open-template interface types, combined execution in one document, permission-based addition of canned reports, full listed scheduling frequencies, and comparative-period output as mandatory accepted requirements.

**Reason discarded:** These details appear in the external draft but are not clearly adopted by stakeholder discussions or summaries. The consolidator does not treat that draft as automatically authoritative. Supported stakeholder requests for templates, cloning, recurring scheduling, and Excel/HTML/CSV outputs remain in FR-024 and FR-029. Candidate IDs supporting those retained requirements have been removed from this blacklist entry.

**Sources:** [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt); [email\_report\_features.eml](../../../data/corpus/email_report_features.eml); [meeting\_tech\_subcommittee\_2009-06-30.txt](../../../data/corpus/meeting_tech_subcommittee_2009-06-30.txt)

### BL-008 — Unspecified or unadopted report features as mandatory scope

Treat every example, survey preference, or incompletely specified capability in the draft or reference sources as a confirmed mandatory feature, including unspecified real-time latency, pivot-table behavior, email delivery, and report fields not defined in the corpus.

**Reason discarded:** The sources include examples and preferences without complete scope, criteria, or acceptance decisions. These cannot be converted into precise mandatory obligations without inventing decisions. Separately supported and adopted reporting obligations remain represented in the requirements. Candidate IDs for retained requirements are excluded from this entry.

**Sources:** [early\_draft\_srs\_galecia.txt](../../../data/corpus/early_draft_srs_galecia.txt); [survey\_results\_2009.txt](../../../data/corpus/survey_results_2009.txt)

## Source Resolution Decisions

- Merged semantically overlapping candidates while preserving distinct scopes and conditions. Candidate IDs remain supporting metadata; evidence excerpts trace requirements to original source documents.
- Applied reviewer feedback to FR-012: retained accepted last-copy reporting at library and system scope, but removed the deleted-last-copy reporting detail because support for that detail appears only in the external draft and no later stakeholder adoption is present.
- Applied reviewer feedback to FR-017: removed hold-status subtotals such as active, frozen, and frozen-until because their support appears only in the external draft, not in the stakeholder survey summary or later consolidated stakeholder requirements.
- Applied reviewer feedback to NFR-002: removed the batch-locking/processing obligation and its candidate reference. The source describes smaller batches as a technical suggestion, not an adopted requirement; the consortium-scale constraint remains.
- Applied reviewer feedback to FR-020: restored the direct request that front-desk payments be reflected immediately in the system, while noting that no more precise update-time measure is supplied.
- Applied reviewer feedback to BL-007 and BL-008: removed candidate IDs that support retained requirements from blacklist entries, including accepted template and scheduling candidates. The blacklist now refers only to rejected or unadopted details.
- The January draft and reference materials provide context but do not automatically establish accepted requests. Draft-only features without clear stakeholder or meeting adoption are excluded; details directly supported by later stakeholder discussion or meeting records remain in scope.
- Capacity is accepted as an all-branch interface and drill-down obligation, but the meaning of capacity remains unresolved because stakeholders list alternative measures without selecting one. Sorting, filtering, trends, and CSV export are separately supported requests.
- For last-copy reporting, both library and system scope are retained because a participant explicitly requests both and the later system-wide emphasis does not reject the library view. WorldCat support means assisting catalogers with updates; no integration contract is present.
- The seven-day in-transit threshold is not adopted as a default because it was only described as probable and omitted from the consolidated requirement. The transfer-on-checkout trigger is excluded pending clarification because source messages conflict.
- Purge candidate reports, separate deletion confirmation, and purge audit trails are retained as distinct safeguards. General deletion tracking is separate because the sources distinguish purge operations from record deletions and provide distinct audit details.
- Digital-resource access is included in the inactive-patron activity definition when digital-collection integration or event data is available, as explicitly stated in the discussion. The availability condition remains explicit.
- Financial-retention sources give an unspecified X-year legal period and a separate statement that some data need seven years. The set retains enforcement of applicable policies but does not apply seven years universally or invent which records it covers.
- The cataloging interview's last-edit-date obligation is retained as FR-033: the reported edit date must exclude last circulation.
- Queue visibility and prioritization are kept together in FR-028; priority display and the ability for selected important reports to move ahead are included, while a complete ordering policy remains unspecified.
- FR-023 is limited to the three data-quality report checks explicitly requested in the cataloging interview. Other broad report families listed only as examples or existing-system gaps are not thereby treated as accepted requirements.
- Documentation requirements are retained as AR-004 because they are operational documentation deliverables; the ID prefix matches the AR category.
- No source establishes mandatory WorldCat integration, a specific reporting-warehouse implementation, report caching, transfer database design, or precise query/report performance thresholds. Such proposals are not stated as requirements.
- Scope follows the working-group minutes: management reporting and analysis are included; day-to-day OPAC and circulation-client functions are excluded. The OPAC is nevertheless protected from reporting impact, and OPAC-created data may be queried for reports.
- The requested system-average comparison for shelf-space reporting is retained in FR-003, supported by the statement that branch managers need to compare local circumstances with the system average.
- Sorting the combined in-transit report by due date is retained in FR-009 because a stakeholder explicitly requests it to help staff pursue the oldest items first.
- Item condition notes are retained in FR-008 because they were directly requested and no source explicitly rejects them. The proposed date-range filter remains excluded as an unconfirmed enhancement.
