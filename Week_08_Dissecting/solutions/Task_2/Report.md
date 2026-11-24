# Task 2 Custom Slash Command

I used OpenAI Codex. Commands such as `/init` are built into Codex. To create a custom workflow that can run scripts, Codex supports **skills**, which combine reusable instructions with optional scripts and resources. [Skills documentation](https://learn.chatgpt.com/docs/build-skills)

For this task, I chose a simpler custom prompt, `/prompts:check-task`, instead of creating a skill. It provides reusable instructions to read an assignment, identify requirements, and plan the implementation. Its Markdown file can be created using PowerShell, but the command itself runs inside Codex. Custom prompts are deprecated in favor of skills. [Custom prompts documentation](https://learn.chatgpt.com/docs/custom-prompts)

[Screenshot](image.png)
