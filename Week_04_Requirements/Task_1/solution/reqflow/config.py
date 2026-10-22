from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    extractor_model: str = "gpt-6-luna"
    consolidator_model: str = "gpt-6-luna"
    reviewer_model: str = "gpt-5.6-luna"
    architect_model: str = "gpt-5.4-nano"
    max_revisions: int = 5
    chunk_chars: int = 14000
    max_input_chars: int = 4000000
    use_cache: bool = True

    def __post_init__(self) -> None:
        models = self.models()
        if any(not model.strip() for model in models.values()):
            raise ValueError("Model names must not be empty.")
        if len(set(models.values())) < 3:
            raise ValueError("ANS4 requires at least three distinct model names.")
        if self.max_revisions < 0:
            raise ValueError("max_revisions must be non-negative.")
        if self.chunk_chars < 1000 or self.max_input_chars < self.chunk_chars:
            raise ValueError("Use chunk_chars >= 1000 and max_input_chars >= chunk_chars.")

    def models(self) -> dict[str, str]:
        return {
            "extractor": self.extractor_model,
            "consolidator": self.consolidator_model,
            "reviewer": self.reviewer_model,
            "architect": self.architect_model,
        }
