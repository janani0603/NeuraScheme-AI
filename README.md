<div align="center">

# 🧠 NeuraScheme AI
### Multi-Agent Government Scheme Intelligence Platform

*Helping citizens discover the right government schemes through AI-powered recommendations, explainable eligibility analysis, and intelligent document guidance.*

---

React • FastAPI • MongoDB Atlas • LangGraph • Gemini • Sentence Transformers

</div>

---

# 📖 Table of Contents

- About
- Problem Statement
- Motivation
- Objectives
- Key Features
- Technology Stack
- Dataset
- System Architecture
- AI Architecture
- Recommendation Pipeline
- Project Structure
- UI Overview
- Backend Overview
- Database
- API Documentation
- Installation
- Deployment
- Future Scope

---

# 🌍 About the Project

Government welfare schemes play a vital role in improving the quality of life for millions of citizens. Every year, both Central and State Governments launch schemes for students, farmers, women, entrepreneurs, senior citizens, MSMEs, and economically weaker sections.

Despite their availability, many citizens never receive these benefits because:

- Information is spread across multiple government websites.
- Eligibility requirements are difficult to understand.
- Application procedures are lengthy.
- Required documents are unclear.
- Users are unaware of newly launched schemes.
- Citizens cannot easily determine which schemes match their profile.

NeuraScheme AI addresses these challenges through a modern web platform powered by multiple AI agents that work together to analyze a user's profile, retrieve relevant schemes, evaluate eligibility, recommend the most suitable options, explain the reasoning behind each recommendation, and guide users throughout the application process.

Rather than acting as a simple chatbot, NeuraScheme AI functions as an intelligent decision support system that combines structured filtering, semantic search, explainable AI, and personalized recommendations.

---

# ❗ Problem Statement

Government welfare information is fragmented across multiple portals and departments. Citizens often struggle to identify relevant schemes, understand eligibility conditions, prepare the required documentation, and submit applications before deadlines.

Develop an AI-powered Government Scheme Intelligence Platform that centralizes scheme information, automatically identifies eligible schemes based on user profiles, explains recommendation decisions, and simplifies the application process through a collaborative multi-agent architecture.

---

# 🎯 Objectives

The primary objectives of NeuraScheme AI are:

- Centralize government scheme information.
- Simplify scheme discovery.
- Provide personalized recommendations.
- Explain why a scheme is recommended.
- Reduce application complexity.
- Assist users in preparing documents.
- Notify users about deadlines.
- Increase awareness of government welfare initiatives.

---

# 💡 Why NeuraScheme AI?

Traditional government portals expect users to search through hundreds of schemes manually.

NeuraScheme AI changes this workflow.

Instead of presenting every available scheme, the platform asks:

- Who are you?
- Where do you live?
- What is your occupation?
- What is your annual income?
- Are you a student, farmer, entrepreneur, or senior citizen?

Using this information, the platform automatically narrows thousands of schemes into a small set of highly relevant recommendations, each accompanied by an explanation of why it was selected.

This approach significantly reduces user effort while improving accessibility and transparency.

---

# ✨ Key Features

## 🔍 Intelligent Scheme Search

Search schemes using:

- Keywords
- Categories
- State
- Ministry
- Eligibility
- Occupation
- Income
- Education
- Gender

---

## 🤖 Multi-Agent AI

The platform uses specialized AI agents instead of a single chatbot.

Agents include:

- Discovery Agent
- Eligibility Agent
- Recommendation Agent
- Document Assistant Agent
- Reminder Agent
- AI Assistant Agent

Each agent performs one task and passes structured results to the next agent, making the system modular, explainable, and easier to maintain.

---

## 🎯 Personalized Recommendations

Recommendations are generated using:

- User profile
- Semantic similarity
- Eligibility analysis
- Rule-based scoring
- AI reasoning

---

## 📄 AI-Generated Scheme Summaries

Long government scheme descriptions are converted into concise summaries containing:

- Purpose
- Benefits
- Eligibility
- Required documents
- Application process
- Important deadlines

---

## 📂 Document Guidance

For every recommended scheme, users receive:

- Required documents
- Missing documents
- Optional documents
- Application instructions

---

## 🔔 Smart Notifications

The system notifies users about:

- New schemes
- Upcoming deadlines
- Saved scheme updates
- Application status

---

## ❤️ Saved Schemes

Users can:

- Bookmark schemes
- Track applications
- Revisit recommendations
- Compare schemes

---

# 🛠 Technology Stack

## Frontend

- React (Vite)
- React Router
- Axios
- CSS3
- Framer Motion
- Recharts

---

## Backend

- FastAPI
- Python
- JWT Authentication
- REST APIs

---

## Database

MongoDB Atlas

Collections include:

- Users
- Schemes
- Saved Schemes
- Notifications
- Conversations
- Recommendations

---

## Artificial Intelligence

- LangGraph
- Gemini API
- Sentence Transformers
- ChromaDB (or MongoDB Atlas Vector Search)

---

# 📊 Dataset

The application is built using a curated Government Schemes dataset obtained from Kaggle.

Each record contains information such as:

| Field | Description |
|--------|-------------|
| scheme_name | Name of the scheme |
| slug | Unique identifier |
| details | Complete description |
| benefits | Benefits offered |
| eligibility | Eligibility requirements |
| application | Application procedure |
| documents | Required documents |
| level | State or Central |
| schemeCategory | Category of the scheme |

The dataset is cleaned and imported into MongoDB Atlas during the data ingestion process.

The original CSV is **not** queried directly by the application. Instead, MongoDB serves as the primary data source, enabling efficient search, filtering, and recommendation.

---

# 🧠 AI Recommendation Pipeline

Unlike traditional machine learning systems that require labeled training data, NeuraScheme AI combines structured filtering, semantic retrieval, and large language models to generate recommendations.

The recommendation pipeline consists of four stages:

1. User Profile Analysis
2. Candidate Scheme Retrieval
3. Eligibility Evaluation
4. AI Explanation Generation

This hybrid approach provides both accurate recommendations and human-readable explanations without requiring a supervised classification model.

---

# 🏗 High-Level System Architecture

                    Kaggle Dataset
                           │
                           ▼
                Data Cleaning Pipeline
                           │
                           ▼
                  MongoDB Atlas Database
                           │
                           ▼
                    FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Discovery Agent   Eligibility Agent   AI Assistant
        │                  │
        └──────────┬───────┘
                   ▼
         Recommendation Agent
                   │
                   ▼
          Document Assistant
                   │
                   ▼
             Reminder Agent
                   │
                   ▼
             React Frontend

---

# 📌 Design Principles

The platform is designed around five core principles:

- Simplicity
- Explainability
- Accessibility
- Scalability
- Transparency

Every recommendation generated by the system should clearly explain why it was suggested, allowing users to make informed decisions rather than blindly trusting AI output.

---

# 🎨 User Interface & User Experience

## Design Philosophy

NeuraScheme AI is designed for a wide range of users, including students, farmers, women entrepreneurs, senior citizens, MSMEs, and citizens with limited technical knowledge. The interface prioritizes simplicity, clarity, and accessibility while maintaining a modern appearance.

The application follows these core design principles:

- Minimal and uncluttered interface
- Mobile-first responsive design
- Easy navigation with minimal clicks
- Accessible typography and color contrast
- Explainable AI with transparent recommendations
- Consistent spacing, icons, and layouts
- Fast loading with clear feedback for AI operations

---

# 🎨 Design System

## Color Palette

| Purpose | Color |
|----------|---------|
| Primary | #2563EB |
| Primary Hover | #1D4ED8 |
| Secondary | #0F172A |
| Success | #16A34A |
| Warning | #F59E0B |
| Error | #DC2626 |
| Background | #F8FAFC |
| Surface | #FFFFFF |
| Border | #E2E8F0 |
| Primary Text | #1E293B |
| Secondary Text | #64748B |

---

## Typography

| Element | Font | Weight |
|----------|------|---------|
| Headings | Poppins | Bold |
| Subheadings | Poppins | Semi Bold |
| Body Text | Inter | Regular |
| Buttons | Inter | Semi Bold |
| Captions | Inter | Regular |

---

## Border Radius

- Cards: 16px
- Buttons: 10px
- Input Fields: 10px
- Dialogs: 16px

---

## Shadows

Cards use soft shadows to create depth while maintaining a clean appearance.

Buttons have subtle hover elevation.

---

# 📱 Responsive Design

The application should support:

- Desktop
- Laptop
- Tablet
- Mobile

Breakpoints

| Device | Width |
|----------|---------|
| Mobile | <768px |
| Tablet | 768–1024px |
| Desktop | >1024px |

Navigation automatically adapts:

- Desktop → Sidebar + Navbar
- Tablet → Collapsible Sidebar
- Mobile → Bottom Navigation + Hamburger Menu

---

# 🏠 Landing Page

## Purpose

The landing page introduces the platform, communicates its value, and encourages users to register or explore government schemes.

---

## Navigation Bar

The navigation bar remains fixed at the top.

### Left Section

- Logo
- NeuraScheme AI

### Right Section

- Home
- Features
- Explore Schemes
- About
- Contact
- Login
- Get Started

---

## Hero Section

The hero section occupies the full viewport.

### Left Side

Main Heading

> Find the Right Government Scheme in Minutes

Supporting Text

> Discover personalized government schemes using AI-powered recommendations, eligibility analysis, and intelligent guidance.

Primary Button

Get Started

Secondary Button

Explore Schemes

---

### Right Side

Illustration showing:

- Citizen profile
- AI assistant
- Government building
- Recommendation cards
- Connected AI agents

---

## Statistics Section

Display animated counters.

Example:

- 3,000+ Government Schemes
- 28 States Covered
- 6 AI Agents
- Thousands of Potential Beneficiaries

---

## Feature Cards

Six cards displayed in a responsive grid.

Each card contains:

- Icon
- Title
- Description

Example cards:

- Smart Search
- Personalized Recommendations
- Eligibility Checker
- AI Assistant
- Document Guidance
- Deadline Alerts

---

## AI Workflow Section

Illustrate the recommendation process.

Profile Creation

↓

AI Analysis

↓

Eligibility Check

↓

Recommendations

↓

Application Guidance

↓

Success

---

## Footer

Contains:

- About
- Documentation
- GitHub
- Privacy Policy
- Terms of Service
- Contact Information

---

# 🔐 Authentication

## Login Page

The login page uses a centered authentication card.

Fields:

- Email
- Password

Actions:

- Login
- Continue with Google (optional)
- Forgot Password
- Register

Validation:

- Invalid email
- Incorrect password
- Empty fields

Display meaningful error messages without exposing technical details.

---

## Registration Page

Registration uses a multi-step form to reduce cognitive load.

### Step 1 – Account Information

- Full Name
- Email
- Phone Number
- Password
- Confirm Password

---

### Step 2 – Personal Information

- Date of Birth
- Gender
- State
- District

---

### Step 3 – Professional Information

- Occupation
- Education
- Annual Income
- Category
- Student Status
- Farmer Status
- Business Owner
- Disability Status

---

### Step 4 – Review & Submit

Display a summary of entered information before account creation.

---

# 🏡 Dashboard

The dashboard is the central workspace after login.

Layout:

Navbar

↓

Sidebar + Main Content

---

## Sidebar

Contains navigation links to:

- Dashboard
- Explore Schemes
- Eligibility Checker
- Saved Schemes
- AI Assistant
- Notifications
- Applications
- Profile
- Settings

---

## Welcome Banner

Personalized greeting.

Example:

Good Morning, Janani

Based on your profile, we've found new government schemes that may interest you.

---

## Quick Statistics

Display four cards.

- Eligible Schemes
- Saved Schemes
- Applications
- Upcoming Deadlines

Each card displays:

- Icon
- Value
- Small description

---

## Recommended Schemes

Display recommendations as horizontal cards.

Each card contains:

- Scheme Name
- Category
- Eligibility Score
- Deadline
- Save Button
- View Details

---

## AI Insights Widget

A dedicated widget displaying personalized suggestions.

Example:

"Based on your updated profile, you now qualify for two new scholarship schemes."

---

## Notifications Panel

Displays recent notifications.

Examples:

- New scholarship available
- Deadline approaching
- Document missing
- Application approved

---

# 🔍 Scheme Explorer

The Scheme Explorer acts as the searchable catalogue of all government schemes.

---

## Search Bar

Supports keyword search.

Examples:

- Scholarship
- Agriculture
- Startup
- Housing

---

## Filters

Users can filter by:

- State
- Scheme Level
- Category
- Occupation
- Income Range
- Gender
- Student
- Farmer
- Senior Citizen
- Women
- MSME

Multiple filters may be selected simultaneously.

---

## Results Grid

Display schemes in responsive cards.

Each card includes:

- Scheme Name
- Category
- Level (State/Central)
- Short Description
- Eligibility Score (if logged in)
- Save Button
- View Details

---

## Sorting

Users may sort by:

- Most Relevant
- Newest
- Deadline
- Alphabetical

---

# 📄 Scheme Details Page

This page provides complete information about an individual government scheme.

---

## Header

Display:

- Scheme Name
- Category
- State/Central Badge
- Ministry
- Deadline

Actions:

- Save
- Share
- Ask AI

---

## Tabs

Information is divided into tabs.

### Overview

Displays:

- Description
- Objectives
- Summary

---

### Benefits

Shows:

- Financial Assistance
- Subsidies
- Scholarships
- Training
- Other benefits

---

### Eligibility

Displays:

- Age
- Income
- Occupation
- State
- Category
- Additional requirements

---

### Required Documents

Checklist of documents.

Examples:

- Aadhaar Card
- Income Certificate
- Community Certificate
- Bank Passbook
- Student ID

Missing documents are highlighted for logged-in users.

---

### Application Process

Step-by-step instructions.

1. Visit official portal
2. Register
3. Upload documents
4. Submit application
5. Track status

Include a button linking to the official application website.

---

### FAQs

Frequently asked questions about the scheme.

---

# ✅ Eligibility Checker

This page collects user information to determine eligibility for available schemes.

---

## Multi-Step Form

### Personal Details

- Age
- Gender
- State
- District

---

### Education & Occupation

- Education
- Occupation
- Student Status
- Farmer Status

---

### Financial Information

- Annual Income
- Category
- Disability Status
- Business Ownership

---

## AI Analysis Progress

Once submitted, display the execution of AI agents.

Example:

✓ Profile Validation

✓ Candidate Scheme Retrieval

✓ Eligibility Evaluation

✓ Recommendation Generation

✓ Explanation Creation

Each completed step should include a short description to improve transparency.

---

## Recommendation Results

Display recommended schemes ranked by relevance.

Each recommendation card includes:

- Scheme Name
- Match Percentage
- Why Recommended
- Key Benefits
- Required Documents
- View Details
- Save Scheme

Recommendations should be accompanied by a brief explanation to help users understand why a scheme matches their profile.

---

# 🔄 User Journey

A typical user flow is as follows:

1. Visit Landing Page
2. Create an Account
3. Complete User Profile
4. Explore Available Schemes
5. Run Eligibility Checker
6. Receive AI Recommendations
7. Review Scheme Details
8. Save Preferred Schemes
9. Apply Through Official Portal
10. Receive Notifications and Updates

# 🧠 Artificial Intelligence Architecture

## Overview

The intelligence behind NeuraScheme AI is powered by a collaborative multi-agent system built using **LangGraph**. Instead of relying on a single Large Language Model (LLM) to answer every question, the platform decomposes the problem into smaller tasks handled by specialized AI agents.

Each agent performs one well-defined responsibility before passing structured output to the next agent. This architecture improves explainability, modularity, and maintainability while reducing unnecessary LLM usage.

The AI workflow combines:

- Structured database queries
- Rule-based filtering
- Semantic search
- Large Language Models
- Explainable recommendations

---

# Why Multi-Agent AI?

A traditional chatbot typically answers user queries in one step.

```
User Question
      │
      ▼
     LLM
      │
      ▼
   Response
```

While simple, this approach has limitations:

- Expensive for repeated queries
- Difficult to explain decisions
- No modularity
- Hard to debug
- Limited personalization

NeuraScheme AI instead follows a collaborative pipeline.

```
User
 │
 ▼
Profile Agent
 │
 ▼
Discovery Agent
 │
 ▼
Eligibility Agent
 │
 ▼
Recommendation Agent
 │
 ▼
Document Agent
 │
 ▼
Assistant Agent
 │
 ▼
Final Response
```

Each agent only performs one responsibility.

---

# AI Workflow

The complete recommendation pipeline consists of six stages.

## Step 1 — User Profile Collection

The user creates an account and completes their profile.

Information collected includes:

- Name
- State
- District
- Age
- Gender
- Occupation
- Education
- Annual Income
- Category
- Student Status
- Farmer Status
- Disability Status
- Business Owner Status

This profile is stored securely in MongoDB Atlas.

---

## Step 2 — Candidate Scheme Retrieval

The Discovery Agent searches MongoDB for schemes matching broad criteria.

Examples include:

- State
- Category
- Occupation
- Scheme Level
- Income Range (when available)

This stage narrows thousands of schemes into a smaller candidate set before AI reasoning begins.

---

## Step 3 — Semantic Search

Many government scheme descriptions use different terminology for similar concepts.

Example:

Scheme A

"Financial assistance for higher education."

Scheme B

"Scholarship support for undergraduate students."

Although the wording differs, both describe similar opportunities.

To improve retrieval quality, NeuraScheme AI uses **Sentence Transformers** to generate vector embeddings for each scheme.

The embedding is generated using:

- Scheme Name
- Details
- Benefits
- Eligibility

These vectors are stored for semantic retrieval.

When the user submits a query, the query is converted into an embedding and compared against stored vectors.

This allows the system to retrieve relevant schemes even when exact keywords are not used.

---

# Step 4 — Eligibility Evaluation

The Eligibility Agent analyzes the retrieved schemes against the user's profile.

The agent evaluates conditions such as:

- State
- Occupation
- Income
- Gender
- Education
- Category
- Student Status
- Farmer Status

The goal is not simply to filter schemes but to determine how closely each scheme matches the user's profile.

---

# Step 5 — Recommendation Scoring

Each candidate scheme receives a recommendation score.

The score is calculated using multiple factors.

Example:

| Factor | Weight |
|----------|--------|
| State Match | 25% |
| Occupation Match | 20% |
| Income Match | 20% |
| Category Match | 15% |
| Education Match | 10% |
| Semantic Similarity | 10% |

These weights can be adjusted as the platform evolves.

The Recommendation Agent ranks schemes from highest to lowest score.

---

# Step 6 — AI Explanation Generation

Ranking alone is not sufficient.

Users should understand *why* a scheme is recommended.

The Assistant Agent sends structured information to the Gemini API to generate an easy-to-understand explanation.

Example:

> "This scheme is recommended because you are a student from Tamil Nadu with an annual family income below the eligibility threshold. Your educational background and age satisfy the required conditions."

This makes recommendations transparent and trustworthy.

---

# LangGraph Workflow

The platform orchestrates AI agents using LangGraph.

```
Start

↓

Load User Profile

↓

Retrieve Candidate Schemes

↓

Semantic Search

↓

Eligibility Evaluation

↓

Recommendation Ranking

↓

Generate Explanation

↓

Return Results
```

Each node receives structured JSON and returns structured JSON.

---

# Dataset Processing Pipeline

The application uses a Government Schemes dataset obtained from Kaggle.

The dataset is **not queried directly** by the application.

Instead, a preprocessing pipeline imports the dataset into MongoDB Atlas.

```
CSV Dataset

↓

Clean Missing Values

↓

Normalize Categories

↓

Generate Embeddings

↓

Store in MongoDB Atlas
```

---

# Dataset Cleaning

Before importing, the following preprocessing steps are performed.

## Remove Missing Values

Rows containing missing essential fields are removed or completed where possible.

---

## Normalize Categories

Example:

Original

Agriculture,Rural & Environment, Social welfare & Empowerment

Converted into

[
"Agriculture",
"Rural & Environment",
"Social Welfare & Empowerment"
]

This improves filtering and indexing.

---

## Clean Text

Remove:

- HTML
- Extra whitespace
- Escape characters
- Duplicate spaces

---

## Create Search Text

For semantic search, the following fields are combined into one searchable document.

- Scheme Name
- Details
- Benefits
- Eligibility

Example

```
Scholarship Scheme

Provides financial assistance...

Eligible students...

Benefits...
```

This combined text is converted into an embedding.

---

# MongoDB Atlas

MongoDB Atlas acts as the primary application database.

The Kaggle dataset is imported only once.

All future operations use MongoDB.

Benefits include:

- Fast querying
- Flexible schema
- Easy scaling
- Atlas Search support
- Vector Search support (optional)

---

# Database Collections

## users

Stores registered users.

Fields include:

- Personal information
- Profile
- Saved schemes
- Preferences

---

## schemes

Contains cleaned government scheme data imported from the Kaggle dataset.

Each document stores:

- Scheme Name
- Details
- Benefits
- Eligibility
- Documents
- Categories
- Level
- Embedding Reference (optional)

---

## recommendations

Stores recommendation history.

Fields include:

- User ID
- Scheme ID
- Recommendation Score
- Generated Explanation
- Timestamp

---

## conversations

Stores AI Assistant chat history.

Each conversation contains:

- User
- Messages
- Recommended Schemes
- Timestamp

---

## notifications

Stores:

- Deadline reminders
- New schemes
- Saved scheme updates
- Application reminders

---

# Backend Architecture

The backend is built using FastAPI and follows a modular architecture.

```
Frontend

↓

API Gateway

↓

Authentication

↓

Services

↓

AI Agents

↓

MongoDB Atlas

↓

Gemini API
```

Each layer has a single responsibility, making the project easier to maintain and extend.

---

# REST API Overview

The backend exposes REST APIs consumed by the React frontend.

Major API groups include:

### Authentication

- Register
- Login
- Refresh Token
- Logout

---

### User

- Get Profile
- Update Profile
- Upload Documents

---

### Schemes

- List Schemes
- Search Schemes
- Filter Schemes
- Get Scheme Details

---

### AI

- Eligibility Check
- Get Recommendations
- Ask AI Assistant
- Generate Explanation

---

### Saved Schemes

- Save Scheme
- Remove Scheme
- List Saved Schemes

---

### Notifications

- Get Notifications
- Mark as Read
- Delete Notification

---

### Admin

- Add Scheme
- Update Scheme
- Delete Scheme
- Import Dataset
- View Analytics

---

# Error Handling

The backend should gracefully handle:

- Invalid requests
- Missing profile data
- Expired JWT tokens
- AI service failures
- MongoDB connection issues
- External API timeouts

Meaningful error messages should always be returned to the frontend.

---

# Performance Optimizations

To ensure smooth user experience:

- Index frequently searched fields in MongoDB.
- Cache common search results.
- Generate embeddings only once during dataset import.
- Paginate search results.
- Use asynchronous FastAPI endpoints.
- Minimize unnecessary LLM calls by filtering candidates before explanation generation.
# 📂 Project Structure

The project is organized into separate frontend and backend applications to ensure modularity and maintainability.

```
NeuraScheme-AI/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── cards/
│   │   │   ├── forms/
│   │   │   ├── layout/
│   │   │   └── charts/
│   │   │
│   │   ├── pages/
│   │   │   ├── Landing/
│   │   │   ├── Login/
│   │   │   ├── Register/
│   │   │   ├── Dashboard/
│   │   │   ├── Explorer/
│   │   │   ├── SchemeDetails/
│   │   │   ├── Eligibility/
│   │   │   ├── Assistant/
│   │   │   ├── Saved/
│   │   │   ├── Notifications/
│   │   │   ├── Profile/
│   │   │   └── Admin/
│   │   │
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── context/
│   │   ├── routes/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── config/
│   │   ├── database/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── scripts/
│   │   ├── import_dataset.py
│   │   ├── clean_dataset.py
│   │   ├── generate_embeddings.py
│   │   └── create_indexes.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── dataset/
│   └── government_schemes.csv
│
├── docs/
│
└── README.md
```

---

# 🗄️ Database Design

MongoDB Atlas is used as the primary database.

## users Collection

Stores user accounts and profile information.

Example fields:

- name
- email
- password
- age
- gender
- occupation
- annualIncome
- education
- category
- state
- district
- savedSchemes
- preferences
- createdAt

---

## schemes Collection

Contains the cleaned Kaggle dataset.

Fields include:

- scheme_name
- slug
- details
- benefits
- eligibility
- application
- documents
- level
- schemeCategory
- embedding (optional)
- createdAt

---

## recommendations Collection

Stores recommendation history.

Fields:

- userId
- schemeId
- recommendationScore
- explanation
- generatedAt

---

## conversations Collection

Stores AI Assistant conversations.

Fields:

- userId
- messages
- recommendedSchemes
- createdAt

---

## notifications Collection

Stores all user notifications.

Examples:

- Deadline reminders
- New schemes
- Saved scheme updates
- Application reminders

---

# 🔐 Authentication

The platform uses JWT Authentication.

Authentication Flow

```
Register

↓

Login

↓

Generate JWT

↓

Protected Routes

↓

Refresh Token

↓

Logout
```

Protected routes include:

- Dashboard
- Profile
- Eligibility Checker
- Saved Schemes
- Notifications
- AI Assistant

Passwords should always be hashed before storage using bcrypt.

---

# ⚙️ Environment Variables

Backend

```env
MONGODB_URI=

DATABASE_NAME=

JWT_SECRET=

JWT_ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

GEMINI_API_KEY=

CHROMA_DB_PATH=

EMBEDDING_MODEL=

CORS_ORIGINS=
```

Frontend

```env
VITE_API_BASE_URL=

VITE_APP_NAME=NeuraScheme AI
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/NeuraScheme-AI.git

cd NeuraScheme-AI
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Import Dataset

```bash
python scripts/import_dataset.py
```

This script should:

- Load the Kaggle CSV
- Clean records
- Normalize categories
- Store data in MongoDB Atlas

---

## Generate Embeddings

```bash
python scripts/generate_embeddings.py
```

This script creates semantic embeddings for each scheme and stores them for similarity search.

---

# ☁️ Deployment

## Frontend

Recommended platforms:

- Vercel
- Netlify

---

## Backend

Recommended platforms:

- Render
- Railway
- Azure App Service

---

## Database

MongoDB Atlas

Deployment Checklist

- Configure environment variables
- Enable HTTPS
- Restrict database IP access
- Enable CORS
- Secure API keys

---

# 🧪 Testing Strategy

Testing should include:

### Unit Testing

- Authentication
- Recommendation logic
- Utility functions

---

### API Testing

- Login
- Registration
- Recommendation endpoint
- Search endpoint

---

### Integration Testing

- React ↔ FastAPI
- FastAPI ↔ MongoDB Atlas
- FastAPI ↔ Gemini API

---

### User Acceptance Testing

Validate:

- Registration flow
- Profile completion
- Eligibility checker
- AI recommendations
- Saved schemes
- Notifications

---

# 📈 Future Enhancements

Potential future improvements include:

- Regional language support
- Voice-based AI Assistant
- OCR for uploaded documents
- DigiLocker integration
- Aadhaar e-KYC (where legally and technically appropriate)
- WhatsApp notifications
- Mobile application
- Admin analytics dashboard
- Personalized learning using user feedback
- Real-time synchronization with government portals through official APIs

---

# 🛣️ Development Roadmap

## Phase 1

- User Authentication
- Dashboard
- MongoDB Integration
- Dataset Import

---

## Phase 2

- Search
- Eligibility Checker
- Recommendations
- AI Assistant

---

## Phase 3

- Notifications
- Saved Schemes
- Admin Dashboard
- Analytics

---

## Phase 4

- OCR
- Voice Assistant
- Mobile App
- Government API Integration

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

Please ensure that:

- Code is documented.
- APIs follow REST conventions.
- Components are reusable.
- Commit messages are descriptive.

---

# 📄 License

This project is licensed under the MIT License.

---

# 🙏 Acknowledgements

This project would not be possible without the following technologies and resources:

- React
- FastAPI
- MongoDB Atlas
- LangGraph
- Google Gemini API
- Sentence Transformers
- ChromaDB
- Kaggle Government Schemes Dataset
- Vercel
- Render

---

# 👨‍💻 Team

Developed as part of a hackathon project focused on AI-powered Decision Intelligence for Government Scheme Discovery.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star on GitHub!

**NeuraScheme AI — Making Government Schemes Accessible Through Artificial Intelligence**

2. Eligibility Explanation Agent
Overview

The Eligibility Explanation Agent is responsible for providing transparent and human-readable explanations for every eligibility decision made by the platform. Rather than simply indicating whether a user qualifies for a scheme, the agent analyzes the eligibility criteria, compares them with the user's profile, identifies matched and unmatched conditions, and explains the reasoning behind the final decision.

This improves transparency, increases user trust, and helps users understand why certain schemes were recommended while others were not.

Why This Agent?

Most government portals only state:

❌ Not Eligible

without explaining the reason.

Similarly, many recommendation systems simply display:

Recommended

without any justification.

NeuraScheme AI addresses this by making every recommendation explainable.

Responsibilities

The Eligibility Explanation Agent performs the following tasks:

Analyze scheme eligibility conditions
Compare them with the user's profile
Identify satisfied conditions
Identify missing conditions
Explain why a scheme was recommended
Explain why a scheme was rejected
Suggest profile improvements where applicable
Workflow
User Profile
      │
      ▼
Eligibility Evaluation
      │
      ▼
Matched Conditions
Missing Conditions
      │
      ▼
Eligibility Explanation Agent
      │
      ▼
Human-Friendly Explanation
Example 1 – Eligible Scheme
User Profile
Age: 20

Gender: Female

State: Tamil Nadu

Occupation: Student

Annual Income: ₹2,20,000
Scheme Requirements
Student

Female

Income < ₹2,50,000

Resident of Tamil Nadu
AI Explanation

✅ You are eligible for this scheme because your profile satisfies all required criteria. You are a female student residing in Tamil Nadu, and your annual family income is below the specified limit of ₹2,50,000.

Example 2 – Not Eligible
User Profile
Occupation: Engineer

Income: ₹7,00,000

State: Karnataka
Scheme Requirements
Farmer

Income < ₹5,00,000

Resident of Karnataka
AI Explanation

❌ You are currently not eligible for this scheme because it is intended exclusively for registered farmers. Additionally, your reported annual income exceeds the maximum eligibility limit of ₹5,00,000.

Improvement Suggestions

Rather than stopping at "Not Eligible," the agent provides constructive guidance.

Example:

Although you do not qualify for this farmer subsidy, you may be eligible for MSME development schemes based on your occupation. Explore the recommended alternatives below.

UI Example
Eligibility Score

92%

✔ Resident of Tamil Nadu

✔ Student

✔ Female

✔ Income within limit

✔ Age criteria satisfied

──────────────────────────

Why Recommended

This scholarship is a strong match because all eligibility conditions are satisfied.

──────────────────────────

Confidence

High
Not Eligible Card
Eligibility Score

42%

✔ Karnataka Resident

✔ Age Requirement Met

✖ Not a Farmer

✖ Income exceeds limit

──────────────────────────

Why Not Eligible

The scheme is intended only for registered farmers with an annual income below ₹5,00,000.

Suggested Alternatives

• Farmer Welfare Scheme B

• MSME Support Scheme

• Startup Assistance Program
Benefits
Builds user trust
Makes AI decisions transparent
Helps users understand eligibility rules
Reduces confusion
Provides actionable alternatives
Improves overall user experience
3. Recommendation Confidence Score
Overview

The Recommendation Confidence Score represents how strongly the system believes a scheme matches a user's profile. Unlike the Eligibility Score, which measures compliance with official scheme requirements, the Confidence Score reflects the overall reliability of the recommendation by combining multiple signals.

This helps users understand not only whether they qualify, but also how suitable the recommendation is based on the available information.

Eligibility Score vs Confidence Score
Eligibility Score	Confidence Score
Checks if the user satisfies the scheme rules	Indicates how confident the AI is in recommending the scheme
Based on rule matching	Based on multiple recommendation signals
Binary or weighted criteria	Semantic, profile, and rule-based reasoning
Measures qualification	Measures recommendation quality
Factors Used

The Recommendation Agent calculates the confidence score using several components.

Factor	Weight
Eligibility Rule Match	40%
Semantic Similarity	25%
User Profile Completeness	15%
Category Match	10%
State Match	10%

The final score is normalized to a percentage.

Confidence Levels
Score	Interpretation
90–100	Very High Confidence
75–89	High Confidence
60–74	Moderate Confidence
Below 60	Low Confidence
Example 1
Scheme

National Scholarship Program

Eligibility Score

100%

Confidence Score

96%

Reason

Your profile satisfies all eligibility conditions. The scheme category aligns closely with your educational background, income level, and location, resulting in a highly reliable recommendation.
Example 2
Scheme

Women Entrepreneur Support Scheme

Eligibility Score

82%

Confidence Score

71%

Reason

You satisfy most eligibility conditions, but your occupation information is incomplete. Completing your profile may improve the accuracy of future recommendations.
Example 3
Scheme

Agricultural Equipment Subsidy

Eligibility Score

58%

Confidence Score

43%

Reason

Although there is some similarity between your profile and the scheme, critical eligibility conditions such as occupation and farmer status are not satisfied. Alternative schemes may be more suitable.
UI Display

Each recommendation card can include both metrics:

National Scholarship Scheme

Eligibility Score

95%

Confidence Score

93%

★★★★★ Excellent Match

──────────────────────────

Why this Scheme?

• Student status matched

• Income within limit

• State matched

• Education criteria satisfied

• Strong semantic similarity
Visual Indicator
🟢 90–100  Excellent Match

🟢 75–89   Strong Match

🟡 60–74   Moderate Match

🔴 Below 60 Weak Match
Benefits
Makes recommendations more trustworthy
Explains recommendation quality
Helps users prioritize schemes
Reduces blind reliance on AI
Provides a transparent, explainable decision-making process
Combined Example

Instead of showing only:

Recommended Scheme

NeuraScheme AI presents:

🎓 National Scholarship Scheme

Eligibility Score: 95%

Confidence Score: 93%

★★★★★ Excellent Match

Why Recommended?

✓ You are a student

✓ Your income is below the eligibility limit

✓ Your state is supported

✓ Your age falls within the required range

✓ Your educational profile aligns with the scheme

Required Documents

• Aadhaar Card

• Income Certificate

• Student ID

• Bank Passbook

Next Step

Click "View Details" to review the application process and required documentation.

</div>
