"""
Check environment variables.
"""

from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def check_env():
    return {
        "DATABASE_URL_set": "DATABASE_URL" in os.environ,
        "DATABASE_URL_length": len(os.environ.get("DATABASE_URL", "")) if "DATABASE_URL" in os.environ else 0,
        "SUPABASE_URL_set": "SUPABASE_URL" in os.environ,
        "SUPABASE_ANON_KEY_set": "SUPABASE_ANON_KEY" in os.environ,
        "SUPABASE_SERVICE_ROLE_KEY_set": "SUPABASE_SERVICE_ROLE_KEY" in os.environ,
        "all_env_keys": [k for k in os.environ.keys() if not k.startswith("_")]
    }

