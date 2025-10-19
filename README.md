---

title: "Furniture Product Recommendation API"
emoji: "🛋️"
colorFrom: "blue"
colorTo: "purple"
sdk: "docker"
sdk_version: "3.11"
app_file: "app/main.py"
pinned: false
license: "mit"
--------------

# 🛋️ Furniture Product Recommendation API

Hey! I built this project as part of my **Ikarus assignment**.
It’s an AI-powered furniture recommendation system made with **FastAPI**, **Gemini AI**, and **Pinecone**.

---

## 🚀 What it does

* Gives product recommendations using natural language
* Lets you chat to find items you like
* Generates product descriptions with **Gemini AI**
* Has analytics and “find similar” features
* Uses Pinecone for vector-based semantic search

---

## 🧠 Tech Stack

* **Backend:** FastAPI
* **AI:** Google Gemini, Sentence Transformers
* **Database:** Pinecone
* **Other:** LangChain, PyTorch

---

## ⚙️ Setup

Make sure you have **Python 3.11+** and your API keys ready.

```bash
git clone https://huggingface.co/spaces/0504ankitsharma/furniture-recommendation-api
cd furniture-recommendation-api

python -m venv venv
source venv/bin/activate  # (use venv\Scripts\activate on Windows)

pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
DATA_PATH=./data/dataset.csv
DEBUG=True
```

Then run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔗 Main Endpoints

* `POST /api/recommendations/chat` — chat-based search
* `POST /api/recommendations/search` — normal search
* `GET /api/recommendations/similar/{id}` — similar products
* `GET /api/analytics/` — basic analytics

---

## 📁 Folder Overview

```
app/
 ├── main.py
 ├── routes/
 ├── services/
 ├── models.py
 └── database.py
```

---

## 📊 Dataset

Basic furniture dataset with columns like:

```
title, brand, description, price, categories, images, material, color
```

---

## 💬 Notes

This was mainly built to demonstrate how AI and vector databases
can make product recommendations smarter and faster.

---

### 👨‍💻 Author

**Ankit Sharma** — built for the **Ikarus assignment** ❤️

MIT License
