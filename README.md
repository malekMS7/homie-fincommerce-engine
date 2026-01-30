# 🏠 Homie - Student Deals Semantic Search

Homie is a smart search engine designed to help students find the best deals (food, clothes, and shops) based on their budget and intent.

Unlike traditional keyword search, Homie uses **Vector Semantic Search** to understand the *meaning* behind a query.

* **The Architecture:**
    1. **Sentence-Transformers:** Converts user queries into numerical vectors (embeddings).
    2. **Qdrant:** Stores these vectors and performs high-speed similarity search to find the most relevant places.
* **Smart Filtering:** Automatically detects intent (e.g., "cheap" = `Low Price`) to filter Qdrant results dynamically.
---

## 🏗️ What's inside of this app?

### Software Stack

| Component | Description |
| :--- | :--- |
| **Qdrant** | Vector database used to store and search place embeddings with high speed. |
| **Sentence-Transformers** | The NLP model used to convert user queries and database items into vectors. |
| **Python (v3.x)** | The main programming language for the backend logic. |
| **Streamlit** | The frontend framework to display the search interface. |

### Application Components

| File | Description |
| :--- | :--- |
| `main.py` | **The Frontend (Streamlit).** The entry point of the application. Run this to start the user interface. |
| `search.py` | **The Brain.** Handles the "smart" logic: detects intent (Price/Category) and queries Qdrant. |
| `embedder.py` | **The Model Wrapper.** Manages the Sentence-Transformer model to vectorize text. |
| `setup_qdrant.py` | **Database Setup.** Script to create the Qdrant collection and configure the schema. |
| `ingest.py` | **Data Loader.** Reads `places.json` and uploads the data into the Qdrant database. |
| `places.json` | **The Dataset.** Contains the raw list of student deals (names, descriptions, prices). |
| `fix_indexes.py` | **Maintenance.** A utility script to ensure Qdrant filters (like price) work correctly. |
| `test_brain.py` | **Testing.** A script to test the search logic without running the full interface. |
---

## 🛠️ Prerequisites

* **Python (v3.10+)**
* A **Qdrant Cloud** account (API Key & URL).

---

## 🚀 Setup

### 1. Clone the repository
```bash
git clone [https://github.com/votre-pseudo/homie.git](https://github.com/votre-pseudo/homie.git)
cd homie
### 2. Setup the virtual environment
It is recommended to use a virtual environment to avoid conflicts with other projects.

```bash
# 1. Create the virtual environment
python -m venv venv

# 2. Activate it:
# On Windows:
.\venv\Scripts\activate

# On Mac / Linux:
source venv/bin/activate
### 3. Install required dependencies
Install all the necessary Python libraries (Streamlit, Qdrant, AI models) with this command:

```bash
pip install -r requirements.txt
### 4. Configuration
 To connect the app to the Qdrant Cloud database, you need to set up your credentials.

1. Open the `search.py` file.
2. Locate the configuration section at the top.
3. Replace the values with your own Qdrant Cluster URL and API Key:

```python
# In search.py

QDRANT_URL = "[https://your-cluster-url.qdrant.io](https://your-cluster-url.qdrant.io)"
QDRANT_API_KEY = "your-api-key-starting-with-eyJ..."
