# Task 8 — Repository Cloning Rule

- Created a project-local Codex rule in [no-clone.rules](../../../.codex/rules/no-clone.rules) that sets `decision = "forbidden"` for the command prefix `git clone`. The rule file is shown in [rule_file.png](rule_file.png).
- Checked the rule with `codex execpolicy check`, which returned `forbidden` for a sample clone command. The rule also contains matching examples and examples of other Git commands.
- Asked Codex to clone `Neltharion59/AI4SE_Playground` into `Week_08_Dissecting/solutions`. The conversation screenshot records Codex reporting that automatic approval review rejected cloning with the rule's justification. [Conversation evidence](result.png)
