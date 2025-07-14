import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("mails.json") as f:
    mails = json.load(f)

texts = [m["subject"] + ": " + m["body"] for m in mails]
embeddings = model.encode(texts, convert_to_numpy=True)
mail_ids = [m["id"] for m in mails]

# Speichern
np.save("embeddings.npy", embeddings)
with open("mail_ids.json", "w") as f:
    json.dump(mail_ids, f)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "index.faiss")

