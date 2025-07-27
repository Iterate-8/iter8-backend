# Environment Variables Setup Guide

## Quick Setup

1. **Run the setup script:**
   ```bash
   ./setup_conda.sh
   ```

2. **Edit the `.env` file** with your actual values (see details below)

3. **Start the application:**
   ```bash
   ./start_conda.sh
   ```

## Required Environment Variables

### 1. Supabase Configuration

You need to get these values from your Supabase project:

#### DATABASE_URL
- **Location:** Supabase Dashboard → Settings → Database
- **Format:** `postgresql+asyncpg://postgres:your_password@db.your_project_ref.supabase.co:5432/postgres`
- **Example:** `postgresql+asyncpg://postgres:mypassword123@db.abcdefghijklmnop.supabase.co:5432/postgres`

#### SUPABASE_URL
- **Location:** Supabase Dashboard → Settings → API
- **Format:** `https://your_project_ref.supabase.co`
- **Example:** `https://abcdefghijklmnop.supabase.co`

#### SUPABASE_ANON_KEY
- **Location:** Supabase Dashboard → Settings → API → Project API keys
- **Note:** This is the "anon" key (public)
- **Example:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### SUPABASE_SERVICE_ROLE_KEY
- **Location:** Supabase Dashboard → Settings → API → Project API keys
- **Note:** This is the "service_role" key (private - keep secret!)
- **Example:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 2. Security Configuration

#### SECRET_KEY
Generate a strong random key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Example:** `my_super_secret_key_that_is_very_long_and_random_12345`

### 3. Application Configuration

#### DEBUG
- **Development:** `True`
- **Production:** `False`

#### ENVIRONMENT
- **Development:** `development`
- **Production:** `production`

#### LOG_LEVEL
- **Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Recommended:** `INFO` for production, `DEBUG` for development

### 4. Server Configuration

#### HOST
- **Development:** `0.0.0.0` (all interfaces)
- **Production:** `0.0.0.0` or specific IP

#### PORT
- **Default:** `8000`
- **Change if needed:** `8080`, `3000`, etc.

### 5. CORS Configuration

#### CORS_ORIGINS
- **Development:** `http://localhost:3000,http://localhost:8080`
- **Production:** `https://yourdomain.com,https://app.yourdomain.com`

## Example .env File

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:mypassword123@db.abcdefghijklmnop.supabase.co:5432/postgres

# Supabase Configuration
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzNjU0NzIwMCwiZXhwIjoxOTUyMTIzMjAwfQ.example
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM2NTQ3MjAwLCJleHAiOjE5NTIxMjMyMDB9.example

# Application Configuration
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security Configuration
SECRET_KEY=my_super_secret_key_that_is_very_long_and_random_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Getting Supabase Credentials

### Step 1: Create a Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login
3. Create a new project
4. Wait for the project to be ready

### Step 2: Get Database URL
1. Go to **Settings** → **Database**
2. Copy the **Connection string**
3. Replace `postgresql://` with `postgresql+asyncpg://`

### Step 3: Get API Keys
1. Go to **Settings** → **API**
2. Copy the **Project URL** (for SUPABASE_URL)
3. Copy the **anon public** key (for SUPABASE_ANON_KEY)
4. Copy the **service_role secret** key (for SUPABASE_SERVICE_ROLE_KEY)

## Troubleshooting

### Common Issues

1. **"Database connection failed"**
   - Check your DATABASE_URL format
   - Verify your Supabase project is active
   - Check if your IP is allowed in Supabase

2. **"Invalid API key"**
   - Make sure you're using the correct keys
   - Check if keys are copied completely

3. **"CORS error"**
   - Update CORS_ORIGINS with your frontend URL
   - Make sure the URL format is correct

### Testing Connection

You can test your database connection with:

```bash
conda activate iter8-backend
python -c "
import asyncio
from app.database import engine
async def test():
    try:
        async with engine.begin() as conn:
            print('✅ Database connection successful!')
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
asyncio.run(test())
"
```

## Security Notes

- **Never commit `.env` files** to version control
- **Keep your service role key secret** - it has admin privileges
- **Use strong secret keys** for production
- **Limit CORS origins** in production
- **Set DEBUG=False** in production 