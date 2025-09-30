# Vercel Deployment Guide for Iter8 Backend

This guide provides step-by-step instructions to deploy your FastAPI GraphQL backend to Vercel's serverless platform.

## 🌟 Why Vercel?

- **Free Tier**: Generous free tier with good limits
- **Serverless**: Automatic scaling, pay-per-use
- **Fast Deployments**: Git-based deployments
- **Global CDN**: Fast worldwide performance
- **Zero Configuration**: Works out of the box

## Prerequisites

1. **Vercel Account** - Sign up at https://vercel.com/
2. **Git Repository** - Your code should be in a Git repository
3. **Vercel CLI** (optional) - For command-line deployment
4. **Supabase Database** (already configured in your project)

## 🚀 Step-by-Step Deployment

### Method 1: Deploy via Vercel Dashboard (Recommended)

#### 1. **Prepare Your Repository**

Make sure all the Vercel configuration files are committed:

```bash
cd /Users/priyadarsimishra/Desktop/iter8/iter8-backend

# Add all Vercel configuration files
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

#### 2. **Connect to Vercel**

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"New Project"**
3. Import your Git repository (GitHub/GitLab/Bitbucket)
4. Select your `iter8-backend` repository

#### 3. **Configure Environment Variables**

In the Vercel dashboard, under **Environment Variables**, add:

```bash
# Database Configuration
DATABASE_URL = postgresql://postgres:iter8password&$123@db.eousczgdnqjsnjnkcswq.supabase.co:5432/postgres

# Supabase Configuration  
SUPABASE_URL = https://eousczgdnqjsnjnkcswq.supabase.co
SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvdXNjemdkbnFqc25qbmtjc3dxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NDA5NjIsImV4cCI6MjA2ODIxNjk2Mn0.MbOlaNtuJl-V5gFRjB8zk1AazXkIRM0HkahWT2Fjxxk
SUPABASE_SERVICE_ROLE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvdXNjemdkbnFqc25qbmtjc3dxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjY0MDk2MiwiZXhwIjoyMDY4MjE2OTYyfQ.N3TSZ3giUJvQRY7sT4Vjnu-iVWke3KBtTEZ2OXKFWlU

# Application Configuration
SECRET_KEY = [Generate a secure key - use a password generator]
DEBUG = False
ENVIRONMENT = production
LOG_LEVEL = INFO
CORS_ORIGINS = *
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

**⚠️ Security Note**: Generate a strong SECRET_KEY using:
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### 4. **Deploy**

1. Click **"Deploy"**
2. Vercel will automatically:
   - Detect it's a Python project
   - Install dependencies from `requirements-vercel.txt`
   - Build and deploy your application

#### 5. **Access Your API**

Once deployed, you'll get a URL like: `https://your-project-name.vercel.app`

### Method 2: Deploy via Vercel CLI

#### 1. **Install Vercel CLI**

```bash
npm install -g vercel
```

#### 2. **Login to Vercel**

```bash
vercel login
```

#### 3. **Deploy**

```bash
cd /Users/priyadarsimishra/Desktop/iter8/iter8-backend

# First deployment (will ask for configuration)
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N (for new project)
# - Project name? iter8-backend
# - Directory? ./
```

#### 4. **Set Environment Variables**

```bash
# Add each environment variable
vercel env add DATABASE_URL
# Enter the value when prompted

vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY
vercel env add SUPABASE_SERVICE_ROLE_KEY
vercel env add SECRET_KEY
vercel env add DEBUG
vercel env add ENVIRONMENT
vercel env add CORS_ORIGINS
```

#### 5. **Redeploy with Environment Variables**

```bash
vercel --prod
```

## 📁 Configuration Files Created

The following files have been created for your Vercel deployment:

### Core Configuration
- **`vercel.json`** - Vercel deployment configuration
- **`api/index.py`** - Serverless entry point
- **`requirements-vercel.txt`** - Optimized dependencies for serverless

### Serverless-Optimized Code
- **`app/vercel_main.py`** - FastAPI app optimized for serverless
- **`app/vercel_database.py`** - Database connections for serverless
- **`app/graphql/vercel_queries.py`** - GraphQL queries for serverless
- **`app/graphql/vercel_schema.py`** - GraphQL schema for serverless

## 🔧 Key Optimizations for Vercel

### 1. **Serverless Architecture**
- No connection pooling (connections per request)
- Removed lifespan events (incompatible with serverless)
- Added Mangum adapter for AWS Lambda compatibility

### 2. **Performance Optimizations**
- Shorter database timeouts (30s vs 60s)
- Optimized for cold starts
- Reduced function duration limits

### 3. **Environment Handling**
- Proper environment variable mapping
- Production-ready defaults
- CORS configuration for frontend integration

## 🧪 Testing Your Deployment

### 1. **Basic Endpoints**

```bash
# Test root endpoint
curl https://your-project-name.vercel.app/

# Test health check
curl https://your-project-name.vercel.app/health

# Test GraphQL endpoint
curl -X POST https://your-project-name.vercel.app/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { __typename }"}'
```

### 2. **GraphiQL Interface**

Visit: `https://your-project-name.vercel.app/graphql` (only available if DEBUG=True)

### 3. **Example GraphQL Query**

```graphql
query GetFeedbackList {
  getFeedbackList(limit: 5) {
    success
    message
    feedbackList {
      id
      feedbackType
      feedback
      startupName
      createdAt
    }
    totalCount
  }
}
```

## 📊 Vercel Free Tier Limits

- **Function Execution**: 100GB-Hours per month
- **Function Duration**: 10 seconds (Hobby), 60 seconds (Pro)
- **Deployments**: Unlimited
- **Bandwidth**: 100GB per month
- **Custom Domains**: Included
- **Serverless Functions**: 12 per deployment (Hobby)

## 🔧 Advanced Configuration

### Custom Domain

1. In Vercel dashboard, go to **Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration instructions

### Environment-Specific Deployments

```bash
# Development branch
vercel

# Production deployment
vercel --prod

# Specific branch deployment  
vercel --target production
```

### Function Configuration

You can customize function settings in `vercel.json`:

```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "memory": 1024
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. **Build Fails**
```bash
# Check build logs in Vercel dashboard
# Common causes:
# - Missing dependencies in requirements-vercel.txt
# - Import errors in serverless code
```

#### 2. **Function Timeout**
```bash
# Increase timeout in vercel.json (max 60s for Pro plan)
# Optimize database queries
# Check for infinite loops
```

#### 3. **Database Connection Issues**
```bash
# Verify DATABASE_URL environment variable
# Check Supabase connection limits
# Ensure SSL is properly configured
```

#### 4. **CORS Issues**
```bash
# Update CORS_ORIGINS environment variable
# Format: "https://yourdomain.com,http://localhost:3000"
```

### Debugging Tips

#### 1. **View Function Logs**
- Go to Vercel dashboard → Functions tab
- Click on any function to see logs
- Use `print()` statements for debugging

#### 2. **Local Testing**
```bash
# Install Vercel CLI
npm install -g vercel

# Run locally
vercel dev

# This will run your serverless functions locally
```

#### 3. **Environment Variables**
```bash
# List all environment variables
vercel env ls

# Add environment variable
vercel env add VARIABLE_NAME

# Remove environment variable  
vercel env rm VARIABLE_NAME
```

## 🚀 Performance Optimization

### 1. **Cold Start Optimization**
- Keep imports minimal in entry points
- Use lazy loading for heavy dependencies
- Consider connection reuse strategies

### 2. **Database Optimization**
- Use connection per request (already implemented)
- Optimize queries for speed
- Consider caching for read-heavy operations

### 3. **Monitoring**
- Enable Vercel Analytics
- Monitor function execution times
- Set up error tracking

## 🔐 Security Best Practices

### 1. **Environment Variables**
- Never commit secrets to git
- Use Vercel's environment variable system
- Rotate secrets regularly

### 2. **CORS Configuration**
- Don't use `*` in production unless necessary
- Specify exact domains for frontend apps

### 3. **Database Security**
- Use Supabase Row Level Security (RLS)
- Limit database user permissions
- Enable connection SSL

## 💰 Cost Considerations

### Free Tier
- Perfect for development and small projects
- Good for testing and prototyping

### Pro Tier ($20/month)
- Higher function execution limits
- Longer function duration (60s)
- Priority support
- Advanced analytics

## 📈 Scaling Considerations

### Horizontal Scaling
- Vercel automatically scales functions
- No server management required
- Pay-per-execution model

### Database Scaling
- Supabase handles database scaling
- Consider connection pooling with PgBouncer
- Monitor database performance

## 🎯 Next Steps

1. **Custom Domain**: Set up your domain name
2. **Monitoring**: Add application monitoring
3. **CI/CD**: Set up automated deployments
4. **Testing**: Implement automated testing
5. **Documentation**: Update API documentation
6. **Error Tracking**: Add error monitoring service

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL Documentation](https://strawberry.rocks/)
- [Supabase Documentation](https://supabase.com/docs)

## 🆘 Support

- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **FastAPI Community**: [github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

---

Your FastAPI GraphQL backend is now ready for serverless deployment on Vercel! 🎉
