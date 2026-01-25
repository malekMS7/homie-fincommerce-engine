from qdrant_client import QdrantClient
from embedder import HomieEmbedder

QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"
COLLECTION_NAME = "homie_places"

def search(user_query, price_filter=None):
    """
    Cette fonction pose une question à la base de données.
    - user_query : La phrase de l'étudiant (ex: "J'ai faim")
    - price_filter : (Optionnel) "cheap", "moderate", etc.
    """
    
    print("\n--- 🕵️ RECHERCHE EN COURS ---")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    embedder = HomieEmbedder() # L'IA de Malek

    print(f"❓ Question : '{user_query}'")
    query_vector = embedder.get_vector(user_query)

    query_filter = None
    if price_filter:
        from qdrant_client.http import models
        print(f"🔍 Filtre appliqué : Prix = {price_filter}")
        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="price_range",
                    match=models.MatchValue(value=price_filter)
                )
            ]
        )

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=query_filter,
        limit=3 
    )

    print(f"\n✅ J'ai trouvé {len(hits)} résultat(s) pertinent(s) :")
    for i, hit in enumerate(hits):
        score = round(hit.score * 100, 1) 
        data = hit.payload
        print(f"\n   🏆 TOP {i+1} (Pertinence : {score}%)")
        print(f"      📍 Nom : {data['name']}")
        print(f"      🏷️  Catégorie : {data['category']}")
        print(f"      💰 Prix : {data['price_range']}")
        print(f"      📝 Description : {data['description']}")

if __name__ == "__main__":
    
    search("je veux un sandwich a proximite ")
