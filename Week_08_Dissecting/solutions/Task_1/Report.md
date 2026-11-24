# Task 1 – Customizing the Codex Prompt

- We used OpenAI Codex.

There were three ways to do it in Codex:
1. **`AGENTS.md`**. Create an `AGENTS.md` file at the repository root and write the project instructions in it. Codex loads them alongside the base prompt when starting a session in the repository.
2. **`developer_instructions`**. Set `developer_instructions` to the desired text as a top-level setting in `config.toml`. Codex adds the text to the session as a separate developer message alongside its base prompt.
3. **`model_instructions_file`**. Save an edited copy of the full base prompt in a Markdown file and set `model_instructions_file` in `config.toml` to its path. Start a new session so Codex loads that file as the base prompt.


- We chose `model_instructions_file` and set it in `.codex/config.toml`. We asked Codex to identify the assignment's week and task number and, after completing the assignment, create `solutions/Task_j/filler_Task_j.md` containing only `=== AI4SE line ===`. [Screenshot of the change](image.png)
