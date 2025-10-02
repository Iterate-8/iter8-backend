"""
Vercel serverless entry point.
"""

from fastapi import FastAPI
from mangum import Mangum

# Create FastAPI app
app = FastAPI(title="Iter8 Backend")

@app.get("/")
def root():
    return {"message": "Hello from Vercel!", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "platform": "Vercel"}

# Vercel handler - wraps FastAPI with Mangum
handler = Mangum(app, lifespan="off")
