# Task 4 Custom Codex Profile

- I created the `ai4se-review` profile for Codex CLI in `ai4se-review.config.toml`. The profile selects `gpt-6.2-sol`, sets `model_reasoning_effort` to `high`, and sets `model_verbosity` to `medium`.
- The profile configuration is shown in [ai4se_profile.png](ai4se_profile.png). The Codex CLI session in [result.png](result.png) displays GPT-6.2-Sol with high reasoning effort.

## Creating and using the profile

1. Create `%USERPROFILE%\.codex\ai4se-review.config.toml`.
2. Set `model = "gpt-6.2-sol"`, `model_reasoning_effort = "high"`, and `model_verbosity = "medium"` on separate lines and save the file.
3. Start Codex with `codex --profile ai4se-review`.
