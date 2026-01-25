import json
from embedder import HomieEmbedder

def main():
    print("🧠 Waking up the AI...")
    embedder = HomieEmbedder()

    try:
        with open('backend/mock_data.json', 'r', encoding='utf-8') as f:
            stores = json.load(f)
            print(f"📂 Found {len(stores)} stores in the file.")
    except FileNotFoundError:
        print("❌ Error: Could not find 'backend/mock_data.json'.")
        return
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        return

    print("\n🚀 Starting conversion to vectors...\n")
    
    successful_count = 0
    
    for store in stores:
        try:
            promo_status = "Student Promo Available" if store.get('has_student_promo') else "Standard Price"
            text_to_embed = (
                f"{store.get('name')}. "
                f"{store.get('description')} "
                f"Category: {store.get('location_category')}. "
                f"Price: {store.get('price_range')}. "
                f"{promo_status}."
            )
            
            vector = embedder.get_vector(text_to_embed)
            
            successful_count += 1
            

            if successful_count % 10 == 0:
                print(f"✅ Processed {successful_count}/50 stores...")
                print(f"   Sample Context: {text_to_embed[:60]}...")
                
        except Exception as e:
            print(f"⚠️ Error processing store {store.get('name')}: {e}")

    print("-" * 40)
    print(f"🎉 SUCCESS! Processed {successful_count} stores.")
    print("vectors are generated and ready for the database.")

if __name__ == "__main__":
    main()