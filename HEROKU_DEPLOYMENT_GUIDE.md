# Heroku Deployment Guide for Iter8 Backend

This guide provides step-by-step instructions to deploy your FastAPI GraphQL backend to Heroku.

## Prerequisites

1. **Heroku CLI installed** - Download from https://devcenter.heroku.com/articles/heroku-cli
2. **Git initialized** in your project directory
3. **Heroku account** - Sign up at https://signup.heroku.com/
4. **Supabase database** (already configured in your project)

## Step-by-Step Deployment

### 1. Install Heroku CLI (if not already installed)

```bash
# On macOS
brew tap heroku/brew && brew install heroku

# On Ubuntu/Debian
sudo snap install --classic heroku

# On Windows - Download installer from Heroku website
```

### 2. Login to Heroku

```bash
heroku login
```

This will open your browser for authentication.

### 3. Create a Heroku Application

```bash
# Navigate to your project directory
cd /Users/priyadarsimishra/Desktop/iter8/iter8-backend

# Create a new Heroku app (replace 'your-app-name' with a unique name)
heroku create your-iter8-backend

# Alternative: Let Heroku generate a random name
heroku create
```

### 4. Set Environment Variables

Set your environment variables on Heroku (replace with your actual values):

```bash
# Database Configuration (your existing Supabase connection)
heroku config:set DATABASE_URL="postgresql://postgres:iter8password&$123@db.eousczgdnqjsnjnkcswq.supabase.co:5432/postgres"

# Supabase Configuration
heroku config:set SUPABASE_URL="https://eousczgdnqjsnjnkcswq.supabase.co"
heroku config:set SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvdXNjemdkbnFqc25qbmtjc3dxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NDA5NjIsImV4cCI6MjA2ODIxNjk2Mn0.MbOlaNtuJl-V5gFRjB8zk1AazXkIRM0HkahWT2Fjxxk"
heroku config:set SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvdXNjemdkbnFqc25qbmtjc3dxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjY0MDk2MiwiZXhwIjoyMDY4MjE2OTYyfQ.N3TSZ3giUJvQRY7sT4Vjnu-iVWke3KBtTEZ2OXKFWlU"

# Application Configuration
heroku config:set DEBUG=False
heroku config:set ENVIRONMENT=production
heroku config:set LOG_LEVEL=INFO

# Security (generate a strong secret key)
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# CORS (adjust as needed for your frontend domains)
heroku config:set CORS_ORIGINS="*"

# Additional configuration
heroku config:set ALGORITHM=HS256
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Commit Your Changes

Make sure all new files are committed to git:

```bash
# Add all files
git add .

# Commit changes
git commit -m "Add Heroku deployment configuration"
```

### 6. Deploy to Heroku

```bash
# Deploy to Heroku
git push heroku main

# If your main branch is named 'master'
# git push heroku master
```

### 7. Scale the Application

```bash
# Ensure at least one web dyno is running
heroku ps:scale web=1
```

### 8. Open Your Application

```bash
# Open the app in your browser
heroku open

# Or get the URL
heroku info
```

## Configuration Files Created

The following files have been created for your Heroku deployment:

- **`Procfile`** - Tells Heroku how to run your application
- **`runtime.txt`** - Specifies Python version
- **`app.json`** - Heroku app configuration and environment variables
- **`requirements.txt`** - Updated with gunicorn for production
- **`Procfile.gunicorn`** - Alternative configuration using gunicorn (better performance)

## Alternative: Using Gunicorn for Better Performance

For better production performance, you can use the gunicorn configuration:

```bash
# Replace the current Procfile with the gunicorn version
mv Procfile Procfile.uvicorn
mv Procfile.gunicorn Procfile

# Commit and deploy
git add .
git commit -m "Switch to gunicorn for production"
git push heroku main
```

## Verifying Your Deployment

### 1. Check Application Status

```bash
# View application logs
heroku logs --tail

# Check dyno status
heroku ps
```

### 2. Test Your API Endpoints

```bash
# Test the root endpoint
curl https://your-app-name.herokuapp.com/

# Test the health endpoint
curl https://your-app-name.herokuapp.com/health

# Test GraphQL endpoint (replace with your app URL)
curl -X POST https://your-app-name.herokuapp.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { __typename }"}'
```

### 3. Access GraphiQL Interface

In production, GraphiQL is disabled by default. To enable it temporarily for testing:

```bash
heroku config:set DEBUG=True
```

Then visit: `https://your-app-name.herokuapp.com/graphql`

**Remember to disable debug mode after testing:**

```bash
heroku config:set DEBUG=False
```

## Database Setup

Your Supabase database should work automatically. If you need to run any database migrations:

```bash
# Run a one-off command to initialize database tables
heroku run python -c "
import asyncio
from app.database import init_db
asyncio.run(init_db())
"
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SUPABASE_URL` | Your Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | `eyJ...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | `eyJ...` |
| `SECRET_KEY` | JWT secret key | Auto-generated |
| `DEBUG` | Debug mode | `False` |
| `ENVIRONMENT` | Environment name | `production` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` or specific domains |

## Troubleshooting

### Common Issues

1. **Application crashes on startup**
   ```bash
   heroku logs --tail
   ```
   Check for missing environment variables or syntax errors.

2. **Database connection issues**
   - Verify `DATABASE_URL` is correctly set
   - Ensure Supabase allows connections from Heroku IPs

3. **CORS issues**
   - Update `CORS_ORIGINS` to include your frontend domain
   ```bash
   heroku config:set CORS_ORIGINS="https://your-frontend.com,http://localhost:3000"
   ```

4. **Memory or performance issues**
   - Consider upgrading dyno type
   ```bash
   heroku dyno:type web=standard-1x
   ```

### Useful Commands

```bash
# View app information
heroku info

# View configuration variables
heroku config

# View recent logs
heroku logs --tail

# Restart the application
heroku restart

# Run a one-off command
heroku run python --version

# Access a remote shell
heroku run bash
```

## Security Considerations

1. **Never commit sensitive data** - Use environment variables
2. **Use strong secret keys** - Generate with `secrets.token_urlsafe(32)`
3. **Configure CORS properly** - Don't use `*` in production unless necessary
4. **Enable HTTPS only** - Heroku provides SSL certificates
5. **Regular updates** - Keep dependencies updated

## Cost Considerations

- **Eco dynos** - Free tier with some limitations
- **Basic dynos** - $7/month, no sleep mode
- **Standard dynos** - Starting at $25/month, more resources

## Next Steps

1. **Custom domain** - Configure your own domain name
2. **Add logging** - Integrate with logging services like Papertrail
3. **Monitoring** - Add application monitoring
4. **CI/CD** - Set up automated deployments from GitHub

## Support

For issues:
- Heroku Documentation: https://devcenter.heroku.com/
- Heroku Support: https://help.heroku.com/
- FastAPI Documentation: https://fastapi.tiangolo.com/
