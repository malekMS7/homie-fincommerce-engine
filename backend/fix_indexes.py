from qdrant_client import QdrantClient
from qdrant_client.http import models


QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"
COLLECTION_NAME = "homie_places"

print("⏳ Connexion à Qdrant...")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

print("⚙️ Création des index en cours...")

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="location_category",
    field_schema=models.PayloadSchemaType.KEYWORD
)
print("    Index 'location_category' créé.")

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="price_range",
    field_schema=models.PayloadSchemaType.KEYWORD
)
print("    Index 'price_range' créé.")

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="has_student_promo",
    field_schema=models.PayloadSchemaType.KEYWORD 
)
print("   ✅Index 'has_student_promo' créé.")