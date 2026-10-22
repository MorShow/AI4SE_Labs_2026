import json
import logging
from typing import Any, TypeVar

from openai import OpenAI
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)
LOG = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self, max_input_chars: int) -> None:
        self.client = OpenAI(timeout=180.0, max_retries=2)
        self.max_input_chars = max_input_chars

    def generate(
        self, role: str, model: str, system: str, payload: dict[str, Any],
        schema: type[T], *, max_output_tokens: int,
    ) -> T:
        content = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        if len(system) + len(content) > self.max_input_chars:
            raise ValueError(
                f"{role} input exceeds {self.max_input_chars} characters. "
                "Reduce corpus size or deliberately increase --max-input-chars after checking model limits."
            )
        for attempt in range(2):
            LOG.info("%s: calling %s (max_output_tokens=%s)", role, model, max_output_tokens)
            # Defer schema parsing until the API's completion status has been checked.
            raw = self.client.responses.with_raw_response.parse(
                model=model, instructions=system, input=content, text_format=schema,
                max_output_tokens=max_output_tokens, store=False,
            )
            body = raw.http_response.json()
            status = body.get("status")
            reason = (body.get("incomplete_details") or {}).get("reason")
            if status == "incomplete" and reason == "max_output_tokens" and attempt == 0:
                max_output_tokens *= 2
                LOG.warning("%s: output truncated; retrying once with max_output_tokens=%s",
                            role, max_output_tokens)
                continue
            if status != "completed":
                raise RuntimeError(
                    f"{role} ({model}) did not complete: status={status}, reason={reason}, "
                    f"max_output_tokens={max_output_tokens}, response_id={body.get('id')}; "
                    "no partial result was accepted."
                )
            try:
                result = raw.parse().output_parsed
            except ValidationError as error:
                raise RuntimeError(
                    f"{role} ({model}) returned invalid {schema.__name__} despite status=completed "
                    f"(response_id={body.get('id')}); no result was accepted."
                ) from error
            if result is None:
                raise RuntimeError(f"{role} returned no parsed output (status={status}); no result was accepted.")
            return result
