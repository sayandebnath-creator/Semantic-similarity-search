import faiss
from sklearn.preprocessing import normalize

def build_faiss_index(embeddings, normalize_vectors=True):
    if normalize_vectors:
        embeddings = normalize(embeddings, axis=1)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def search(query_embedding, index, k=3):
    return index.search(query_embedding, k)
