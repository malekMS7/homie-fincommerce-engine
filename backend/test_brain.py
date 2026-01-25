from backend.embedder import HomieEmbedder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Wake up the brain
print("🧠 Waking up the model...")
embedder = HomieEmbedder()

# 2. Define 3 words to test
word_main = "Pizza"
word_close = "Food"
word_far = "Computer"

# 3. Convert them to numbers (vectors)
vec_main = embedder.get_vector(word_main)
vec_close = embedder.get_vector(word_close)
vec_far = embedder.get_vector(word_far)

# 4. Calculate similarity (Math magic)
# We reshape the data because the math tool expects a list of lists
score_close = cosine_similarity([vec_main], [vec_close])[0][0]
score_far = cosine_similarity([vec_main], [vec_far])[0][0]

# 5. Print the results
print(f"\n--- 🧪 AI IQ Test Results ---")
print(f"Similarity between '{word_main}' and '{word_close}': {score_close:.4f}  (Should be HIGH)")
print(f"Similarity between '{word_main}' and '{word_far}':   {score_far:.4f}  (Should be LOW)")

if score_close > score_far:
    print("\n✅ SUCCESS: The AI understands context!")
else:
    print("\n❌ FAIL: The AI is confused.")