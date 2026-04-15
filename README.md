# Sales Assistant API

A sophisticated AI-powered sales assistant API built with FastAPI, featuring Retrieval-Augmented Generation (RAG), intelligent lead scoring, and caching capabilities.

## Architecture

This project follows a clean, layered architecture:

- **app/**: Main application package
  - **core/**: Configuration and settings
  - **models/**: Pydantic data models
  - **repositories/**: Data access layer (knowledge base)
  - **services/**: Business logic layer
  - **routers/**: API endpoints
  - **utils/**: Utility functions
- **data/**: Static data files (knowledge base)
- **tests/**: Unit and integration tests

## Features

- **Intelligent Chat**: AI-powered responses using OpenAI GPT models
- **RAG Integration**: Context-aware responses from knowledge base
- **Lead Scoring**: Automatic lead qualification and categorization
- **Caching**: Response caching for improved performance
- **RESTful API**: Clean, documented endpoints

## Installation

1. Clone the repository.
2. Create a `.env` file in the project root and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=seu_api_key_aqui
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

> The application will read `OPENAI_API_KEY` from the environment. It also supports loading the key from `../auth/openai_key.txt` if `.env` is not present.

## Running locally

Run the application:

```bash
python run.py
```

The API will be available at `http://localhost:8000`

## Running with Docker

Build and start the service using Docker Compose:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Endpoints

- `POST /chat`: Process chat messages with JSON body
- `GET /health-check`: Health check endpoint


## Testing

Run the test suite with:

```bash
pytest
```

## Development

The project uses:
- FastAPI for the web framework
- Pydantic for data validation
- OpenAI API for LLM interactions
- JSON-based knowledge base for RAG
