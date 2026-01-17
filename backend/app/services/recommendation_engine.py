from typing import List
from datetime import datetime

from app.models.schemas import Policy, Recommendation, RiskLevel

class RecommendationEngine:
    def __init__(self):
        pass
    
    def generate(self, policy: Policy) -> List[Recommendation]:
        """Generate recommendations for a policy"""
        recommendations = []
        
        # Budget recommendations
        if policy.budget > 2000000:
            recommendations.append(Recommendation(
                title="Optimize Budget Allocation",
                description=f"Current budget of ${policy.budget:,.0f} is substantial. Consider phased allocation with performance-based releases.",
                priority="high",
                category="budget",
                expected_impact="Reduce financial risk by 25% while maintaining policy effectiveness",
                implementation_effort="medium"
            ))
        elif policy.budget < 500000:
            recommendations.append(Recommendation(
                title="Increase Budget for Better Outcomes",
                description="Current budget may limit policy impact. Consider additional funding for key initiatives.",
                priority="medium",
                category="budget",
                expected_impact="Potential 30-40% improvement in policy outcomes",
                implementation_effort="high"
            ))
        
        # Timeline recommendations
        if policy.end_date:
            days_remaining = (policy.end_date - datetime.now()).days
            if days_remaining < 60:
                recommendations.append(Recommendation(
                    title="Extend Timeline or Prioritize Deliverables",
                    description=f"Only {days_remaining} days remaining. Consider timeline extension or focus on critical outcomes.",
                    priority="high",
                    category="timeline",
                    expected_impact="Ensure quality delivery and avoid rushed implementation",
                    implementation_effort="low"
                ))
        
        # Metrics recommendations
        if len(policy.target_metrics) == 0:
            recommendations.append(Recommendation(
                title="Define Clear Success Metrics",
                description="No target metrics defined. Establish measurable KPIs to track policy effectiveness.",
                priority="high",
                category="strategy",
                expected_impact="Enable data-driven decision making and impact measurement",
                implementation_effort="medium"
            ))
        elif len(policy.target_metrics) > 4:
            recommendations.append(Recommendation(
                title="Focus on Key Metrics",
                description=f"Too many metrics ({len(policy.target_metrics)}) may dilute focus. Prioritize 2-3 critical KPIs.",
                priority="medium",
                category="strategy",
                expected_impact="Improve clarity and focus on most important outcomes",
                implementation_effort="low"
            ))
        
        # Category-specific recommendations
        if policy.category == "Healthcare":
            recommendations.append(Recommendation(
                title="Engage Healthcare Stakeholders",
                description="Ensure active participation from healthcare providers and patient advocacy groups.",
                priority="high",
                category="strategy",
                expected_impact="Improve policy adoption and effectiveness by 20-30%",
                implementation_effort="medium"
            ))
        elif policy.category == "Education":
            recommendations.append(Recommendation(
                title="Leverage Educational Technology",
                description="Consider integrating EdTech solutions to enhance policy delivery and measurement.",
                priority="medium",
                category="strategy",
                expected_impact="Increase reach and engagement by 35%",
                implementation_effort="high"
            ))
        elif policy.category == "Infrastructure":
            recommendations.append(Recommendation(
                title="Conduct Infrastructure Assessment",
                description="Perform comprehensive infrastructure audit before full implementation.",
                priority="high",
                category="risk_mitigation",
                expected_impact="Identify and mitigate potential infrastructure bottlenecks early",
                implementation_effort="medium"
            ))
        
        # Status-based recommendations
        if policy.status.value == "draft":
            recommendations.append(Recommendation(
                title="Finalize Policy Design",
                description="Complete policy design and stakeholder alignment before activation.",
                priority="high",
                category="strategy",
                expected_impact="Ensure smooth launch and reduce implementation risks",
                implementation_effort="medium"
            ))
        
        # Default recommendation if none generated
        if not recommendations:
            recommendations.append(Recommendation(
                title="Maintain Current Strategy",
                description="Policy appears well-structured. Continue with current approach and monitor progress.",
                priority="low",
                category="strategy",
                expected_impact="Sustain current positive trajectory",
                implementation_effort="low"
            ))
        
        return recommendations
    
    def generate_regional_recommendations(self, policy: Policy, regional_impacts: dict) -> dict:
        """Generate region-specific recommendations"""
        regional_recs = {}
        
        for region, impact_data in regional_impacts.items():
            recs = []
            
            impact_score = impact_data.get("impact_score", 50)
            
            # Low impact recommendations
            if impact_score < 40:
                recs.append({
                    "title": f"Improve {region} Region Performance",
                    "description": f"Impact score of {impact_score}% is below target. Review execution strategy and resource allocation.",
                    "priority": "high",
                    "expected_impact": "20-30% improvement in regional outcomes"
                })
            
            # Deployment issues
            if impact_data.get("deployment_status") == "At Risk":
                recs.append({
                    "title": f"Address {region} Region Risks",
                    "description": "This region is showing deployment risks. Increase monitoring and support.",
                    "priority": "high",
                    "expected_impact": "Reduce implementation delays by 40%"
                })
            
            regional_recs[region] = recs
        
        return regional_recs
    
    def generate_budget_optimization_recommendations(self, policy: Policy, regional_data: dict) -> List[Recommendation]:
        """Generate budget optimization recommendations based on regional performance"""
        recs = []
        
        # Identify underperforming regions and reallocate budget
        regional_impacts = {k: v.get("impact_score", 50) for k, v in regional_data.items() if isinstance(v, dict)}
        
        if regional_impacts:
            best_region = max(regional_impacts, key=regional_impacts.get)
            worst_region = min(regional_impacts, key=regional_impacts.get)
            
            if regional_impacts[best_region] > regional_impacts[worst_region] + 20:
                recs.append(Recommendation(
                    title=f"Reallocate Budget from {best_region} to {worst_region}",
                    description=f"{best_region} shows {regional_impacts[best_region]:.0f}% impact while {worst_region} shows only {regional_impacts[worst_region]:.0f}%. Consider budget shift.",
                    priority="high",
                    category="budget",
                    expected_impact="Optimize resource allocation and improve overall policy effectiveness",
                    implementation_effort="medium"
                ))
        
        return recs
