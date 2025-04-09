from flask import Flask, request, jsonify, render_template
from data import load_company_data
from embedder import get_embeddings
from faiss_indexer import build_faiss_index, search
from sklearn.preprocessing import normalize
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load company data
data = load_company_data()

# Use name + sector + description for embeddings
texts = [
    f"{d['name']} | {d['sector']} | {d['description']} | CEO: {d['ceo']} | Location: {d['city']}, {d['state']} | Website: {d['website']}" 
    for d in data
]

# Generate & normalize embeddings
embeddings = normalize(get_embeddings(texts), axis=1)

# Build FAISS index
index = build_faiss_index(embeddings)

# Routes
@app.route('/')
def index_page():
    return render_template("search.html")

@app.route('/search', methods=['POST'])
def search_companies():
    content = request.get_json()
    query = content.get("query", "") if content else ""

    if not query.strip():
        return jsonify([])

    # Normalize query vector
    query_vec = normalize(get_embeddings([query]), axis=1)

    # Search index
    distances, indices = search(query_vec, index)

    # Prepare results
    results = []
    for i, idx in enumerate(indices[0]):
        company = data[idx]
        results.append({
            "rank": i + 1,
            "name": company['name'],
            "symbol": company.get('symbol'),
            "sector": company.get('sector'),
            "ceo": company.get('ceo'),
            "city": company.get('city'),
            "state": company.get('state'),
            "image": company.get('image'),
            "website": company.get('website'),
            "description": company['description'],
            "score": round(float(distances[0][i]), 4)
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
    