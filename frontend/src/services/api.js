/**
 * TeslaPulse — API Client
 * Axios-based service for all backend communication.
 */

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2min for training
  headers: { 'Content-Type': 'application/json' },
});

// ---- Stock Data ----
export async function fetchStockData(start, end) {
  const params = {};
  if (start) params.start = start;
  if (end) params.end = end;
  const { data } = await api.get('/api/stock-data', { params });
  return data;
}

// ---- EDA ----
export async function fetchEDA(start, end) {
  const params = {};
  if (start) params.start = start;
  if (end) params.end = end;
  const { data } = await api.get('/api/eda', { params });
  return data;
}

// ---- Train Models ----
export async function trainModels(start, end) {
  const { data } = await api.post('/api/train', { start, end });
  return data;
}

// ---- Predict ----
export async function getPredictions(model, start, end) {
  const { data } = await api.post('/api/predict', { model, start, end });
  return data;
}

// ---- Model Comparison ----
export async function getModelComparison() {
  const { data } = await api.get('/api/models/compare');
  return data;
}

// ---- Real-time Price ----
export async function getRealtimePrice() {
  const { data } = await api.get('/api/realtime');
  return data;
}

// ---- Prediction History ----
export async function getPredictionHistory(limit = 50) {
  const { data } = await api.get('/api/predictions/history', { params: { limit } });
  return data;
}

export default api;
