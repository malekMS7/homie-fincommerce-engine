from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"
COLLECTION_NAME = "homie_places"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🧠 Loading AI Model...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

print("☁️ Connecting to Qdrant Cloud...")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

class SearchQuery(BaseModel):
    query: str

@app.get("/search")
def search(query: str):
    print(f"🔍 Processing query: '{query}'")
    
    try:
        vector = model.encode(query).tolist()

        search_result = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=5
        )
        
        results = search_result.points
        formatted_results = []
        
        for hit in results:
            data = hit.payload or {}
            formatted_results.append({
                "name": data.get("name", "Unknown"),
                "description": data.get("description", "No description"),
                "category": data.get("category"),
                "price": data.get("price_range"),
                "promo": data.get("has_student_promo"),
                "score": hit.score
            })
            
        return {"results": formatted_results}

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))