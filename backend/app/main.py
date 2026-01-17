from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn

from app.models.schemas import (
    Policy, PolicyCreate, ImpactAnalysis, RiskPrediction, 
    Recommendation, ExecutiveReport, DashboardMetrics
)
from app.services.data_service import DataService
from app.services.impact_analyzer import ImpactAnalyzer
from app.services.risk_predictor import RiskPredictor
from app.services.recommendation_engine import RecommendationEngine
from app.services.report_generator import ReportGenerator

app = FastAPI(
    title="Policy Impact & Risk Analytics API",
    description="Platform for analyzing policy impact, predicting risks, and generating insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://policy-frontend.fly.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_service = DataService()
impact_analyzer = ImpactAnalyzer()
risk_predictor = RiskPredictor()
recommendation_engine = RecommendationEngine()
report_generator = ReportGenerator()

@app.get("/")
async def root():
    return {"message": "Policy Impact & Risk Analytics Platform API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/policies", response_model=List[Policy])
async def get_policies():
    """Get all policies"""
    return data_service.get_all_policies()

@app.get("/api/policies/{policy_id}", response_model=Policy)
async def get_policy(policy_id: int):
    """Get a specific policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@app.post("/api/policies", response_model=Policy)
async def create_policy(policy: PolicyCreate):
    """Create a new policy"""
    return data_service.create_policy(policy)

@app.get("/api/policies/{policy_id}/impact", response_model=ImpactAnalysis)
async def get_impact_analysis(policy_id: int):
    """Get impact analysis for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    analysis = impact_analyzer.analyze(policy)
    return analysis

@app.post("/api/policies/{policy_id}/predict-risk", response_model=RiskPrediction)
async def predict_risk(policy_id: int):
    """Predict risk for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    prediction = risk_predictor.predict(policy)
    return prediction

@app.get("/api/policies/{policy_id}/recommendations", response_model=List[Recommendation])
async def get_recommendations(policy_id: int):
    """Get recommendations for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    recommendations = recommendation_engine.generate(policy)
    return recommendations

@app.get("/api/policies/{policy_id}/report", response_model=ExecutiveReport)
async def get_executive_report(policy_id: int):
    """Generate executive report for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    impact = impact_analyzer.analyze(policy)
    risk = risk_predictor.predict(policy)
    recommendations = recommendation_engine.generate(policy)
    
    report = report_generator.generate(policy, impact, risk, recommendations)
    return report

@app.get("/api/policies/{policy_id}/regional-impact")
async def get_regional_impact(policy_id: int):
    """Get regional impact breakdown for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return impact_analyzer.get_regional_impact(policy)

@app.get("/api/policies/{policy_id}/regional-risks")
async def get_regional_risks(policy_id: int):
    """Get regional risk analysis for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return risk_predictor.get_regional_risks(policy)

@app.get("/api/policies/{policy_id}/regional-comparison")
async def get_regional_comparison(policy_id: int):
    """Get comparative analysis across regions"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return data_service.get_regional_comparison(policy_id)

@app.get("/api/policies/{policy_id}/regional-recommendations")
async def get_regional_recommendations(policy_id: int):
    """Get region-specific recommendations"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    regional_impact = impact_analyzer.get_regional_impact(policy)
    return recommendation_engine.generate_regional_recommendations(policy, regional_impact)

@app.get("/api/policies/{policy_id}/failure-probability")
async def get_failure_probability(policy_id: int):
    """Get predicted failure probability for a policy"""
    policy = data_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    failure_prob = risk_predictor.predict_failure_probability(policy)
    return {
        "policy_id": policy_id,
        "failure_probability": failure_prob,
        "success_probability": round(100 - failure_prob, 2),
        "risk_assessment": "High Risk" if failure_prob > 60 else "Medium Risk" if failure_prob > 30 else "Low Risk"
    }

@app.post("/api/policies/filter")
async def filter_policies(
    category: Optional[str] = None,
    status: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None,
    search_term: Optional[str] = None
):
    """Filter policies with advanced criteria"""
    return data_service.filter_policies(category, status, min_budget, max_budget, search_term)

@app.get("/api/policies/by-category/{category}", response_model=List[Policy])
async def get_policies_by_category(category: str):
    """Get all policies in a specific category"""
    return data_service.get_policies_by_category(category)

@app.get("/api/policies/by-status/{status}", response_model=List[Policy])
async def get_policies_by_status(status: str):
    """Get all policies with a specific status"""
    return data_service.get_policies_by_status(status)

@app.get("/api/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics():
    """Get dashboard metrics"""
    policies = data_service.get_all_policies()
    return data_service.get_dashboard_metrics(policies)

@app.get("/api/dashboard/executive-overview")
async def get_executive_overview():
    """Get executive-level overview of all policies"""
    policies = data_service.get_all_policies()
    
    # Calculate aggregate metrics
    total_budget = sum(p.budget for p in policies)
    active_count = len([p for p in policies if p.status.value == "active"])
    draft_count = len([p for p in policies if p.status.value == "draft"])
    completed_count = len([p for p in policies if p.status.value == "completed"])
    
    # Calculate average metrics across all policies
    avg_impact_scores = []
    avg_rois = []
    avg_risk_scores = []
    
    for policy in policies[:5]:  # Sample first 5 for performance
        impact = impact_analyzer.analyze(policy)
        risk = risk_predictor.predict(policy)
        avg_impact_scores.append(impact.overall_impact_score)
        avg_rois.append(impact.roi)
        avg_risk_scores.append(risk.risk_score)
    
    return {
        "total_policies": len(policies),
        "total_budget": round(total_budget, 2),
        "active_policies": active_count,
        "draft_policies": draft_count,
        "completed_policies": completed_count,
        "average_impact_score": round(sum(avg_impact_scores) / len(avg_impact_scores), 2) if avg_impact_scores else 0,
        "average_roi": round(sum(avg_rois) / len(avg_rois), 2) if avg_rois else 0,
        "average_risk_score": round(sum(avg_risk_scores) / len(avg_risk_scores), 2) if avg_risk_scores else 0,
        "policies_by_category": {}  # Will be populated by get_dashboard_metrics
    }

@app.get("/api/data/refresh")
async def refresh_data():
    """Refresh data from sources"""
    data_service.refresh_data()
    return {"message": "Data refreshed successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
