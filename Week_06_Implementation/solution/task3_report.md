# Task 3: Chunk embeddings

In this task, I needed to turn the chunks into embeddings. I used a fairly straightforward approach: a local Qwen embedding model running through Ollama. Since our chunks are pieces of code, I thought longer vectors might help capture the differences between them: they contain complex context, and many chunks look similar and could end up with similar embeddings. Still, I settled on a vector size of 1024 which is the medium size.

Getting the embeddings only required sending HTTP requests to the local Ollama server's `/api/embed` endpoint and reading the output vectors for use in the next steps.

Finally, I saved the embeddings as NumPy arrays in an `.npz` archive. Since we do not have that many chunks, I did not think we needed a vector database with more advanced storage and retrieval features.

**A LLM-generated reproduction instruction:** From this directory, install `requirements.txt`, start Ollama, pull the model, and run `python embed_chunks.py`. This creates the complete `embeddings.npz`. To rebuild only the inputs without an API call, run `python embed_chunks.py --prepare-only`. Optional arguments are `--input`, `--output`, `--batch-size`, `--model`, and `--ollama-url`; the URL defaults to `OLLAMA_HOST` or `http://localhost:11434`. Search queries in Task 4 must use the same embedding model as the stored chunks.

```powershell
python -m pip install -r requirements.txt
ollama pull qwen3-embedding:0.6b
python embed_chunks.py
```

Load the completed archive:

```python
import json
from pathlib import Path
import numpy as np

chunks_by_id = {
    chunk["id"]: chunk
    for chunk in json.loads(Path("chunks.json").read_text(encoding="utf-8"))
}
with np.load("embeddings.npz", allow_pickle=False) as data:
    chunk_ids = data["chunk_ids"]
    texts = data["texts"]
    chunks = [chunks_by_id[chunk_id] for chunk_id in chunk_ids]
    embeddings = data["embeddings"]
    # embeddings[i] belongs to chunks[i], identified by chunk_ids[i].
```

If Ollama is not running, start the desktop app or run `ollama serve` in another terminal.

