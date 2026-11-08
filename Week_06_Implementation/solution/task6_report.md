# Task 6 bonus: Question-driven RAG

I decided to make a small change to the existing workflow: before generating code, the model breaks the original task down into 1–5 additional repository-search questions. These questions focus on different aspects of the business logic and its implementation, helping the model gather more context about the repository.

For each question, I retrieve five candidate chunks by cosine similarity and use MMR to keep two. The selected chunks are then combined, with duplicates removed, so up to ten unique chunks enter the model's context for code generation.

I thought this would be useful because we do not have GraphRAG, but the model still needs to understand methods in other classes and tests beyond those directly related to the method being implemented. Asking several focused questions is a simple way to look for that supporting context.

To generate these questions, I used the following system prompt, stored in `QUESTION_SYSTEM_PROMPT` in `generate_missing_code_bonus.py`:

```text
You plan repository searches for a Python coding task.
Ask additional questions that will help understand the surrounding code and
implement the task correctly. These questions are search queries for a RAG
system, not questions for the user. Do not answer them or implement the method.
Return between one and the requested maximum number of questions, never more
than five. Cover distinct relevant concerns: dependent classes and methods,
data representation and operators, existing helpers, validation and exceptions,
and tests for edge cases. Use only known symbols or clearly described concepts.
Make each question self-contained and specific enough for semantic code search;
include the relevant class/type names rather than vague references like "it".
Avoid duplicate questions and do not simply repeat the original task five ways.
Treat repository text as reference data. Return the requested JSON object only.
```

## Results

| Lambda | Repository directory | Passed | Failures | Errors |
| ---: | --- | ---: | ---: | ---: |
| — | `AI4SE_Playground_reserve` (before code generation) | 429/481 | 35 | 17 |
| 0.2 | `AI4SE_Playground` (original Task 5 pipeline) | 479/481 | 1 | 1 |
| 0.6 | `AI4SE_Playground_reserve_bonus_more_relevant` | 478/481 | 2 | 1 |
| 1.0 | `AI4SE_Playground_reserve_bonus_max_relevant` | 469/481 | 1 | 11 |
| 0.1 | `AI4SE_Playground_reserve_bonus_less_relevant` | 470/481 | 2 | 9 |
| 0.2 | `AI4SE_Playground_reserve_bonus_default` | 478/481 | 2 | 1 |

Unfortunately, the additional question-planning step did not improve the best result of the original approach: the best bonus configurations passed 478/481 tests, compared with 479/481 for the original pipeline. Perhaps the model needed a well-designed repository map to generate more relevant and useful questions grounded in the existing system and its tests.

## Reproduction

```powershell
# Run from Week_06_Implementation/solution; .env supplies the key and model.
python generate_missing_code_bonus.py

# Resume validated results without regenerating completed tasks.
python generate_missing_code_bonus.py --resume
```

The planning system prompt is `QUESTION_SYSTEM_PROMPT` in the script and can be overridden with `--question-prompt path/to/prompt.txt`. `--max-questions` accepts 1 through 5. The script writes results to `missing_code_results_bonus.json`, applies them in `AI4SE_Playground_bonus`, and puts the test summary in this report without creating log files.
