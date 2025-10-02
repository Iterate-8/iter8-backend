"""
Vercel serverless entry point using Mangum for ASGI support.
"""

from fastapi import FastAPI
from mangum import Mangum

# Create simple FastAPI app
app = FastAPI(title="Iter8 Backend")

@app.get("/")
def root():
    return {"message": "Hello from Vercel!", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "platform": "Vercel"}

# Wrap with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app)
