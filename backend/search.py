from sentence_transformers import util
from qdrant_client import QdrantClient
from qdrant_client.http import models
from embedder import HomieEmbedder

QDRANT_URL = "https://a9c95c9f-8d40-45cc-b9b2-9b2ef9ce0da9.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.V5_kAU9dMt48OGzrEXQ-I23cSXzjoNDgJ1j71e03llM"
COLLECTION_NAME = "homie_places"

def analyze_user_intent(query_text, embedder_model):
    """
    Analyse la phrase pour extraire les filtres.
    """
    text_lower = query_text.lower()
    
    detected_filters = {}
    query_vector = embedder_model.encode(query_text)
    
    print(f"\n ANALYSE INTELLIGENTE DE : '{query_text}'")
    cat_concepts = {
        "food": "Manger, restaurant, faim, nourriture, snack, déjeuner, burger, pizza, tacos, dîner",
        "clothes": "Vêtements, habits, mode, shopping, pantalon, pull, chaussures, boutique, friperie, s'habiller",
        "shop": "Grandes surfaces, supermarché, courses, épicerie, marché, acheter à manger, frigo vide, lait, pâtes, fournitures"
    }

    best_cat_score = 0
    best_cat = None

    for cat, desc in cat_concepts.items():
        score = util.cos_sim(query_vector, embedder_model.encode(desc)).item()
        if score > best_cat_score:
            best_cat_score = score
            best_cat = cat
    
    if best_cat_score > 0.25:
        detected_filters["location_category"] = best_cat 
        print(f"    Catégorie trouvée : {best_cat} (Score: {best_cat_score:.2f})")
    else:
        print("    Aucune catégorie spécifique détectée.")
    if "pas cher" in text_lower or "moins cher" in text_lower or "gratuit" in text_lower or "budget" in text_lower:
        detected_filters["price_range"] = "low"
        print("    Budget détecté (Forcé par mot-clé) : low")
        
    else:
        price_concepts = {
            "low": "étudiant, petit prix, économique, gratuit, budget, moins cher",
            "high": "Cher, luxe, qualité, premium, coûteux, haut de gamme" 
        }
        
        best_price_score = 0
        best_price = None

        for price_val, desc in price_concepts.items():
            score = util.cos_sim(query_vector, embedder_model.encode(desc)).item()
            if score > best_price_score:
                best_price_score = score
                best_price = price_val

        if best_price_score > 0.28: 
            detected_filters["price_range"] = best_price
            print(f"    Budget détecté par IA : {best_price} (Score: {best_price_score:.2f})")
        else:
            print("    Pas de filtre de prix (On montre tout).")



    promo_concept = "Promotion, solde, réduction, offre étudiant, bon plan, remise"
    promo_score = util.cos_sim(query_vector, embedder_model.encode(promo_concept)).item()
    
    if promo_score > 0.35:
        detected_filters["has_student_promo"] = True
        print(f"    Promo détectée ! (Score: {promo_score:.2f})")

    return detected_filters

def build_qdrant_filter(filters_dict):
    """
    Traduit le dictionnaire Python en langage Qdrant.
    """
    if not filters_dict:
        return None 

    conditions = []
    for key, value in filters_dict.items():
        conditions.append(
            models.FieldCondition(
                key=key, 
                match=models.MatchValue(value=value)
            )
        )
    
    return models.Filter(must=conditions)

def search_smart(user_query):
    """
    Fonction principale.
    """
    print("\n--- 🕵️ DÉMARRAGE DE LA RECHERCHE ---")
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    embedder = HomieEmbedder()

    filters_dict = analyze_user_intent(user_query, embedder.model)
    
    qdrant_filter = build_qdrant_filter(filters_dict)

    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedder.get_vector(user_query),
        query_filter=qdrant_filter,
        limit=5
    )

    print(f"\n {len(search_results)} résultats trouvés.")
    for hit in search_results:
        print(f"   📍 {hit.payload['name']} ({hit.score:.2f})")

    return search_results