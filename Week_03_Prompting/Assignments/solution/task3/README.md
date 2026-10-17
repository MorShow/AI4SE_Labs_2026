# Task 3

For this task, I chose Precision, Recall, and F1-score as complements to exact-match Accuracy. Accuracy gives a prediction credit only when the SQL result fully matches the reference result. These additional metrics can assign a score between 0 and 1 when an answer is only partly correct, making it possible to compare prompt configurations beyond complete matches.

The implementation compares the restaurant names returned by the generated SQL with the names in the reference result. Let $P$ be the list of predicted names and $G$ the list of reference names for one question. The per-question formulas are:

$$
\operatorname{Precision}(P,G)=
\frac{\sum_{p\in P}\mathbf{1}[p\in G]}{|P|},
\qquad
\operatorname{Recall}(P,G)=
\frac{\sum_{g\in G}\mathbf{1}[g\in P]}{|G|}.
$$

$$
F_1(P,G)=
\frac{2\,\operatorname{Precision}(P,G)\operatorname{Recall}(P,G)}
{\operatorname{Precision}(P,G)+\operatorname{Recall}(P,G)}.
$$

Recall measures how many reference names were retrieved. Precision measures how many predicted names occur in the reference result. F1 is their harmonic mean.

I also tested the Jaccard index to obtain another non-binary score. With $P_s$ and $G_s$ denoting the sets of unique names:

$$
J(P,G)=\frac{|P_s\cap G_s|}{|P_s\cup G_s|}.
$$

All metrics rank the three configurations in the same order, so they do not change the overall comparison. They do reveal one detail about CRISP: its Precision is 64%, which is 14-17 points above its Accuracy and Recall. This suggests that the names CRISP does return are often relevant, while it still misses some reference names. Jaccard gives a similar overall picture.

I considered LLM-as-a-judge as another option. A separate model could assess answers against explicit criteria and account for semantic nuances, especially for free-form text. That would require additional time and compute, so I did not use it here.

Overall, I would be prepared to defend these metrics in the context of classical machine learning, but here they turned out to be less useful and insightful than I expected. More broadly, evaluating conventional ML models and evaluating language models are two different worlds, and the latter require different kinds of evaluation pipelines.
