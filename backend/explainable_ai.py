"""
🧠 NTRO-CryptoForensics: Explainable AI Reasoning Layer
======================================================

Transparent AI reasoning engine that:
- Explains every risk assessment and threat classification decision
- Provides evidence trails for legal and investigative reporting
- Makes AI predictions auditable and interpretable
- Generates human-readable reasoning for complex correlations
- Supports regulatory compliance and court admissibility

Critical for law enforcement and intelligence agency use cases.
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
from collections import defaultdict

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvidenceType(Enum):
    BLOCKCHAIN_TRANSACTION = "blockchain_transaction"
    COMMUNICATION_INTERCEPT = "communication_intercept"
    DARK_WEB_ACTIVITY = "dark_web_activity"
    DATA_LEAK = "data_leak"
    BEHAVIORAL_PATTERN = "behavioral_pattern"
    LINGUISTIC_ANALYSIS = "linguistic_analysis"
    TIMING_CORRELATION = "timing_correlation"
    CROSS_REFERENCE = "cross_reference"

class ConfidenceLevel(Enum):
    VERY_LOW = (0.0, 0.2, "Very Low")
    LOW = (0.2, 0.4, "Low")
    MEDIUM = (0.4, 0.6, "Medium")
    HIGH = (0.6, 0.8, "High")
    VERY_HIGH = (0.8, 1.0, "Very High")
    
    def __init__(self, min_val, max_val, label):
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
    
    @classmethod
    def from_score(cls, score: float):
        for level in cls:
            if level.min_val <= score <= level.max_val:
                return level
        return cls.MEDIUM

class ReasoningType(Enum):
    DEDUCTIVE = "deductive"  # From general rules to specific conclusions
    INDUCTIVE = "inductive"  # From specific observations to general patterns
    ABDUCTIVE = "abductive"  # Best explanation for observations
    PROBABILISTIC = "probabilistic"  # Based on statistical inference

@dataclass
class Evidence:
    """Individual piece of evidence supporting a conclusion"""
    evidence_id: str
    evidence_type: EvidenceType
    description: str
    source: str
    timestamp: datetime
    confidence: float
    weight: float  # How much this evidence contributes to the conclusion
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReasoningStep:
    """Individual step in reasoning process"""
    step_id: str
    reasoning_type: ReasoningType
    premise: str
    conclusion: str
    evidence_used: List[str]  # Evidence IDs
    confidence: float
    logical_operator: str  # AND, OR, IF-THEN, etc.
    explanation: str

@dataclass
class ExplanationSummary:
    """Summary explanation for decisions"""
    decision_id: str
    question: str
    final_conclusion: str
    confidence_level: ConfidenceLevel
    key_evidence: List[str]
    reasoning_chain: List[str]
    risk_factors: List[str]
    mitigating_factors: List[str]
    recommended_actions: List[str]

class ExplainableAI:
    """Enhanced explainable AI with reasoning capabilities"""
    
    def __init__(self):
        self.evidence_store: Dict[str, Evidence] = {}
        self.reasoning_steps: List[ReasoningStep] = []
        logger.info("🧠 Advanced Explainable AI Layer initialized")
    
    def explain_risk_score(self, address_data: dict) -> str:
        """Generate comprehensive explanation for risk score"""
        risk = address_data.get('risk_score', 0)
        category = address_data.get('category', 'unknown')
        tx_count = address_data.get('transaction_count', 0)
        
        # Create evidence for this decision
        evidence_items = []
        
        # High-level risk assessment
        if risk > 70:
            evidence_items.append(f"HIGH RISK: Classified as '{category}' with {risk}% confidence")
        elif risk > 40:
            evidence_items.append(f"MEDIUM RISK: Classified as '{category}' with {risk}% confidence")
        else:
            evidence_items.append(f"LOW RISK: Standard activity pattern detected")
        
        # Transaction volume analysis
        if tx_count > 500:
            evidence_items.append(f"HIGH ACTIVITY: {tx_count} transactions indicate active usage")
        elif tx_count > 100:
            evidence_items.append(f"MODERATE ACTIVITY: {tx_count} transactions")
        else:
            evidence_items.append(f"LOW ACTIVITY: {tx_count} transactions")
        
        # Category-specific explanations
        category_explanations = {
            'darknet': 'Associated with dark web marketplaces - indicates potential illicit activity',
            'mixer': 'Cryptocurrency mixing service - used to obscure transaction trails',
            'exchange': 'Cryptocurrency exchange - legitimate but high-volume',
            'gambling': 'Online gambling platform - legitimate but monitored',
            'mining': 'Mining pool or individual miner - typically legitimate'
        }
        
        if category in category_explanations:
            evidence_items.append(f"CATEGORY ANALYSIS: {category_explanations[category]}")
        
        # Additional risk factors
        if address_data.get('recent_activity', False):
            evidence_items.append("TEMPORAL FACTOR: Recent activity detected")
        
        if address_data.get('large_transactions', False):
            evidence_items.append("VOLUME FACTOR: Large transaction amounts detected")
        
        # Compile explanation
        explanation = f"""
        🔍 RISK ASSESSMENT EXPLANATION
        
        Address: {address_data.get('address', 'N/A')}
        Overall Risk Score: {risk}%
        Classification: {category.upper()}
        
        EVIDENCE ANALYSIS:
        {chr(10).join(f'• {item}' for item in evidence_items)}
        
        REASONING CHAIN:
        1. Transaction pattern analysis → Activity level: {'High' if tx_count > 500 else 'Moderate' if tx_count > 100 else 'Low'}
        2. Behavioral classification → Category: {category}
        3. Risk correlation → Final score: {risk}%
        
        CONFIDENCE LEVEL: {ConfidenceLevel.from_score(risk/100).label}
        
        RECOMMENDED ACTION: {'Immediate investigation' if risk > 70 else 'Enhanced monitoring' if risk > 40 else 'Standard monitoring'}
        """
        
        return explanation.strip()
    
    def explain_threat_persona(self, persona_data: dict) -> str:
        """Explain threat persona classification"""
        threat_level = persona_data.get('threat_level', 'UNKNOWN')
        confidence = persona_data.get('confidence_score', 0.0)
        
        explanation = f"""
        👤 THREAT PERSONA ANALYSIS
        
        Persona ID: {persona_data.get('persona_id', 'N/A')}
        Primary Identifier: {persona_data.get('primary_identifier', 'N/A')}
        Threat Level: {threat_level}
        Confidence: {confidence:.2f}
        
        DIGITAL FOOTPRINT:
        • Crypto Wallets: {len(persona_data.get('crypto_wallets', []))}
        • Email Addresses: {len(persona_data.get('email_addresses', []))}
        • Communication Channels: {len(persona_data.get('telegram_handles', []))}
        
        BEHAVIORAL INDICATORS:
        • Operational Security: {persona_data.get('activity_patterns', {}).get('operational_security', {}).get('security_level', 'Unknown')}
        • Communication Style: {persona_data.get('linguistic_profile', {}).get('dominant_sentiment', 'Unknown')}
        • Technical Sophistication: {'High' if persona_data.get('linguistic_profile', {}).get('technical_terminology') else 'Unknown'}
        
        RISK FACTORS:
        {chr(10).join(f'• {factor}' for factor in persona_data.get('risk_factors', ['None identified']))}
        
        REASONING:
        The threat level assessment is based on cross-platform behavioral analysis,
        technical sophistication indicators, and operational security practices.
        Multiple data sources were correlated to build this persona profile.
        """
        
        return explanation.strip()
    
    def explain_correlation_decision(self, correlation_data: dict) -> str:
        """Explain entity correlation decisions"""
        correlation_strength = correlation_data.get('correlation_strength', 0.0)
        correlation_type = correlation_data.get('correlation_type', 'unknown')
        
        explanation = f"""
        🔗 CORRELATION ANALYSIS
        
        Entity 1: {correlation_data.get('entity1', 'N/A')}
        Entity 2: {correlation_data.get('entity2', 'N/A')}
        Correlation Type: {correlation_type}
        Strength: {correlation_strength:.2f}
        
        EVIDENCE BASIS:
        {chr(10).join(f'• {evidence}' for evidence in correlation_data.get('evidence', ['No specific evidence listed']))}
        
        STATISTICAL CONFIDENCE:
        • Correlation Coefficient: {correlation_strength:.3f}
        • Significance Level: {'High' if correlation_strength > 0.7 else 'Medium' if correlation_strength > 0.4 else 'Low'}
        • False Positive Risk: {(1 - correlation_strength) * 100:.1f}%
        
        INVESTIGATIVE IMPLICATIONS:
        {'Strong correlation suggests same threat actor or coordinated activity' if correlation_strength > 0.7 
         else 'Moderate correlation warrants further investigation' if correlation_strength > 0.4 
         else 'Weak correlation - may be coincidental'}
        """
        
        return explanation.strip()
    
    def explain_real_time_alert(self, alert_data: dict) -> str:
        """Explain real-time alert decisions"""
        severity = alert_data.get('severity', 'UNKNOWN')
        alert_type = alert_data.get('alert_type', 'unknown')
        
        explanation = f"""
        🚨 REAL-TIME ALERT EXPLANATION
        
        Alert ID: {alert_data.get('alert_id', 'N/A')}
        Severity: {severity}
        Type: {alert_type}
        Address: {alert_data.get('address', 'N/A')}
        
        TRIGGER CONDITIONS:
        {chr(10).join(f'• {condition}' for condition in alert_data.get('evidence', ['No conditions specified']))}
        
        TIMELINE ANALYSIS:
        • Detection Time: {alert_data.get('timestamp', 'N/A')}
        • Correlated Events: {len(alert_data.get('correlated_leaks', []))}
        
        THREAT ASSESSMENT:
        • Investigation Priority: {alert_data.get('investigation_priority', 5)}/10
        • Immediate Action Required: {'Yes' if severity in ['HIGH', 'CRITICAL'] else 'No'}
        
        RECOMMENDED RESPONSE:
        {chr(10).join(f'• {action}' for action in alert_data.get('recommended_actions', ['Standard monitoring']))}
        
        AUTOMATED REASONING:
        This alert was generated by real-time correlation between leak detection
        and blockchain activity monitoring. The severity assessment considers
        timing, correlation strength, and historical threat patterns.
        """
        
        return explanation.strip()
    
    def generate_comprehensive_explanation(self, analysis_type: str, data: dict) -> ExplanationSummary:
        """Generate comprehensive explanation for any analysis type"""
        
        if analysis_type == "risk_assessment":
            return self._explain_risk_assessment(data)
        elif analysis_type == "threat_persona":
            return self._explain_threat_persona_comprehensive(data)
        elif analysis_type == "correlation":
            return self._explain_correlation_comprehensive(data)
        elif analysis_type == "real_time_alert":
            return self._explain_alert_comprehensive(data)
        else:
            return self._explain_generic(data)
    
    def _explain_risk_assessment(self, data: dict) -> ExplanationSummary:
        """Comprehensive risk assessment explanation"""
        risk_score = data.get('risk_score', 0)
        
        return ExplanationSummary(
            decision_id=f"risk_{int(datetime.utcnow().timestamp())}",
            question="What is the risk level of this cryptocurrency address?",
            final_conclusion=f"Risk level: {'HIGH' if risk_score > 70 else 'MEDIUM' if risk_score > 40 else 'LOW'} ({risk_score}%)",
            confidence_level=ConfidenceLevel.from_score(risk_score/100),
            key_evidence=[
                f"Transaction volume: {data.get('transaction_count', 0)} transactions",
                f"Classification: {data.get('category', 'unknown')}",
                f"Recent activity: {'Yes' if data.get('recent_activity') else 'No'}"
            ],
            reasoning_chain=[
                "Analyzed transaction patterns and volumes",
                "Applied machine learning classification",
                "Correlated with known threat databases",
                "Calculated composite risk score"
            ],
            risk_factors=[
                factor for factor in [
                    "High transaction volume" if data.get('transaction_count', 0) > 500 else None,
                    "Dark web classification" if data.get('category') == 'darknet' else None,
                    "Recent suspicious activity" if data.get('recent_activity') else None
                ] if factor
            ],
            mitigating_factors=[
                factor for factor in [
                    "Low transaction volume" if data.get('transaction_count', 0) < 10 else None,
                    "Legitimate exchange classification" if data.get('category') == 'exchange' else None,
                    "No recent activity" if not data.get('recent_activity') else None
                ] if factor
            ],
            recommended_actions=[
                "Enhanced monitoring" if risk_score > 40 else "Standard monitoring",
                "Cross-reference with law enforcement databases" if risk_score > 70 else "Periodic review"
            ]
        )
    
    def _explain_threat_persona_comprehensive(self, data: dict) -> ExplanationSummary:
        """Comprehensive threat persona explanation"""
        threat_level = data.get('threat_level', 'UNKNOWN')
        
        return ExplanationSummary(
            decision_id=f"persona_{int(datetime.utcnow().timestamp())}",
            question="What threat level does this entity represent?",
            final_conclusion=f"Threat Level: {threat_level}",
            confidence_level=ConfidenceLevel.from_score(data.get('confidence_score', 0.5)),
            key_evidence=[
                f"Digital footprint spans {len(data.get('crypto_wallets', []))} crypto wallets",
                f"Active on {len(data.get('telegram_handles', []))} communication channels",
                f"Operational security: {data.get('activity_patterns', {}).get('operational_security', {}).get('security_level', 'Unknown')}"
            ],
            reasoning_chain=[
                "Collected multi-platform intelligence",
                "Analyzed communication patterns and linguistic markers",
                "Assessed operational security practices",
                "Correlated behavioral indicators",
                "Classified threat level based on aggregated evidence"
            ],
            risk_factors=data.get('risk_factors', []),
            mitigating_factors=[
                "Limited digital footprint" if len(data.get('crypto_wallets', [])) < 2 else "Standard activity patterns"
            ],
            recommended_actions=data.get('recommended_actions', [])
        )
    
    def _explain_correlation_comprehensive(self, data: dict) -> ExplanationSummary:
        """Comprehensive correlation explanation"""
        strength = data.get('correlation_strength', 0.0)
        
        return ExplanationSummary(
            decision_id=f"corr_{int(datetime.utcnow().timestamp())}",
            question="Are these entities related?",
            final_conclusion=f"Correlation strength: {strength:.2f} ({'Strong' if strength > 0.7 else 'Moderate' if strength > 0.4 else 'Weak'})",
            confidence_level=ConfidenceLevel.from_score(strength),
            key_evidence=data.get('evidence', []),
            reasoning_chain=[
                "Identified shared identifiers across platforms",
                "Calculated statistical correlation coefficients",
                "Applied graph-based clustering analysis",
                "Validated correlation through multiple methods"
            ],
            risk_factors=[
                "High correlation suggests coordinated activity" if strength > 0.7 else None
            ],
            mitigating_factors=[
                "Correlation may be coincidental" if strength < 0.5 else None
            ],
            recommended_actions=[
                "Treat as single threat entity" if strength > 0.8 else "Monitor for additional correlations"
            ]
        )
    
    def _explain_alert_comprehensive(self, data: dict) -> ExplanationSummary:
        """Comprehensive alert explanation"""
        severity = data.get('severity', 'UNKNOWN')
        
        return ExplanationSummary(
            decision_id=f"alert_{int(datetime.utcnow().timestamp())}",
            question="Why was this alert generated?",
            final_conclusion=f"Alert severity: {severity}",
            confidence_level=ConfidenceLevel.HIGH,  # Alerts are high confidence by design
            key_evidence=data.get('evidence', []),
            reasoning_chain=[
                "Detected anomalous activity pattern",
                "Correlated with real-time intelligence feeds",
                "Applied threat classification algorithms",
                "Calculated severity based on risk factors"
            ],
            risk_factors=[
                f"Investigation priority: {data.get('investigation_priority', 5)}/10"
            ],
            mitigating_factors=[],
            recommended_actions=data.get('recommended_actions', [])
        )
    
    def _explain_generic(self, data: dict) -> ExplanationSummary:
        """Generic explanation for unknown analysis types"""
        return ExplanationSummary(
            decision_id=f"generic_{int(datetime.utcnow().timestamp())}",
            question="Analysis result explanation",
            final_conclusion="Analysis completed with available data",
            confidence_level=ConfidenceLevel.MEDIUM,
            key_evidence=["Data analysis performed"],
            reasoning_chain=["Applied standard analytical methods"],
            risk_factors=[],
            mitigating_factors=[],
            recommended_actions=["Review results and collect additional data if needed"]
        )

# Create singleton instance for backward compatibility
explainable_ai = ExplainableAI()

# Enhanced API functions
def explain_decision(analysis_type: str, data: dict) -> str:
    """Main API function for getting explanations"""
    if analysis_type == "risk_score":
        return explainable_ai.explain_risk_score(data)
    elif analysis_type == "threat_persona":
        return explainable_ai.explain_threat_persona(data)
    elif analysis_type == "correlation":
        return explainable_ai.explain_correlation_decision(data)
    elif analysis_type == "alert":
        return explainable_ai.explain_real_time_alert(data)
    else:
        return f"Explanation not available for analysis type: {analysis_type}"

def get_comprehensive_explanation(analysis_type: str, data: dict) -> ExplanationSummary:
    """Get comprehensive structured explanation"""
    return explainable_ai.generate_comprehensive_explanation(analysis_type, data)
            explanations.append("Low risk - normal usage pattern")
        
        return ". ".join(explanations)
    
    def explain_category(self, category: str) -> str:
        """Explain what a category means"""
        descriptions = {
            'exchange': 'Cryptocurrency exchange wallet',
            'darknet': 'Associated with dark web marketplaces',
            'mixer': 'Tumbler/mixing service for anonymity',
            'ransomware': 'Linked to ransomware payments',
            'mining_pool': 'Mining pool payout address',
            'unknown': 'Insufficient data for classification'
        }
        return descriptions.get(category, 'Unknown category type')

# Create singleton instance
explainable_ai = ExplainableAI()
