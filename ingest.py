import os 
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from backend.embedder import HomieEmbedder  

QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"
COLLECTION_NAME = "homie_places"


def ingest_data():
    print("🧠 Chargement du modèle IA...")
    embedder = HomieEmbedder()

    print("☁️ Connexion à Qdrant Cloud...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

   
    json_path = './backend/mock_data.json'

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"📂 Fichier chargé : {len(data)} lieux trouvés.")
    except FileNotFoundError:
        print(f"❌ Erreur : Impossible de trouver '{json_path}'")
        return

    points = []
    print(f"⚙️ Vectorisation en cours...")

    for item in data:
        promo_status = "Student Promo Available" if item.get('has_student_promo') else "Standard Price"
        text_to_embed = (
            f"{item.get('name')}. "
            f"{item.get('description')} "
            f"Category: {item.get('location_category')}. "
            f"Price: {item.get('price_range')}. "
            f"{promo_status}."
        )
        vector = embedder.get_vector(text_to_embed)
        point = models.PointStruct(
            id=item['id'],
            vector=vector,
            payload={
                "name": item['name'],
                "category": item['location_category'],
                "price_range": item['price_range'],
                "has_student_promo": item['has_student_promo'],
                "description": item['description'],
                "full_context": text_to_embed  
            }
        )
        points.append(point)

    print(f"🚀 Envoi des {len(points)} points vers Qdrant Cloud...")
    operation = client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True
    )

    if operation.status == "completed":
        print("✅ SUCCESS ! La base Qdrant est à jour avec l'intelligence de Malek.")
    else:
        print("❌ Oups, erreur lors de l'envoi.")


if __name__ == "__main__":
    ingest_data()