---
name: analyze-file
description: Analyze assignment descriptions, source code, or other files and provide a quick orientation with exactly five short main bullet points and brief surrounding context. Use for concise file explanations or overviews rather than implementation or exhaustive reviews.
---

# Analyze File

Help the reader quickly understand the supplied file or related set of files.
Accept explicit paths or files clearly identified in the conversation. If the
target is unclear, ask which file to analyze; do not arbitrarily choose between
assignments with the same number in different weeks.

## Gather context

1. Read applicable repository instructions and the target file. Use a format-
   appropriate reader for non-text files. For a large file, inspect its structure
   and relevant sections; disclose partial coverage instead of implying a full review.
2. Read only context needed to explain it: referenced assignment inputs, a caller
   or imported interface, nearby setup documentation, or a relevant test. Avoid
   loading the whole repository.
3. Keep analysis read-only. Do not execute analyzed code, install dependencies,
   change files, or complete an assignment merely to explain it. Distinguish
   observed content from inference and flag missing context briefly.

Useful PowerShell commands from the repository root; replace the examples with
the requested task number, paths, and symbols, and run only relevant commands:

```powershell
rg --files --hidden -g 'AGENTS.md' -g '*Task_5*' -g '!.git/**' -g '!.venv/**'
Get-Content -LiteralPath 'AGENTS.md'
Get-Content -LiteralPath 'Week_08_Dissecting/Assignments/Task_5/Task_5.md'
# For Python code, locate definitions and references in the relevant module.
rg -n '^(class |def |async def )' 'path/to/module.py'
rg -n -F 'symbol_name' 'path/to/relevant/module'
```

Check that paths exist, keep searches scoped, and use native file search if
`rg` is unavailable. No search matches does not establish absent behavior.

## Select the five main points

Choose the most useful facts for understanding this particular file. Avoid
padding simple files with invented complexity or repeating the introduction.

- **Assignments:** prioritize the goal, required work, inputs or prerequisites,
  deliverables, and constraints or completion criteria. Preserve exact names,
  point values, and tool restrictions when relevant. Distinguish optional advice
  and conditional alternatives from actual requirements.
- **Code:** prioritize purpose, inputs and outputs, main control or data flow,
  dependencies and integration, and significant edge cases or limitations.
  Explain actual behavior and side effects. Comments do not prove implementation;
  do not claim runtime correctness without observed execution.
- **Other files:** adapt the points to purpose, structure, key content,
  relationships, and practical implications. For multiple files, synthesize their
  relationship in five total points unless separate analyses are requested.

## Response format

Answer in the user's language unless requested otherwise. Follow repository
language rules when explicitly asked to save an assessment artifact.

Start with one or two short sentences identifying the file, its role, and its
project context. Then provide **exactly five top-level bullet points**, each
with a short descriptive lead and **one to three short sentences**. Prefer one
sentence and avoid sublists. Link to relevant files or code locations where useful.

Finish with one or two short sentences connecting the points: what to understand
first, a practical implication, or an unresolved limitation. Do not append another
checklist or tutorial. Aim for roughly 150-250 words, less for simple files.
Save the explanation only if the user explicitly requests a file.
