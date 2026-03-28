# Stage 1: Build Frontend (React)
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build Backend (FastAPI) and Serve Both
FROM python:3.9-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend assets from Stage 1 into the backend's static directory
COPY --from=frontend-builder /frontend/dist ./static

# Cloud Run sets the PORT env variable
ENV PORT=8000
EXPOSE ${PORT}

# Run the app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
