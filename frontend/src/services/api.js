import axios from 'axios'

// Change from local to your Render backend URL
const API_BASE_URL = "https://policy-impact-risk-analytics-platform-api.onrender.com"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})
export const getPolicies = () => api.get('/api/policies')
export const getPolicy = (id) => api.get(`/api/policies/${id}`)
export const createPolicy = (policy) => api.post('/api/policies', policy)
export const getImpactAnalysis = (id) => api.get(`/api/policies/${id}/impact`)
export const predictRisk = (id) => api.post(`/api/policies/${id}/predict-risk`)
export const getRecommendations = (id) => api.get(`/api/policies/${id}/recommendations`)
export const getExecutiveReport = (id) => api.get(`/api/policies/${id}/report`)
export const getDashboardMetrics = () => api.get('/api/dashboard/metrics')


export default api
