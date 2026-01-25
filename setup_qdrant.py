from qdrant_client import QdrantClient
from qdrant_client.http import models

QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io" 
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"

COLLECTION_NAME = "homie_places"
VECTOR_SIZE = 384 

print("⏳ Connexion à Qdrant Cloud...")
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=60 
)

def init_collection():
    
    if client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"⚠️ La collection '{COLLECTION_NAME}' existe déjà sur le Cloud.")
        return

    print(f"🚀 Création de la collection '{COLLECTION_NAME}'...")
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE
        )
    )
    
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="category", field_schema=models.PayloadSchemaType.KEYWORD)
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="price_range", field_schema=models.PayloadSchemaType.KEYWORD)
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="has_student_promo", field_schema=models.PayloadSchemaType.KEYWORD)

    print(f"✅ Collection '{COLLECTION_NAME}' créée avec succès sur le Cloud !")

if __name__ == "__main__":
    init_collection()