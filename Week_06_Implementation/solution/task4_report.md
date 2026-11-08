# Task 4: Cosine-similarity retrieval and MMR

Here, I decided to follow a common retrieval practice and select chunks not only by how relevant they are to the input query, but also by how different they are from each other. For this, I used MMR (Maximal Marginal Relevance), which balances relevance to the query against redundancy among the selected chunks. I measured relevance using cosine similarity, which compares the directions of two embedding vectors. For redundancy, I used overlap: the maximum cosine similarity between a candidate chunk and any chunk already selected. In my implementation, negative similarities are treated as zero overlap. The MMR score is:

$$
\operatorname{MMR}(c) = \lambda\,\operatorname{cos}(q,c) - (1-\lambda)\,\underbrace{\max\left(\{0\} \cup \{\operatorname{cos}(c,s) : s \in S\}\right)}_{\operatorname{overlap}(c,S)}.
$$

Here, $q$ is the query embedding, $c$ is a candidate chunk embedding, and $S$ is the set of chunks already selected. A higher $\lambda$ gives more weight to relevance; a lower value gives more weight to diversity. I used $\lambda = 0.2$ to put a stronger emphasis on reducing redundancy within the relevant candidate pool.

The algorithm works as follows:

0. Retrieve the 20 chunks with the highest cosine similarity to the query.
1. Select the most relevant chunk first.
2. Calculate each remaining candidate's overlap with that chunk and its MMR score.
3. Select the candidate with the highest MMR score.
4. Recalculate overlaps and scores using all chunks selected so far.
5. Repeat until five chunks have been selected.

For a small illustrative example, suppose chunk A has already been selected because it has the highest query similarity, 0.90. Two remaining candidates have the following scores, using $\lambda = 0.2$:

| Candidate | Query similarity | Overlap with A | MMR score |
| --- | ---: | ---: | ---: |
| B | 0.88 | 0.95 | $0.2 \times 0.88 - 0.8 \times 0.95 = -0.584$ |
| C | 0.75 | 0.50 | $0.2 \times 0.75 - 0.8 \times 0.50 = -0.250$ |

The algorithm selects C next: although B is more relevant to the query, it is also much more similar to A. Before choosing another chunk, the overlap is recalculated as the maximum similarity to either A or C.

I thought this diversity was especially useful for this task. Our method and test chunks carry surrounding context such as class descriptions, module-level variables, and imports, which can help the model understand the business case and the code it needs to work with. I wanted the final selection to provide complementary context instead of spending most of the available space on very similar chunks. This was my motivation for using MMR; embedding diversity alone does not guarantee that every useful kind of context will be included.
