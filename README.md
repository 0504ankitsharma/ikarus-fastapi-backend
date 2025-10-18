---
title: Furniture Product Recommendation API
emoji: 🛋️
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "3.11"
app_file: app/main.py
pinned: false
license: mit
---

# 🛋️ Furniture Product Recommendation API

AI-powered furniture product recommendation system using FastAPI, Gemini AI, and Pinecone vector database.

## 🌟 Features

- **🔍 Semantic Search**: Find products using natural language queries
- **💬 Conversational Interface**: Chat-based product discovery
- **🤖 AI Descriptions**: Generated product descriptions using Google Gemini
- **📊 Analytics Dashboard**: Comprehensive product insights
- **🎯 Similar Products**: Find related items
- **🚀 Vector Search**: Fast semantic search with Pinecone

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **AI/ML**: 
  - Google Gemini (GenAI)
  - Sentence Transformers (Embeddings)
  - PyTorch (Computer Vision)
  - LangChain (AI Orchestration)
- **Database**: Pinecone Vector DB
- **NLP**: HuggingFace Transformers

## 📋 Prerequisites

- Python 3.11.9
- Gemini API Key
- Pinecone API Key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://huggingface.co/spaces/0504ankitsharma/furniture-recommendation-api
cd furniture-recommendation-api
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch (CPU version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=ikarus
PINECONE_DIMENSION=1024
PINECONE_ENVIRONMENT=us-east-1-aws

DATA_PATH=./data/dataset.csv
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CV_MODEL=efficientnet_b0
DEBUG=True
```

### 4. Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## 📡 API Endpoints

### Recommendations

- **POST** `/api/recommendations/search` - Search products
- **POST** `/api/recommendations/chat` - Conversational search
- **GET** `/api/recommendations/similar/{product_id}` - Get similar products

### Analytics

- **GET** `/api/analytics/` - Get dataset analytics
- **GET** `/api/analytics/products` - Get all products

### Health

- **GET** `/health` - Health check

## 💡 Usage Examples

### Search Products

```python
import requests

response = requests.post(
    "http://localhost:8000/api/recommendations/search",
    json={
        "query": "modern dining chairs",
        "top_k": 5,
        "include_description": true
    }
)

print(response.json())
```

### Chat Interface

```python
response = requests.post(
    "http://localhost:8000/api/recommendations/chat",
    json={
        "message": "I need a comfortable office chair",
        "top_k": 3
    }
)

print(response.json())
```

### Get Analytics

```python
response = requests.get("http://localhost:8000/api/analytics/")
print(response.json())
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Configuration
│   ├── models.py                    # Pydantic models
│   ├── database.py                  # Pinecone integration
│   ├── services/
│   │   ├── embedding_service.py     # Text embeddings
│   │   ├── recommendation_service.py # Recommendation logic
│   │   ├── image_service.py         # Computer vision
│   │   └── genai_service.py         # Gemini AI
│   ├── routes/
│   │   ├── recommendations.py       # Recommendation endpoints
│   │   └── analytics.py             # Analytics endpoints
│   └── utils/
│       └── data_loader.py           # Dataset loader
├── data/
│   └── dataset.csv                  # Product dataset
├── .env                             # Environment variables
├── requirements.txt                 # Dependencies
└── README.md                        # Documentation
```

## 🔧 Configuration

All configuration is done through environment variables in `.env`:

- **GEMINI_API_KEY**: Google Gemini API key
- **PINECONE_API_KEY**: Pinecone API key
- **DATA_PATH**: Path to product dataset
- **EMBEDDING_MODEL**: Sentence transformer model
- **DEBUG**: Enable debug mode

## 📊 Dataset

The system uses a furniture product dataset with the following columns:

- title, brand, description, price
- categories, images, manufacturer
- package_dimensions, country_of_origin
- material, color, uniq_id

## 🤖 AI Features

### 1. Semantic Search
Uses sentence transformers to create embeddings and find semantically similar products.

### 2. Generative Descriptions
Google Gemini generates creative, engaging product descriptions.

### 3. Image Classification
EfficientNet-based computer vision for product categorization.

### 4. Conversational AI
LangChain-powered chatbot for natural product discovery.

## 🔒 Security Notes

- Never commit `.env` file
- Use environment variables for secrets
- Enable CORS only for trusted origins in production
- Rate limit API endpoints for production use

## 📝 License

MIT License

## 👨‍💻 Author

**Ankit Sharma** ([@0504ankitsharma](https://huggingface.co/0504ankitsharma))

## 🙏 Acknowledgments

- Google Gemini AI
- Pinecone
- HuggingFace
- FastAPI

## 📧 Contact

For questions or feedback, please open an issue on the repository.

---

Built with ❤️ using FastAPI and AI