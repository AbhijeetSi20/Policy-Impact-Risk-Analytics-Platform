import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict

from app.models.schemas import Policy, ImpactAnalysis, MetricComparison

class ImpactAnalyzer:
    def __init__(self):
        self.regions = ["North", "South", "East", "West", "Central"]
    
    def analyze(self, policy: Policy) -> ImpactAnalysis:
        """Analyze policy impact (before vs after)"""
        
        # Generate mock before/after data
        metrics_comparison = []
        trend_data = {}
        
        for metric_name, target_value in policy.target_metrics.items():
            # Simulate before value (lower than target)
            before_value = target_value * np.random.uniform(0.6, 0.85)
            # Simulate after value (closer to or exceeding target)
            after_value = target_value * np.random.uniform(0.9, 1.15)
            
            change_absolute = after_value - before_value
            change_percentage = (change_absolute / before_value) * 100 if before_value > 0 else 0
            
            metrics_comparison.append(MetricComparison(
                metric_name=metric_name,
                before_value=round(before_value, 2),
                after_value=round(after_value, 2),
                change_percentage=round(change_percentage, 2),
                change_absolute=round(change_absolute, 2)
            ))
            
            # Generate trend data (12 months)
            trend_data[metric_name] = [
                round(before_value + (after_value - before_value) * (i / 11) + np.random.uniform(-2, 2), 2)
                for i in range(12)
            ]
        
        # Calculate overall impact score (weighted average of improvements)
        impact_scores = [abs(mc.change_percentage) for mc in metrics_comparison]
        overall_impact_score = min(100, np.mean(impact_scores) * 0.8)
        
        # Calculate ROI
        total_improvement = sum([mc.change_absolute for mc in metrics_comparison])
        roi = (total_improvement / policy.budget) * 100 if policy.budget > 0 else 0
        
        # Generate key insights
        key_insights = self._generate_insights(metrics_comparison, overall_impact_score, roi)
        
        return ImpactAnalysis(
            policy_id=policy.id,
            overall_impact_score=round(overall_impact_score, 2),
            roi=round(roi, 2),
            metrics_comparison=metrics_comparison,
            key_insights=key_insights,
            trend_data=trend_data,
            generated_at=datetime.now()
        )
    
    def get_regional_impact(self, policy: Policy) -> Dict[str, Dict]:
        """Analyze impact breakdown by region"""
        regional_impact = {}
        
        for region in self.regions:
            # Generate region-specific metrics
            metrics_comparison = []
            
            for metric_name, target_value in policy.target_metrics.items():
                # Regional performance varies
                before_value = target_value * np.random.uniform(0.5, 0.8)
                after_value = target_value * np.random.uniform(0.85, 1.1)
                
                change_percentage = ((after_value - before_value) / before_value) * 100 if before_value > 0 else 0
                
                metrics_comparison.append({
                    "metric_name": metric_name,
                    "before_value": round(before_value, 2),
                    "after_value": round(after_value, 2),
                    "change_percentage": round(change_percentage, 2)
                })
            
            # Calculate regional scores
            impact_scores = [abs(m["change_percentage"]) for m in metrics_comparison]
            regional_impact_score = round(min(100, np.mean(impact_scores) * 0.8), 2)
            
            regional_impact[region] = {
                "region": region,
                "impact_score": regional_impact_score,
                "beneficiaries": round(np.random.uniform(5000, 50000), 0),
                "metrics": metrics_comparison,
                "deployment_status": np.random.choice(["On Track", "At Risk", "Delayed"])
            }
        
        return regional_impact
    
    def calculate_cost_per_beneficiary(self, policy: Policy, beneficiaries: int = None) -> float:
        """Calculate cost per beneficiary"""
        if beneficiaries is None:
            beneficiaries = round(np.random.uniform(10000, 100000))
        
        return round(policy.budget / beneficiaries, 2) if beneficiaries > 0 else 0
    
    def get_efficiency_score(self, policy: Policy, impact_score: float, roi: float) -> float:
        """Calculate efficiency score based on impact and ROI"""
        efficiency = (impact_score * 0.6 + min(100, roi / 2) * 0.4)
        return round(min(100, efficiency), 2)
    
    def _generate_insights(self, metrics: List[MetricComparison], impact_score: float, roi: float) -> List[str]:
        """Generate key insights from analysis"""
        insights = []
        
        if impact_score > 70:
            insights.append("Policy demonstrates strong positive impact across key metrics")
        elif impact_score > 40:
            insights.append("Policy shows moderate impact with room for optimization")
        else:
            insights.append("Policy impact is below expectations; review strategy recommended")
        
        best_metric = max(metrics, key=lambda m: abs(m.change_percentage))
        insights.append(f"Strongest improvement in {best_metric.metric_name} ({best_metric.change_percentage:.1f}% change)")
        
        if roi > 200:
            insights.append("Exceptional ROI indicates high policy effectiveness")
        elif roi > 100:
            insights.append("Positive ROI demonstrates policy value")
        else:
            insights.append("ROI below target; consider cost optimization strategies")
        
        return insights
