"""
Vercel serverless entry point.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Simple test app first
app = FastAPI(title="Iter8 Backend")

@app.get("/")
def root():
    return {"message": "Hello from Vercel!", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "platform": "Vercel"}
