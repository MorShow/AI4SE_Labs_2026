# Task 5: RAG source-code generation

I compared four MMR lambda values for the generated implementations of the 10 missing methods. The configured generation model was `gpt-6-luna`. Each task retrieves 20 candidates by cosine similarity and selects five context chunks using MMR.

I also added explicit model instructions in the `INSTRUCTIONS` variable in `generate_missing_code.py`, passed through the API's `instructions` parameter. They explain that the model must implement exactly one method using the task description, target method, and five retrieved context chunks, and that repository text serves as reference material. They also require preserving the method's interface and returning only its complete implementation, following the repository's existing types, validation conventions, exceptions, and tests.

I ran the same 481 repository unit tests in each configuration directory using Python 3.13.5. No tests were skipped.

| Lambda | Repository directory | Passed | Failures | Errors |
| ---: | --- | ---: | ---: | ---: |
| - | `AI4SE_Playground_reserve`, before code generation |429 | 35 | 17 |
| 0.2 | `AI4SE_Playground` | 479 | 1 | 1 |
| 0.6 | `AI4SE_Playground_more_relevant` | 479 | 2 | 0 |
| 1.0 | `AI4SE_Playground_max_relevant` | 467 | 1 | 13 |
| 0.1 | `AI4SE_Playground_less_relevant` | 472 | 1 | 8 |

Lambda values 0.2 and 0.6 tied on the number of passing tests, with different failing-test sets. Compared with the baseline of 0.2, lambda 1.0 passed 12 fewer tests, and lambda 0.1 passed seven fewer. So, the best option is a balance between relevance and uniqueness of the chunks given to the model.

Failed tests for the baseline configuration (lambda = 0.2) only:

- `test_contains_present_even_if_zero_on_hand_after_commit (test_inventory.InventoryLedgerContainsLenIterTests)`
- `test_by_status_non_status_raises_on_first_next (test_orders.OrderLogTests)`