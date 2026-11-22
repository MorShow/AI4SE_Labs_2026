# Task 5 Report

- Created the repository-scoped Codex skill [`analyze-file`](../../../.agents/skills/analyze-file/SKILL.md), with [UI metadata](../../../.agents/skills/analyze-file/agents/openai.yaml). It analyzes assignment descriptions, source code, and other files for quick orientation.
- The output contains a brief introduction, exactly five main bullet points of one to three short sentences each, and brief closing context. The skill adapts its analysis to the file type and answers in the student's language for conversational explanations.
- Adapted the analysis idea from Task 2's [`/prompts:check-task`](../../../.codex/prompts/check-task.md) into a broader file-analysis workflow. Added scoped read-only context searches, guidance for code behavior and assignment requirements, and explicit handling of incomplete context; the original slash command remains available.
- Replaced the earlier `check-task` skill with `.agents/skills/analyze-file/`, following [OpenAI's repository skill structure](https://learn.chatgpt.com/docs/build-skills). Added the required [`filler_Task_5.md`](filler_Task_5.md) containing the exact AI4SE marker line.
- Validation: the bundled `quick_validate.py` returned `Skill is valid!`; UI metadata, local report links, and the marker file were checked. These checks validate structure and references; discovery and automatic invocation in a fresh Codex session were not tested.

## Usage

1. Invoke `$analyze-file Week_08_Dissecting/Assignments/Task_5/Task_5.md` to analyze an assignment, or pass a source-code path instead.
2. Codex reads the file and relevant supporting context, then returns the compact five-point explanation without modifying or executing the analyzed files.
