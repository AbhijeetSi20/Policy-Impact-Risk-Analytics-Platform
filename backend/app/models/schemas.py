from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PolicyStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PolicyBase(BaseModel):
    name: str
    description: str
    category: str
    start_date: datetime
    end_date: Optional[datetime] = None
    budget: float
    target_metrics: Dict[str, float] = {}

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    status: PolicyStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MetricComparison(BaseModel):
    metric_name: str
    before_value: float
    after_value: float
    change_percentage: float
    change_absolute: float

class ImpactAnalysis(BaseModel):
    policy_id: int
    overall_impact_score: float = Field(..., ge=0, le=100)
    roi: float
    metrics_comparison: List[MetricComparison]
    key_insights: List[str]
    trend_data: Dict[str, List[float]]
    generated_at: datetime

class RiskFactor(BaseModel):
    factor_name: str
    risk_score: float = Field(..., ge=0, le=100)
    description: str
    mitigation_strategy: Optional[str] = None

class RiskPrediction(BaseModel):
    policy_id: int
    overall_risk_level: RiskLevel
    risk_score: float = Field(..., ge=0, le=100)
    risk_factors: List[RiskFactor]
    confidence: float = Field(..., ge=0, le=1)
    predicted_at: datetime

class Recommendation(BaseModel):
    title: str
    description: str
    priority: str  # "high", "medium", "low"
    category: str  # "budget", "timeline", "strategy", "risk_mitigation"
    expected_impact: str
    implementation_effort: str

class ExecutiveReport(BaseModel):
    policy_id: int
    policy_name: str
    executive_summary: str
    impact_analysis: ImpactAnalysis
    risk_assessment: RiskPrediction
    recommendations: List[Recommendation]
    key_metrics: Dict[str, Any]
    generated_at: datetime

class DashboardMetrics(BaseModel):
    total_policies: int
    active_policies: int
    total_budget: float
    average_roi: float
    high_risk_policies: int
    policies_by_status: Dict[str, int]
    policies_by_category: Dict[str, int]
    recent_activities: List[Dict[str, Any]]
