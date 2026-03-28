# AI Fitness & Diet Planner

A multi-agent AI-powered fitness and diet planning application built with FastAPI, React, and Google Gemini.

## Overview

This project implements an orchestrator pattern with three specialized AI agents:

- **Planner Agent** — Analyzes user health data and coordinates the workflow
- **Fitness Agent** — Generates personalized workout plans
- **Diet Agent** — Creates tailored nutrition and meal plans

## Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Backend   | FastAPI + Python    |
| Frontend  | React + Vite        |
| AI        | Google Gemini API   |
| Alt. UI   | Streamlit           |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Gemini API key

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

## License

MIT
