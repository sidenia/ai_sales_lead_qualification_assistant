from fastapi import FastAPI

from app.routers.chat import router as chat_router

app = FastAPI(
    title="Sales Assistant API",
    description="AI-powered sales assistant with simple RAG and lead scoring",
    version="1.0.0"
)

app.include_router(chat_router)


@app.get("/health-check") # at root for compatibility with load balancers
def health_check():
    return {"status": "healthy"}