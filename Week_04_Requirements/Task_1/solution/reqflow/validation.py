from collections import Counter

from .schemas import (
    OverallPriorities, RequirementSet,
    PriorityAssessment, Review, ReviewIssue, SourceChunk, Spec,
)


def issue(spec: Spec, message: str, *ids: str) -> ReviewIssue:
    return ReviewIssue(spec=spec, severity="Critical", requirement_ids=list(ids), source_ids=[], message=message)


def validate_set(draft: RequirementSet, sources: list[SourceChunk]) -> list[ReviewIssue]:
    errors: list[ReviewIssue] = []
    source_map = {source.id: source for source in sources}
    ids = [req.id for req in draft.requirements]
    blacklist_ids = [entry.id for entry in draft.blacklist]
    for req_id, count in Counter(ids + blacklist_ids).items():
        if count > 1:
            errors.append(issue("OS2", "Duplicate ID.", req_id))
    known_ids = set(ids)
    for req in draft.requirements:
        if not req.id.startswith(req.category + "-"):
            errors.append(issue("OS2", "ID prefix must match category.", req.id))
        if (req.category == "AR") != (req.additional_type is not None):
            errors.append(issue("OS1", "Only AR requires a non-null additional_type.", req.id))
        for related in req.related_requirement_ids:
            if related not in known_ids or related == req.id:
                errors.append(issue("OS4", f"Invalid related requirement ID {related}.", req.id))
    for entry in [*draft.requirements, *draft.blacklist]:
        for evidence in entry.evidence:
            if evidence.source_id not in source_map:
                errors.append(issue("OS4", f"Unknown source ID {evidence.source_id}.", entry.id))
    return errors


def gate_review(review: Review, draft: RequirementSet, structural: list[ReviewIssue]) -> Review:
    issues = review.issues + structural
    counts = Counter(item.severity for item in issues)
    approved = counts["Critical"] == 0 and counts["Medium"] < 3
    recommendations = {item.requirement_id: item for item in review.priority_assessments}
    assessments = [
        recommendations.get(req.id, PriorityAssessment(
            requirement_id=req.id, business_priority=req.business_priority, rationale=req.priority_reason,
        )) for req in draft.requirements
    ] if approved else []
    return review.model_copy(update={
        "approved": approved,
        "issues": issues,
        "priority_assessments": assessments,
    })


def validate_priorities(priorities: OverallPriorities, draft: RequirementSet) -> list[str]:
    errors = []
    expected = {req.id for req in draft.requirements}
    actual = [item.requirement_id for item in priorities.items]
    missing = sorted(expected - set(actual))
    unexpected = sorted(set(actual) - expected)
    duplicates = sorted(req_id for req_id, count in Counter(actual).items() if count > 1)
    if missing:
        errors.append(f"Add missing approved requirement IDs: {', '.join(missing)}.")
    if unexpected:
        errors.append(f"Remove unapproved requirement IDs: {', '.join(unexpected)}.")
    if duplicates:
        errors.append(f"Keep exactly one item for repeated requirement IDs: {', '.join(duplicates)}.")
    return errors
