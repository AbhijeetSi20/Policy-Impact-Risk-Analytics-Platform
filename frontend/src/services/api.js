import axios from 'axios'
from fastapi.middleware.cors import CORSMiddleware

// Change from local to your Render backend URL
const API_BASE_URL = "https://policy-impact-risk-analytics-platform-api.onrender.com"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://policy-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

export const getPolicies = () => api.get('/policies')
export const getPolicy = (id) => api.get(`/policies/${id}`)
export const createPolicy = (policy) => api.post('/policies', policy)
export const getImpactAnalysis = (id) => api.get(`/policies/${id}/impact`)
export const predictRisk = (id) => api.post(`/policies/${id}/predict-risk`)
export const getRecommendations = (id) => api.get(`/policies/${id}/recommendations`)
export const getExecutiveReport = (id) => api.get(`/policies/${id}/report`)
export const getDashboardMetrics = () => api.get('/dashboard/metrics')

export default api
