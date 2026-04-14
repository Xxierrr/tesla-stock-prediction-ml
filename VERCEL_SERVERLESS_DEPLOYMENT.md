# TeslaPulse - Vercel Serverless Deployment Guide

## Architecture
Your Flask backend has been converted to **Vercel Python Serverless Functions**. Each API route is now an individual serverless function.

## Project Structure
```
tesla-stock-prediction-ml/
├── api/                          # Serverless functions
│   ├── stock-data.py            # /api/stock-data endpoint
│   ├── realtime.py              # /api/realtime endpoint
│   ├── eda.py                   # /api/eda endpoint
│   └── health.py                # /api/health endpoint
├── backend/                      # Shared backend code
│   ├── services/                # Business logic
│   ├── utils/                   # Utilities
│   ├── models/                  # ML models
│   ├── data/                    # Data files
│   └── config.py                # Configuration
├── frontend/                     # React app
│   ├── src/
│   ├── dist/                    # Build output
│   └── package.json
├── requirements.txt             # Python dependencies (root level)
└── vercel.json                  # Vercel configuration
```

## How It Works

### Serverless Functions
Each file in `/api` folder becomes a serverless endpoint:
- `api/stock-data.py` → `/api/stock-data`
- `api/realtime.py` → `/api/realtime`
- `api/eda.py` → `/api/eda`

### Function Format
```python
def handler(event, context):
    # event contains query params, body, headers
    # context contains request metadata
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json_string
    }
```

## Deployment Steps

### 1. Commit and Push
```bash
git add .
git commit -m "Convert to Vercel serverless functions"
git push
```

### 2. Configure Vercel Project

#### Option A: New Deployment
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import `Xxierrr/tesla-stock-prediction-ml`
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: Leave empty (monorepo)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: Leave empty or set to your Vercel domain
6. Click "Deploy"

#### Option B: Update Existing Deployment
1. Go to your existing Vercel project
2. Settings → General
3. **Root Directory**: Leave empty
4. **Build Command**: `cd frontend && npm install && npm run build`
5. **Output Directory**: `frontend/dist`
6. Save and redeploy

### 3. Verify Deployment

Test your endpoints:
- Frontend: `https://your-app.vercel.app`
- Health: `https://your-app.vercel.app/api/health`
- Realtime: `https://your-app.vercel.app/api/realtime`
- Stock Data: `https://your-app.vercel.app/api/stock-data?start=2020-01-01&end=2024-12-31`

## Frontend Configuration

Your React app already uses environment variables for the API URL:

```javascript
// frontend/src/services/api.js
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';
```

### For Vercel Deployment
Since frontend and backend are on the same domain, you can:

**Option 1: Use relative URLs (Recommended)**
Set `VITE_API_URL` to empty string or don't set it, then update api.js:
```javascript
const API_BASE = import.meta.env.VITE_API_URL || '';
```

**Option 2: Use full URL**
Set `VITE_API_URL` to your Vercel domain:
```
VITE_API_URL=https://your-app.vercel.app
```

## Local Development

### Backend (Serverless Functions)
You can still run Flask locally for development:
```bash
cd backend
python app.py
# Runs on http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

Create `frontend/.env.local`:
```
VITE_API_URL=http://localhost:5000
```

## Vercel Serverless Limitations

### Free Tier
- **Execution Time**: 10 seconds max per function
- **Memory**: 1024 MB
- **Deployments**: 100/day
- **Bandwidth**: 100 GB/month

### Important Notes
1. **No Persistent Storage**: Files written during execution are lost
   - ML models must be in repo or loaded from external storage
   - Database writes won't persist (use external DB)

2. **Cold Starts**: First request after inactivity takes 1-3 seconds

3. **Timeouts**: Long-running operations (like model training) may timeout
   - Consider breaking into smaller operations
   - Or use Render/Railway for training endpoints

## Troubleshooting

### 404 Errors on /api/*
- Check `vercel.json` routes are correct
- Verify serverless function files exist in `/api` folder
- Check Vercel build logs

### Import Errors
- Ensure `requirements.txt` is at root level
- Check `sys.path.insert` in serverless functions
- Verify all dependencies are listed

### CORS Errors
- Check `Access-Control-Allow-Origin` headers in function responses
- Verify frontend domain is allowed

### Timeout Errors
- Reduce data processing in single request
- Cache results when possible
- Consider pagination for large datasets

### Model Loading Issues
- Ensure `.pkl` files are in repo
- Check file paths are relative
- Verify scikit-learn version matches

## Monitoring

### Vercel Dashboard
- **Functions**: View serverless function logs
- **Analytics**: Monitor performance
- **Logs**: Real-time request logs

### Debugging
Add logging in your functions:
```python
print(f"Debug: {variable}")  # Shows in Vercel logs
```

## Cost Optimization

### Free Tier Tips
1. **Cache Responses**: Reduce function invocations
2. **Optimize Imports**: Only import what you need
3. **Lazy Loading**: Import heavy libraries inside functions
4. **CDN**: Leverage Vercel's CDN for static assets

### When to Upgrade
Consider paid plans if you need:
- Longer execution times (>10s)
- More memory (>1GB)
- Higher bandwidth
- Team collaboration features

## Migration from Flask App

### What Changed
- ✅ Flask routes → Serverless functions
- ✅ Shared code in `/backend` folder
- ✅ Same business logic
- ✅ Same ML models
- ✅ Same frontend code

### What Stayed the Same
- API endpoints (`/api/stock-data`, etc.)
- Request/response format
- Frontend API calls
- Data processing logic

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ✅ Monitor performance
4. ⏳ Optimize cold starts (if needed)
5. ⏳ Add caching (if needed)
6. ⏳ Consider paid plan (if limits reached)

## Support

- **Vercel Docs**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **GitHub Issues**: Create issue in your repo
- **Vercel Support**: support@vercel.com (paid plans)
