# NeuraScheme AI

## AI Agent for Government Scheme Intelligence Platform

**Empowering Every Citizen Through Intelligent Government Scheme Discovery**

---

# Overview

NeuraScheme AI is a **AI Agent for Government Scheme Intelligence Platform** that helps citizens discover government schemes they are eligible for without manually searching through thousands of schemes.

The platform combines **rule-based eligibility analysis**, **semantic search**, and a **six-agent AI architecture** to provide personalized recommendations, AI-generated explanations, and conversational guidance throughout the application process.

---

# Problem Statement

Government schemes are spread across multiple portals with complex eligibility criteria. Citizens often struggle to:

- Find relevant schemes
- Understand eligibility requirements
- Compare scheme benefits
- Identify required documents
- Complete the application process

NeuraScheme AI simplifies this process by providing an intelligent, personalized recommendation system.

---

# Solution

NeuraScheme AI allows users to:

- Create a personalized profile
- Automatically discover eligible government schemes
- Receive AI-powered recommendations
- Understand why each scheme is recommended
- Interact with an AI Assistant for guidance
- Access application information and required documents

---

# Multi-Agent Architecture

```text
                   User
                     │
                     ▼
             Profile Agent
                     │
                     ▼
            Retrieval Agent
                     │
                     ▼
           Eligibility Agent
                     │
                     ▼
        Recommendation Agent
                     │
                     ▼
         Explanation Agent
                     │
                     ▼
         AI Assistant Agent
                     │
                     ▼
      Personalized Recommendations
```

---

# AI Agents

## 1. Profile Agent

### Responsibility

Processes and validates user information before recommendation.

### Functions

- Collects user profile information
- Validates profile data
- Normalizes user attributes
- Calculates profile completeness
- Generates structured user profile

### Output

- Standardized user profile
- Profile completeness score

---

## 2. Retrieval Agent

### Responsibility

Searches the government scheme database to retrieve relevant schemes.

### Functions

- Semantic search
- Metadata filtering
- Vector-based retrieval
- Candidate scheme selection

### Output

- Relevant government schemes

---

## 3. Eligibility Agent

### Responsibility

Determines whether the user satisfies the eligibility criteria for each scheme.

### Functions

- Eligibility verification
- Rule matching
- Missing condition detection
- Eligibility scoring

### Output

- Eligible schemes
- Matched conditions
- Missing conditions
- Eligibility score

---

## 4. Recommendation Agent

### Responsibility

Ranks eligible schemes based on relevance and confidence.

### Functions

- Recommendation ranking
- Confidence score calculation
- Personalized recommendation generation

### Output

- Top recommended schemes
- Confidence scores

---

## 5. Explanation Agent

### Responsibility

Generates personalized explanations using a Large Language Model.

### Functions

- Explain recommendations
- Highlight benefits
- Summarize eligibility
- Describe required documents
- Explain application process

### Output

- Natural language explanation
- Benefit summary
- Application guidance

---

## 6. AI Assistant Agent

### Responsibility

Provides conversational support for users.

### Functions

- Answer scheme-related questions
- Explain eligibility
- Guide application process
- Provide additional scheme information

### Output

- Conversational responses
- User guidance
- Clarifications

---

# Workflow

```text
User Registration
        │
        ▼
Create User Profile
        │
        ▼
Profile Agent
        │
        ▼
Retrieve Candidate Schemes
        │
        ▼
Eligibility Verification
        │
        ▼
Recommendation Ranking
        │
        ▼
AI Explanation
        │
        ▼
AI Assistant
        │
        ▼
Final Personalized Recommendations
```

---

# Features

## User Features

- User Registration and Login
- Secure Authentication
- Profile Management
- Personalized Recommendations
- Government Scheme Discovery
- Eligibility Verification
- AI-generated Explanations
- Interactive AI Chat Assistant
- Search and Filtering

## AI Features

- Multi-Agent AI Architecture
- Semantic Search
- Rule-Based Eligibility Checking
- Recommendation Ranking
- Natural Language Explanations
- Conversational AI
- Confidence-Based Scoring

---

# Technology Stack

## Frontend

- React.js
- Vite
- CSS3
- Axios

## Backend

- FastAPI
- Python 3.11
- JWT Authentication
- Motor
- PyMongo

## Database

- MongoDB Atlas

## Artificial Intelligence

- LangGraph
- Groq API
- Llama Models
- Sentence Transformers

## Machine Learning

- Semantic Search
- Vector Embeddings
- Rule-Based Recommendation Engine

---

# Dataset

The platform uses a curated dataset containing **3,397 Government Schemes** with information including:

- Scheme Name
- Benefits
- Eligibility Criteria
- Required Documents
- Application Process
- Category
- Government Level
- Tags

---

# Security

- JWT Authentication
- Password Hashing (bcrypt)
- Secure REST APIs
- MongoDB Atlas
- Environment Variable Configuration

---

# Project Structure

```text
NeuraScheme-AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── database/
│   │   ├── models/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── scripts/
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

# Run the Project

## Prerequisites

- Node.js 20 or later
- Python 3.11 or later
- A MongoDB Atlas database
- A Groq API key

## 1. Configure the backend

Create `backend/.env` with the following values. Replace the placeholders with your own credentials.

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=neurascheme
JWT_SECRET=use_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_DB_PATH=chroma_db
```

From the project root, create and activate a virtual environment, then install the backend dependencies:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`; interactive API documentation is at `http://localhost:8000/docs`.

## 2. Import and index scheme data

In a second terminal, with the backend virtual environment active:

```powershell
cd backend
.\venv\Scripts\python.exe scripts\clean_dataset.py
.\venv\Scripts\python.exe scripts\import_dataset.py
.\venv\Scripts\python.exe scripts\build_chroma_index.py
```

`build_chroma_index.py` is required for semantic retrieval. Re-run it after adding or substantially changing schemes in the admin panel.
Existing admin credentials:
email: admin123@neurascheme.com
password: Admin@1234
To create an administrator account, run:

```powershell
.\venv\Scripts\python.exe scripts\seed_admin.py
```

## 3. Run the frontend

In another terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

The frontend is available at `http://localhost:5173` and connects to `http://localhost:8000` by default. To use another API URL, create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The frontend dependencies, including `jspdf` for the document scanner's image-to-PDF feature, are managed in `frontend/package.json`.

## 4. Run the agent integration test

The agent test is a live integration test: it requires the MongoDB and Groq values above and creates test recommendation/deadline records with user ID `test123`.

```powershell
cd backend
venv\Scripts\activate
python ../demo/demo_agents.py
```

---

# Future Enhancements

- Voice Assistant
- Regional Language Support
- OCR-Based Document Verification
- WhatsApp Integration
- Mobile Application
- Real-Time Government Scheme Updates
- Predictive Eligibility Analysis

---

# Use Cases

- Students
- Farmers
- Women
- Senior Citizens
- Entrepreneurs
- Persons with Disabilities
- Job Seekers
- Low-Income Families

---

# Key Highlights

- Multi-Agent AI Architecture
- Personalized Government Scheme Recommendations
- AI-Powered Explanations
- Intelligent Chat Assistant
- Semantic Search
- Eligibility Verification
- Confidence-Based Recommendation Ranking
- Secure Authentication
- Modern Full-Stack Architecture
