import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import random

from app.models.schemas import Policy, PolicyCreate, PolicyStatus, DashboardMetrics

class DataService:
    def __init__(self):
        self.policies: List[Policy] = []
        self.regions = ["North", "South", "East", "West", "Central"]
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize with mock policy data"""
        categories = ["Healthcare", "Education", "Infrastructure", "Environment", "Economic"]
        statuses = [PolicyStatus.ACTIVE, PolicyStatus.COMPLETED, PolicyStatus.DRAFT]
        
        for i in range(1, 21):
            start_date = datetime.now() - timedelta(days=random.randint(30, 365))
            end_date = start_date + timedelta(days=random.randint(90, 730)) if random.random() > 0.3 else None
            
            policy = Policy(
                id=i,
                name=f"Policy {i}: {random.choice(categories)} Initiative",
                description=f"Comprehensive {random.choice(categories).lower()} policy aimed at improving outcomes",
                category=random.choice(categories),
                start_date=start_date,
                end_date=end_date,
                budget=random.uniform(100000, 5000000),
                target_metrics={
                    "employment_rate": random.uniform(5, 15),
                    "satisfaction_score": random.uniform(60, 90),
                    "cost_efficiency": random.uniform(70, 95)
                },
                status=random.choice(statuses),
                created_at=start_date - timedelta(days=30),
                updated_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            self.policies.append(policy)
    
    def get_all_policies(self) -> List[Policy]:
        """Get all policies"""
        return self.policies
    
    def get_policy(self, policy_id: int) -> Optional[Policy]:
        """Get a specific policy by ID"""
        return next((p for p in self.policies if p.id == policy_id), None)
    
    def create_policy(self, policy_create: PolicyCreate) -> Policy:
        """Create a new policy"""
        new_id = max([p.id for p in self.policies], default=0) + 1
        policy = Policy(
            id=new_id,
            **policy_create.dict(),
            status=PolicyStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.policies.append(policy)
        return policy
    
    def get_policies_by_category(self, category: str) -> List[Policy]:
        """Get policies by category"""
        return [p for p in self.policies if p.category == category]
    
    def get_policies_by_status(self, status: str) -> List[Policy]:
        """Get policies by status"""
        return [p for p in self.policies if p.status.value == status]
    
    def get_active_policies(self) -> List[Policy]:
        """Get all active policies"""
        return [p for p in self.policies if p.status == PolicyStatus.ACTIVE]
    
    def filter_policies(
        self, 
        category: Optional[str] = None,
        status: Optional[str] = None,
        min_budget: Optional[float] = None,
        max_budget: Optional[float] = None,
        search_term: Optional[str] = None
    ) -> List[Policy]:
        """Advanced filtering of policies"""
        filtered = self.policies
        
        if category:
            filtered = [p for p in filtered if p.category == category]
        
        if status:
            filtered = [p for p in filtered if p.status.value == status]
        
        if min_budget is not None:
            filtered = [p for p in filtered if p.budget >= min_budget]
        
        if max_budget is not None:
            filtered = [p for p in filtered if p.budget <= max_budget]
        
        if search_term:
            search_lower = search_term.lower()
            filtered = [p for p in filtered if search_lower in p.name.lower() or search_lower in p.description.lower()]
        
        return filtered
    
    def get_regional_performance_data(self, policy_id: int) -> Dict[str, Any]:
        """Generate regional performance data for a policy"""
        regional_data = {}
        
        for region in self.regions:
            regional_data[region] = {
                "region": region,
                "beneficiaries": random.randint(1000, 50000),
                "impact_score": round(random.uniform(30, 95), 2),
                "roi": round(random.uniform(50, 250), 2),
                "success_rate": round(random.uniform(65, 99), 2),
                "cost_per_beneficiary": round(random.uniform(100, 2000), 2),
                "satisfaction_score": round(random.uniform(60, 95), 2),
                "deployment_status": random.choice(["On Track", "At Risk", "Delayed"])
            }
        
        return regional_data
    
    def get_regional_comparison(self, policy_id: int) -> Dict[str, Any]:
        """Get comparative analysis across regions"""
        regional_data = self.get_regional_performance_data(policy_id)
        
        # Calculate aggregates
        impact_scores = [v["impact_score"] for v in regional_data.values()]
        rois = [v["roi"] for v in regional_data.values()]
        
        return {
            "policy_id": policy_id,
            "regional_breakdown": regional_data,
            "best_performing_region": max(regional_data.items(), key=lambda x: x[1]["impact_score"])[0],
            "needs_improvement": min(regional_data.items(), key=lambda x: x[1]["impact_score"])[0],
            "average_impact": round(np.mean(impact_scores), 2),
            "average_roi": round(np.mean(rois), 2),
            "regional_variance": round(np.std(impact_scores), 2)
        }
    
    def get_dashboard_metrics(self, policies: List[Policy]) -> DashboardMetrics:
        """Calculate dashboard metrics"""
        total_policies = len(policies)
        active_policies = len([p for p in policies if p.status == PolicyStatus.ACTIVE])
        total_budget = sum(p.budget for p in policies)
        
        # Mock average ROI calculation
        average_roi = np.random.uniform(120, 250)
        
        # Mock high risk count (would come from risk predictor in real scenario)
        high_risk_policies = random.randint(2, 5)
        
        policies_by_status = {}
        for status in PolicyStatus:
            policies_by_status[status.value] = len([p for p in policies if p.status == status])
        
        policies_by_category = {}
        for policy in policies:
            policies_by_category[policy.category] = policies_by_category.get(policy.category, 0) + 1
        
        recent_activities = [
            {
                "policy_id": p.id,
                "policy_name": p.name,
                "action": "Updated",
                "timestamp": p.updated_at.isoformat()
            }
            for p in sorted(policies, key=lambda x: x.updated_at, reverse=True)[:5]
        ]
        
        return DashboardMetrics(
            total_policies=total_policies,
            active_policies=active_policies,
            total_budget=total_budget,
            average_roi=average_roi,
            high_risk_policies=high_risk_policies,
            policies_by_status=policies_by_status,
            policies_by_category=policies_by_category,
            recent_activities=recent_activities
        )
    
    def refresh_data(self):
        """Refresh data from external sources (mock implementation)"""
        # In production, this would fetch from databases, APIs, etc.
        pass
