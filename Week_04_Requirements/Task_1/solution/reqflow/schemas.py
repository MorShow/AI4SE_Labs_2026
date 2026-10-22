from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Category = Literal["FR", "NFR", "IR", "AR"]
Priority = Literal["High", "Medium", "Low"]
Spec = Literal["OS1", "OS2", "OS3", "OS4", "OS5", "OS6", "OS7", "OS8", "OS9"]
SPECS: tuple[Spec, ...] = ("OS1", "OS2", "OS3", "OS4", "OS5", "OS6", "OS7", "OS8", "OS9")


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SourceChunk(Record):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)
    id: str
    document: str
    start_line: int
    end_line: int
    text: str

    def numbered_text(self) -> str:
        return "\n".join(
            f"L{number}: {line}"
            for number, line in enumerate(self.text.splitlines(), self.start_line)
        )


class Evidence(Record):
    source_id: str
    quote: str = Field(min_length=1, description="Supporting excerpt or faithful paraphrase; Reviewer checks its meaning against the source.")


class ExtractedCandidate(Record):
    name: str = Field(min_length=1)
    description: str = Field(min_length=20)
    category: Category
    evidence: list[Evidence] = Field(min_length=1)


class Extraction(Record):
    candidates: list[ExtractedCandidate]
    no_requirements_reason: str = Field(description="Explain an empty extraction; otherwise use an empty string.")


class Candidate(ExtractedCandidate):
    id: str


class Requirement(Record):
    id: str = Field(pattern=r"^(FR|NFR|IR|AR)-[0-9]{3,}$")
    name: str = Field(min_length=1)
    description: str = Field(min_length=20, description="One explanatory paragraph, preserving conditions and exceptions.")
    category: Category
    additional_type: Literal["Operational", "Legal", "Deployment", "Other"] | None
    business_priority: Priority
    priority_reason: str = Field(min_length=1)
    candidate_ids: list[str] = Field(description="All contributing candidate IDs; empty only for a recovered omission.")
    evidence: list[Evidence] = Field(min_length=1)
    related_requirement_ids: list[str]


class BlacklistEntry(Record):
    id: str = Field(pattern=r"^BL-[0-9]{3,}$")
    name: str = Field(min_length=1)
    description: str = Field(min_length=20)
    reason: str = Field(min_length=1)
    candidate_ids: list[str]
    evidence: list[Evidence] = Field(min_length=1)


class RequirementSet(Record):
    title: str = Field(min_length=1)
    scope: str = Field(min_length=1)
    requirements: list[Requirement] = Field(min_length=1)
    blacklist: list[BlacklistEntry]
    decisions: list[str] = Field(description="Explain source conflicts and their resolution; do not invent source authority.")


class ReviewIssue(Record):
    spec: Spec
    severity: Literal["Critical", "Medium", "Low"]
    requirement_ids: list[str]
    source_ids: list[str]
    message: str = Field(min_length=1, description="Concrete issue and requested correction, with source evidence where relevant.")


class SpecCheck(Record):
    spec: Spec
    passed: bool
    explanation: str = Field(min_length=1)


class PriorityAssessment(Record):
    requirement_id: str
    business_priority: Priority
    rationale: str = Field(min_length=1)


class Review(Record):
    approved: bool
    checks: list[SpecCheck]
    issues: list[ReviewIssue]
    priority_assessments: list[PriorityAssessment] = Field(
        description="Empty when rejected. On approval give priority recommendations for accepted requirements; unchanged priorities may be omitted."
    )


class OverallPriorityAssessment(Record):
    requirement_id: str
    overall_priority: Priority
    rationale: str = Field(min_length=1, description="Explain the overall priority using business value and the developer perspective.")


class OverallPriorities(Record):
    items: list[OverallPriorityAssessment] = Field(description="One overall priority per approved requirement; item order has no meaning.")
