# 🚀 TeslaPulse — Tesla Stock Price Prediction

A full-stack web application for predicting Tesla (TSLA) stock prices using Machine Learning models. Built with **React + Vite** (frontend) and **Flask** (backend) with **scikit-learn** for ML.

![TeslaPulse](https://img.shields.io/badge/TeslaPulse-v1.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?style=flat-square&logo=flask)

---

## 📋 Features

### Machine Learning Pipeline
- **Data Collection**: Historical TSLA data via Yahoo Finance API
- **EDA**: Interactive visualizations — correlation heatmaps, moving averages, volume trends, return distributions
- **Feature Engineering**: MA(20/50/200), RSI-14, Bollinger Bands, MACD, Volatility
- **Feature Selection**: Correlation-based + Random Forest importance ranking
- **3 ML Models**: Linear Regression, Random Forest, Deep Neural Network (MLP)
- **K-Fold Validation**: TimeSeriesSplit (5-fold) preserving temporal order
- **Metrics**: RMSE, MAE, R², MAPE

### Frontend
- 🎨 Premium dark theme with glassmorphism effects
- 📊 Interactive Plotly charts (candlestick, line, bar, heatmap)
- 📈 Real-time TSLA price ticker
- 🔄 Model comparison dashboard
- 📅 Custom date range selection
- 📱 Fully responsive design

### Backend API
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stock-data` | GET | Historical TSLA data |
| `/api/eda` | GET | EDA statistics & charts |
| `/api/train` | POST | Train all ML models |
| `/api/predict` | POST | Run predictions |
| `/api/models/compare` | GET | Model comparison |
| `/api/realtime` | GET | Current TSLA price |
| `/api/predictions/history` | GET | Past predictions |

---

## 🛠️ Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- pip & npm

### 1. Clone & Install Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend

```bash
cd frontend
npm install
```

### 3. Run Backend

```bash
cd backend
python app.py
```
Backend runs at `http://localhost:5000`

### 4. Run Frontend

```bash
cd frontend
npm run dev
```
Frontend runs at `http://localhost:5173`

---

## 📁 Project Structure

```
ANN_CA2/
├── backend/
│   ├── app.py                    # Flask API
│   ├── config.py                 # Configuration
│   ├── requirements.txt          # Python deps
│   ├── models/                   # Saved trained models
│   ├── data/                     # Cached CSV data
│   ├── services/
│   │   ├── data_service.py       # Yahoo Finance data fetching
│   │   ├── eda_service.py        # EDA computations
│   │   ├── feature_engineering.py # Technical indicators
│   │   ├── model_service.py      # ML training & prediction
│   │   └── db_service.py         # SQLite storage
│   └── utils/
│       ├── metrics.py            # RMSE, MAE, R²
│       └── preprocessing.py      # Scaling, sequences
├── frontend/
│   ├── src/
│   │   ├── components/           # React UI components
│   │   ├── pages/                # Page components
│   │   ├── services/api.js       # Axios API client
│   │   ├── index.css             # Design system
│   │   ├── App.jsx               # Router
│   │   └── main.jsx              # Entry point
│   ├── index.html
│   └── package.json
└── README.md
```

---

## 🚀 Deployment

### Frontend → Vercel / Netlify
1. Push to GitHub
2. Connect repo to Vercel/Netlify
3. Build command: `npm run build`
4. Output directory: `dist`
5. Environment variable: `VITE_API_URL=https://your-backend.onrender.com`

### Backend → Render / Heroku
1. Push `backend/` to GitHub
2. Create Web Service on Render
3. Start command: `gunicorn app:app`
4. Add `requirements.txt` for auto-install
5. Configure CORS in `app.py` for your frontend URL

---

## 📊 Models Overview

| Model | Type | Description |
|-------|------|-------------|
| **Linear Regression** | Traditional ML | Simple linear relationship between features and price |
| **Random Forest** | Ensemble ML | 100 decision trees with max depth 15, captures non-linear patterns |
| **MLP (Deep Learning)** | Neural Network | 3-layer neural network (128→64→32) with sequential features |

---

## 📄 License

MIT License — Built for ANN CA2 Assignment
