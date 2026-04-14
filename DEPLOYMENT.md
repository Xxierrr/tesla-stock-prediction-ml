# TeslaPulse Deployment Guide

## Architecture
- **Frontend**: React (Vite) deployed on Vercel
- **Backend**: Flask API deployed on Render

## Backend Deployment (Render)

### Step 1: Push your code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `Xxierrr/tesla-stock-prediction-ml`
4. Configure:
   - **Name**: `teslapulse-api`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes)
7. Copy your Render URL (e.g., `https://teslapulse-api.onrender.com`)

### Step 3: Test Backend
Visit: `https://your-app.onrender.com/api/health`

Should return: `{"status": "ok", "service": "TeslaPulse API"}`

## Frontend Deployment (Vercel)

### Step 1: Update Environment Variable
1. Go to your Vercel project: `tesla-stock-prediction-ml-487y`
2. Go to Settings → Environment Variables
3. Add/Update:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-render-app.onrender.com` (your Render URL)
4. Click "Save"

### Step 2: Redeploy Frontend
1. Go to Deployments tab
2. Click "Redeploy" on the latest deployment
3. Wait for deployment to complete

### Step 3: Update Backend CORS (if needed)
If your Vercel frontend URL changes, update `backend/app.py`:
```python
ALLOWED_ORIGINS = [
    "https://your-new-vercel-url.vercel.app",
    "http://localhost:5173"
]
```

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
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

## Troubleshooting

### CORS Errors
- Ensure your Vercel frontend URL is in `ALLOWED_ORIGINS` in `backend/app.py`
- Redeploy backend after updating CORS settings

### 404 Errors on API
- Check `VITE_API_URL` is set correctly in Vercel
- Verify Render backend is running
- Check Render logs for errors

### Render Free Tier Limitations
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for one app)

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=https://your-render-app.onrender.com
```

### Backend (Render Dashboard)
No additional env vars needed for basic setup.

## Monitoring

### Render
- View logs: Render Dashboard → Your Service → Logs
- Check status: Render Dashboard → Your Service

### Vercel
- View logs: Vercel Dashboard → Your Project → Deployments → Click deployment
- Check build logs and runtime logs

## Cost
- **Render Free Tier**: $0/month (with limitations)
- **Vercel Hobby**: $0/month
- **Total**: $0/month

## Upgrading (Optional)

### Render Paid Plans
- **Starter**: $7/month - No spin-down, better performance
- **Standard**: $25/month - More resources

### Keep Free Tier Active
Use a service like [UptimeRobot](https://uptimerobot.com) to ping your API every 5 minutes to prevent spin-down.
