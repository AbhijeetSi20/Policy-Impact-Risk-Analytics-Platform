import numpy as np
from datetime import datetime
from typing import List, Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

from app.models.schemas import Policy, RiskPrediction, RiskLevel, RiskFactor

class RiskPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.regions = ["North", "South", "East", "West", "Central"]
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load ML model for risk prediction"""
        # In production, this would load a trained model
        # For now, we'll use a simple rule-based approach with ML-like structure
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Train on mock data (in production, use real historical data)
        self._train_mock_model()
    
    def _train_mock_model(self):
        """Train model on mock data"""
        # Generate mock training data
        np.random.seed(42)
        n_samples = 1000
        X = np.random.rand(n_samples, 5)  # 5 features
        y = np.random.randint(0, 4, n_samples)  # 4 risk levels
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict(self, policy: Policy) -> RiskPrediction:
        """Predict risk for a policy"""
        
        # Extract features from policy
        features = self._extract_features(policy)
        features_scaled = self.scaler.transform([features])
        
        # Predict risk level
        risk_class = self.model.predict(features_scaled)[0]
        risk_proba = self.model.predict_proba(features_scaled)[0]
        
        # Map to risk levels
        risk_levels = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        overall_risk_level = risk_levels[risk_class]
        
        # Calculate risk score (0-100)
        risk_score = (risk_class + 1) * 25 + np.random.uniform(-5, 5)
        risk_score = max(0, min(100, risk_score))
        
        # Generate risk factors
        risk_factors = self._generate_risk_factors(policy, features)
        
        # Calculate confidence based on probability
        confidence = float(max(risk_proba))
        
        return RiskPrediction(
            policy_id=policy.id,
            overall_risk_level=overall_risk_level,
            risk_score=round(risk_score, 2),
            risk_factors=risk_factors,
            confidence=round(confidence, 3),
            predicted_at=datetime.now()
        )
    
    def get_regional_risks(self, policy: Policy) -> Dict[str, Dict]:
        """Analyze risk factors by region"""
        regional_risks = {}
        
        for region in self.regions:
            base_risk = np.random.uniform(20, 80)
            
            # Regional factors
            infrastructure_score = np.random.uniform(40, 95)
            stakeholder_sentiment = np.random.uniform(50, 95)
            
            risk_factors = []
            
            # Infrastructure risk
            if infrastructure_score < 60:
                risk_factors.append({
                    "factor": "Infrastructure Gap",
                    "score": round(100 - infrastructure_score, 1),
                    "severity": "High" if infrastructure_score < 45 else "Medium"
                })
            
            # Stakeholder risk
            if stakeholder_sentiment < 65:
                risk_factors.append({
                    "factor": "Low Stakeholder Engagement",
                    "score": round(100 - stakeholder_sentiment, 1),
                    "severity": "Medium"
                })
            
            regional_risks[region] = {
                "region": region,
                "overall_risk_score": round(base_risk, 2),
                "infrastructure_readiness": round(infrastructure_score, 2),
                "stakeholder_sentiment": round(stakeholder_sentiment, 2),
                "key_risk_factors": risk_factors,
                "risk_level": "High" if base_risk > 70 else "Medium" if base_risk > 40 else "Low"
            }
        
        return regional_risks
    
    def predict_failure_probability(self, policy: Policy) -> float:
        """Predict probability of policy failure (0-100)"""
        risk_prediction = self.predict(policy)
        
        # Map risk level to failure probability
        failure_map = {
            RiskLevel.LOW: np.random.uniform(5, 15),
            RiskLevel.MEDIUM: np.random.uniform(25, 45),
            RiskLevel.HIGH: np.random.uniform(55, 75),
            RiskLevel.CRITICAL: np.random.uniform(80, 95)
        }
        
        return round(failure_map.get(risk_prediction.overall_risk_level, 50), 2)
        
        # Calculate risk score (0-100)
        risk_score = (risk_class + 1) * 25 + np.random.uniform(-5, 5)
        risk_score = max(0, min(100, risk_score))
        
        # Generate risk factors
        risk_factors = self._generate_risk_factors(policy, features)
        
        # Calculate confidence based on probability
        confidence = float(max(risk_proba))
        
        return RiskPrediction(
            policy_id=policy.id,
            overall_risk_level=overall_risk_level,
            risk_score=round(risk_score, 2),
            risk_factors=risk_factors,
            confidence=round(confidence, 3),
            predicted_at=datetime.now()
        )
    
    def _extract_features(self, policy: Policy) -> List[float]:
        """Extract features from policy for ML model"""
        # Normalize budget (feature 1)
        budget_feature = min(1.0, policy.budget / 5000000)
        
        # Days since start (feature 2)
        days_running = (datetime.now() - policy.start_date).days
        days_feature = min(1.0, days_running / 365)
        
        # Number of target metrics (feature 3)
        metrics_count = len(policy.target_metrics)
        metrics_feature = min(1.0, metrics_count / 5)
        
        # Budget per metric (feature 4)
        budget_per_metric = policy.budget / max(1, metrics_count)
        budget_per_metric_feature = min(1.0, budget_per_metric / 1000000)
        
        # Status encoding (feature 5)
        status_map = {"draft": 0.2, "active": 0.5, "completed": 0.8, "archived": 0.1}
        status_feature = status_map.get(policy.status.value, 0.5)
        
        return [budget_feature, days_feature, metrics_feature, budget_per_metric_feature, status_feature]
    
    def _generate_risk_factors(self, policy: Policy, features: List[float]) -> List[RiskFactor]:
        """Generate detailed risk factors"""
        factors = []
        
        # Budget risk
        if policy.budget > 3000000:
            factors.append(RiskFactor(
                factor_name="High Budget Risk",
                risk_score=65.0,
                description="Large budget allocation increases financial exposure",
                mitigation_strategy="Implement phased budget releases with milestone reviews"
            ))
        
        # Timeline risk
        if policy.end_date:
            days_remaining = (policy.end_date - datetime.now()).days
            if days_remaining < 90:
                factors.append(RiskFactor(
                    factor_name="Timeline Pressure",
                    risk_score=70.0,
                    description="Limited time remaining may impact delivery quality",
                    mitigation_strategy="Prioritize critical deliverables and consider timeline extension"
                ))
        
        # Metrics complexity risk
        if len(policy.target_metrics) > 3:
            factors.append(RiskFactor(
                factor_name="Complex Metrics",
                risk_score=55.0,
                description="Multiple target metrics increase tracking complexity",
                mitigation_strategy="Focus on key performance indicators and simplify measurement"
            ))
        
        # Default risk factors
        if not factors:
            factors.append(RiskFactor(
                factor_name="Standard Operational Risk",
                risk_score=30.0,
                description="Standard risks associated with policy implementation",
                mitigation_strategy="Maintain regular monitoring and review cycles"
            ))
        
        return factors
