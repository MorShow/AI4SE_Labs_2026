# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 4.5b out of 5b
- Commentary: The student delivers a strong, end-to-end Text2SQL prompt-comparison pipeline. Task 1 provides three well-crafted framework prompts (CRISP, RACE, ToT) with solid reasoning. Task 2 generates predictions with measured inference times and an interactive dashboard report. Task 3 proposes the Soft Execution F1 metric, implements it alongside Jaccard, and compares values across prompts. Task 4 produces a sophisticated interactive dashboard with multiple tables and graphs and good interpretation, though it omits the requested statistical-significance testing for prompt differences.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: The student chose three prompting frameworks — CRISP, RACE, and Tree-of-Thoughts (ToT) — none of which is ROSES or zero-shot. The `prompts.yml` file contains three detailed, well-structured prompts tailored to a Text2SQL task, each defining role, context, constraints, and output style. The README explains why each framework was chosen (role/goal/context focus, testing ToT on a more serious problem than counting). The prompts themselves are high quality and demonstrate understanding of the frameworks. The only minor weakness is that explicit source URLs for the frameworks are not cited, but the reasoning for each choice is present.

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: The student generated predictions for all three prompts using `generate_predictions.py`, calling an Ollama server and storing `question`, `predicted_sql`, and `total_time` (inference time) for each prediction in CSV files named with model and prompt identity. The `evaluate_retrieval_predictions.py` script executes the generated SQL against a SQLite database and compares results to the reference. The `generate_dashboard.py` script produces an interactive HTML report (`report.html`) with accuracy, a correctness agreement matrix, per-question results, and visualization. Inference times are measured and reported. All required outputs are present: prediction CSVs with metadata and a comparative report with visualization.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: The student proposed the Soft Execution F1 metric (a membership-based Precision/Recall/F1 from a research paper) as a complement to exact-match accuracy, and also added the Jaccard index. The `evaluate_soft_execution.py` script implements the metric, executes predictions against the SQLite database, and computes Precision, Recall, F1, and Jaccard for each prompt configuration. A `report.md` with a comparison table and interpretation is generated, and the README provides formulas, discussion of how the metric complements (not replaces) accuracy, and notes its handling of duplicates and empty results. The implementation is complete and the metric values are compared across CRISP, RACE, and ToT.

## Task 4
- Awarded: 1.5b   (max 2b)
- Commentary: The student built a sophisticated interactive HTML dashboard (`template.html` + `generate_dashboard.py`) rendered into `report.html` with actual data. It includes a configuration scorecard, latency-by-question line plots, an accuracy-vs-latency scatter plot, result-size bucket analysis, question-length bucket analysis, pairwise disagreement comparison, and a case viewer. Tables and graphs are abundant and well-designed. The README provides interpretation considering the prompts, the local model, and the coding agent as factors, and explains why CRISP outperformed the others. However, the task explicitly asks to determine whether differences between prompts are statistically significant, and no statistical significance test (e.g., McNemar's test, t-test, or p-value) is performed or reported. This missing requirement justifies a half-point deduction.
