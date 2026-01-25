from sentence_transformers import SentenceTransformer

class HomieEmbedder:
    def __init__(self):
        print("⏳ Chargement du modèle IA Multilingue... (Ça peut prendre quelques secondes)")
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ Modèle chargé avec succès !")

    def get_vector(self, text):
        """
        Convertit un texte en vecteur (liste de chiffres).
        """
        if not text:
            return []
        
        vector = self.model.encode(text)
        
        if vector is None or len(vector) == 0:
            raise ValueError("Erreur lors de la vectorisation (Embedding failed)")
        

        return vector.tolist()


if __name__ == "__main__":
    my_embedder = HomieEmbedder()
    test_text = "Une pizzeria pas chère près de la fac"
    result = my_embedder.get_vector(test_text)
    
    print("-" * 30)
    print(f"🔹 Texte : '{test_text}'")
    print(f"🔹 Vecteur créé ! Longueur : {len(result)}")
    print(f"🔹 Les 5 premiers chiffres : {result[:5]}")
    print("-" * 30)
    print("🎉 SUCCÈS ! Le cerveau est prêt.")