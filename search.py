import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

# Modelle und Daten laden
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("mails.json") as f:
    mails = json.load(f)
with open("mail_ids.json") as f:
    mail_ids = json.load(f)

index = faiss.read_index("index.faiss")

# Interaktive Suche
print("🔍 Semantische Mail-Suche (Tippe 'exit' zum Beenden)")
while True:
    query = input("\nFrage: ")
    if query.strip().lower() in ("exit", "quit"):
        break

    qvec = model.encode([query])
    D, I = index.search(np.array(qvec), k=3)
    print("\n📬 Ähnliche Mails:")
    for rank, idx in enumerate(I[0], start=1):
        mail = mails[mail_ids.index(mail_ids[idx])]
        print(f"\n#{rank}: {mail['subject']}\n{mail['body'][:200]}{'...' if len(mail['body']) > 200 else ''}")

