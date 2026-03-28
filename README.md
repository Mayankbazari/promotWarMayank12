# AI Emergency Decision Agent

A multi-agent AI-powered emergency analysis system that classifies emergencies and generates structured action plans using Google Gemini.

## Architecture

```
User Input (text)
        ↓
Emergency Classifier Agent (Gemini)
        ↓
Planner Agent (decides flow)
        ↓
Specialized Agents
  ├─ Medical Agent
  └─ Accident Agent
        ↓
Tools (emergency numbers, severity rules)
        ↓
Final Structured Action Plan
```

## Tech Stack

| Layer      | Technology              |
|------------|------------------------|
| Backend    | FastAPI + Python 3.12  |
| Frontend   | React + Vite           |
| AI         | Google Gemini API      |
| Deployment | Cloud Run + Docker     |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Gemini API key

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your GEMINI_API_KEY
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### Run Tests

```bash
cd backend
pytest tests/ -v
```

## Deployment (Cloud Run)

```bash
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/emergency-agent
gcloud run deploy emergency-agent --image gcr.io/PROJECT_ID/emergency-agent
```

## License

MIT
