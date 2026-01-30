import json
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from embedder import HomieEmbedder

QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"
COLLECTION_NAME = "homie_places"
JSON_PATH = './data/places.json'

def ingest_data():
    print("🧠 Chargement du modèle IA...")
    embedder = HomieEmbedder()

    print("☁️ Connexion à Qdrant Cloud...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    print("🗑️  Reset de la collection (pour partir sur du propre)...")
    client.delete_collection(collection_name=COLLECTION_NAME)
    
    print("🆕 Création de la collection optimisée...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )

    print("🔧 Création des index de recherche (Anti-erreur 400)...")
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="location_category", field_schema=models.PayloadSchemaType.KEYWORD)
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="price_range", field_schema=models.PayloadSchemaType.KEYWORD)

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"📂 Fichier chargé : {len(data)} lieux trouvés.")
    except FileNotFoundError:
        print(f"❌ Erreur : Impossible de trouver '{JSON_PATH}'")
        return

    points = []
    print(f"⚙️ Vectorisation et Normalisation en cours...")

    for i, item in enumerate(data):
        promo_status = "Student Promo Available" if item.get('has_student_promo') else "Standard Price"
        
        text_to_embed = (
            f"{item.get('name')}. "
            f"{item.get('description')} "
            f"Category: {item.get('location_category')}. "
            f"Price: {item.get('price_range')}. "
            f"{promo_status}."
        )
        vector = embedder.get_vector(text_to_embed)

        category_clean = item['location_category'].lower() if item.get('location_category') else "unknown"
        price_clean = item['price_range'].lower() if item.get('price_range') else "unknown"

        point = models.PointStruct(
            id=i, 
            vector=vector,
            payload={
                "name": item['name'],
                "location_category": category_clean, 
                "price_range": price_clean,
                "has_student_promo": item.get('has_student_promo', False),
                "description": item.get('description', ''),
                "full_context": text_to_embed
            }
        )
        points.append(point)

    print(f"🚀 Envoi des {len(points)} points vers Qdrant Cloud...")
    client.upload_points(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("✅ SUCCÈS TOTAL ! La base est propre, indexée et vectorisée.")
if __name__ == "__main__":
    ingest_data()