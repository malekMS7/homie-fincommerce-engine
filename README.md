# 🏠 Homie: Moteur de Recherche Étudiant (Backend Engine)

**Homie** est un moteur de recherche intelligent pour les étudiants en Tunisie. Contrairement aux cartes classiques, il utilise l'IA pour comprendre des requêtes subjectives comme *"endroit calme pour réviser"* ou *"café pas cher avec wifi"*.

> ⚠️ **État du projet :** Ce dépôt contient le **Backend (FastAPI)** et l'intégration **Qdrant**. Le Frontend est en cours de développement.

---

## 🛠️ Stack Technique
* **Langage:** Python 3.12
* **API Framework:** FastAPI
* **Base de Données Vectorielle:** Qdrant Cloud
* **Modèle IA:** `paraphrase-multilingual-MiniLM-L12-v2` (Sentence Transformers)
* **Architecture:** REST API

---

## 📂 Structure du Projet
L'architecture suit une organisation claire pour séparer la logique serveur des données.

```text
homie/
├── backend/
│   ├── main.py        
│   ├── ingest.py      
│   ├── search.py      
│   └── places.json    
├── requirements.txt   
└── README.md   

## Guide d'Installation
git clone [https://github.com/malekMS7/homie-fincommerce-engine.git](https://github.com/malekMS7/homie-fincommerce-engine.git)
cd homie-fincommerce-engine
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

## lancer et tester
python -m uvicorn backend.main:app --reload

methode1 de test:

Ouvrez votre navigateur sur : http://127.0.0.1:8000/docs

Cliquez sur la section GET /search

Cliquez sur le bouton Try it out

Saisissez une requête (ex: "cheap coffee for studying")

Cliquez sur Execute


methode2 de test:

Tester via URL Directe:Vous pouvez aussi voir la réponse JSON brute ici : http://127.0.0.1:8000/search?query=calm%20place