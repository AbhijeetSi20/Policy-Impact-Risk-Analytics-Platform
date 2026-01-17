from datetime import datetime
from typing import Dict, Any, List

from app.models.schemas import (
    Policy, ImpactAnalysis, RiskPrediction, 
    Recommendation, ExecutiveReport
)

class ReportGenerator:
    def __init__(self):
        pass
    
    def generate(
        self, 
        policy: Policy, 
        impact: ImpactAnalysis, 
        risk: RiskPrediction,
        recommendations: List[Recommendation]
    ) -> ExecutiveReport:
        """Generate executive report"""
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(policy, impact, risk, recommendations)
        
        # Compile key metrics
        key_metrics = {
            "budget_utilization": round((policy.budget / 5000000) * 100, 2) if policy.budget < 5000000 else 100,
            "impact_score": impact.overall_impact_score,
            "roi": impact.roi,
            "risk_score": risk.risk_score,
            "risk_level": risk.overall_risk_level.value,
            "recommendations_count": len(recommendations),
            "high_priority_recommendations": len([r for r in recommendations if r.priority == "high"]),
            "metrics_tracked": len(impact.metrics_comparison),
            "average_metric_improvement": round(
                sum([abs(mc.change_percentage) for mc in impact.metrics_comparison]) / len(impact.metrics_comparison),
                2
            ) if impact.metrics_comparison else 0
        }
        
        return ExecutiveReport(
            policy_id=policy.id,
            policy_name=policy.name,
            executive_summary=executive_summary,
            impact_analysis=impact,
            risk_assessment=risk,
            recommendations=recommendations,
            key_metrics=key_metrics,
            generated_at=datetime.now()
        )
    
    def _generate_executive_summary(
        self, 
        policy: Policy, 
        impact: ImpactAnalysis, 
        risk: RiskPrediction,
        recommendations: List[Recommendation]
    ) -> str:
        """Generate executive summary text"""
        
        summary_parts = []
        
        # Policy overview
        summary_parts.append(
            f"The {policy.name} ({policy.category}) has been analyzed for impact, risk, and strategic recommendations."
        )
        
        # Impact summary
        if impact.overall_impact_score >= 70:
            impact_desc = "demonstrates strong positive impact"
        elif impact.overall_impact_score >= 40:
            impact_desc = "shows moderate impact"
        else:
            impact_desc = "requires attention to improve impact"
        
        summary_parts.append(
            f"Impact analysis indicates the policy {impact_desc} with an overall impact score of {impact.overall_impact_score:.1f}/100 "
            f"and an ROI of {impact.roi:.1f}%."
        )
        
        # Risk summary
        risk_desc = {
            "low": "presents minimal risk",
            "medium": "has moderate risk factors",
            "high": "carries significant risk",
            "critical": "requires immediate risk mitigation"
        }.get(risk.overall_risk_level.value, "has risk factors")
        
        summary_parts.append(
            f"Risk assessment shows the policy {risk_desc} with a risk score of {risk.risk_score:.1f}/100 "
            f"({risk.overall_risk_level.value.upper()} risk level)."
        )
        
        # Recommendations summary
        high_priority = [r for r in recommendations if r.priority == "high"]
        if high_priority:
            summary_parts.append(
                f"{len(high_priority)} high-priority recommendation(s) have been identified to optimize policy performance and mitigate risks."
            )
        
        # Overall assessment
        if impact.overall_impact_score >= 70 and risk.overall_risk_level.value in ["low", "medium"]:
            summary_parts.append(
                "Overall assessment: Policy is performing well with strong impact and manageable risk profile."
            )
        elif impact.overall_impact_score < 40 or risk.overall_risk_level.value == "critical":
            summary_parts.append(
                "Overall assessment: Policy requires immediate attention to improve impact and address critical risks."
            )
        else:
            summary_parts.append(
                "Overall assessment: Policy shows promise but would benefit from implementing recommended improvements."
            )
        
        return " ".join(summary_parts)
