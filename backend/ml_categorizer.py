"""
Machine Learning-Based Address Categorization Module
Advanced ML models for cryptocurrency address classification
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Simplified ML implementation (production would use scikit-learn, transformers, etc.)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddressCategorizer:
    """ML-based cryptocurrency address categorization"""
    
    def __init__(self):
        # Predefined categories
        self.categories = {
            'ransomware': 0,
            'darknet_market': 1,
            'money_laundering': 2,
            'terror_financing': 3,
            'drug_trafficking': 4,
            'fraud_scam': 5,
            'exchange': 6,
            'mining': 7,
            'gambling': 8,
            'legitimate': 9,
            'unknown': 10
        }
        
        # Risk category keywords
        self.risk_keywords = {
            'ransomware': ['ransomware', 'ransom', 'wannacry', 'locky', 'petya', 'ryuk', 'encrypt'],
            'darknet_market': ['darknet', 'dark web', 'marketplace', 'silk road', 'alphabay', 'dream market', 'tor'],
            'money_laundering': ['laundering', 'mixer', 'tumbler', 'mixing', 'wash', 'clean'],
            'terror_financing': ['terrorism', 'terrorist', 'isis', 'funding', 'jihad'],
            'drug_trafficking': ['drug', 'cocaine', 'heroin', 'marijuana', 'trafficking', 'dealer'],
            'fraud_scam': ['scam', 'fraud', 'phishing', 'ponzi', 'pyramid', 'fake', 'steal'],
            'exchange': ['exchange', 'coinbase', 'binance', 'kraken', 'bitfinex', 'trading'],
            'mining': ['mining', 'pool', 'miner', 'hashrate'],
            'gambling': ['gambling', 'casino', 'poker', 'dice', 'bet'],
        }
    
    def extract_features(self, address_data: Dict) -> np.ndarray:
        """Extract features from address data for classification"""
        features = []
        
        # Transaction-based features
        tx_count = address_data.get('tx_count', 0)
        balance = address_data.get('balance', 0)
        total_received = address_data.get('total_received', 0)
        total_sent = address_data.get('total_sent', 0)
        
        features.extend([
            min(tx_count / 1000.0, 1.0),  # Normalized transaction count
            min(balance / 100.0, 1.0),     # Normalized balance
            min(total_received / 1000.0, 1.0),
            min(total_sent / 1000.0, 1.0),
        ])
        
        # Context-based features (keyword matching)
        context = address_data.get('context', '').lower()
        for category in self.risk_keywords.keys():
            has_keyword = any(kw in context for kw in self.risk_keywords[category])
            features.append(1.0 if has_keyword else 0.0)
        
        # Source-based features
        source_type = address_data.get('source_type', 'unknown')
        features.append(1.0 if source_type == 'dark_web' else 0.0)
        features.append(1.0 if source_type == 'surface_web' else 0.0)
        
        # PII correlation features
        pii_data = address_data.get('pii_data', {})
        features.append(1.0 if pii_data else 0.0)
        features.append(len(pii_data.get('email', [])) / 10.0)
        features.append(len(pii_data.get('phone', [])) / 10.0)
        
        return np.array(features, dtype=np.float32)
    
    def categorize_address(self, address_data: Dict) -> Dict:
        """Categorize address using rule-based and feature extraction"""
        context = address_data.get('context', '').lower()
        
        # Score each category
        category_scores = {}
        
        for category, keywords in self.risk_keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword in context:
                    score += 1.0
            category_scores[category] = score
        
        # Find highest scoring category
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[best_category]
            
            if max_score > 0:
                confidence = min(max_score / len(self.risk_keywords[best_category]), 1.0)
                return {
                    'category': best_category,
                    'confidence': confidence,
                    'alternative_categories': self._get_alternatives(category_scores)
                }
        
        # Default to unknown
        return {
            'category': 'unknown',
            'confidence': 0.5,
            'alternative_categories': []
        }
    
    def _get_alternatives(self, category_scores: Dict) -> List[Dict]:
        """Get alternative category suggestions"""
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        alternatives = []
        for category, score in sorted_categories[1:4]:  # Top 3 alternatives
            if score > 0:
                alternatives.append({
                    'category': category,
                    'score': score
                })
        
        return alternatives
    
    def calculate_risk_score(self, address_data: Dict, category: str) -> float:
        """Calculate comprehensive risk score"""
        risk_score = 0.0
        
        # Base risk by category
        high_risk_categories = ['ransomware', 'darknet_market', 'money_laundering', 
                               'terror_financing', 'drug_trafficking', 'fraud_scam']
        medium_risk_categories = ['gambling']
        
        if category in high_risk_categories:
            risk_score += 0.6
        elif category in medium_risk_categories:
            risk_score += 0.3
        else:
            risk_score += 0.1
        
        # Transaction volume risk
        tx_count = address_data.get('tx_count', 0)
        if tx_count > 1000:
            risk_score += 0.2
        elif tx_count > 100:
            risk_score += 0.1
        
        # Balance risk (very high balance = potential laundering)
        balance = address_data.get('balance', 0)
        if balance > 100:
            risk_score += 0.1
        
        # PII correlation increases risk
        if address_data.get('pii_data'):
            risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    def analyze_transaction_pattern(self, transactions: List[Dict]) -> Dict:
        """Analyze transaction patterns for suspicious activity"""
        if not transactions:
            return {'pattern': 'no_data', 'suspicion_level': 0.0}
        
        # Calculate transaction statistics
        amounts = [tx.get('amount', 0) for tx in transactions]
        timestamps = [tx.get('timestamp') for tx in transactions if tx.get('timestamp')]
        
        avg_amount = np.mean(amounts) if amounts else 0
        std_amount = np.std(amounts) if amounts else 0
        
        patterns = []
        suspicion = 0.0
        
        # Check for round number transactions (money laundering indicator)
        round_numbers = sum(1 for amt in amounts if amt % 1 == 0 and amt > 0)
        if round_numbers / len(amounts) > 0.7:
            patterns.append('frequent_round_amounts')
            suspicion += 0.2
        
        # Check for high variability (mixing indicator)
        if std_amount > avg_amount * 2:
            patterns.append('high_variability')
            suspicion += 0.15
        
        # Check for rapid transactions
        if len(timestamps) > 1:
            time_diffs = []
            sorted_times = sorted(timestamps)
            for i in range(1, len(sorted_times)):
                if isinstance(sorted_times[i], datetime) and isinstance(sorted_times[i-1], datetime):
                    diff = (sorted_times[i] - sorted_times[i-1]).total_seconds()
                    time_diffs.append(diff)
            
            if time_diffs and np.mean(time_diffs) < 300:  # Less than 5 minutes average
                patterns.append('rapid_transactions')
                suspicion += 0.25
        
        return {
            'patterns': patterns,
            'suspicion_level': min(suspicion, 1.0),
            'avg_amount': avg_amount,
            'transaction_count': len(transactions)
        }


class AddressClusterer:
    """Cluster related addresses together"""
    
    def __init__(self):
        self.clusters = {}
    
    def find_related_addresses(self, address: str, all_addresses: List[Dict]) -> List[str]:
        """Find addresses related through transactions or common entities"""
        related = []
        
        # Simple implementation: find addresses with shared PII
        target_pii = None
        for addr_data in all_addresses:
            if addr_data['address'] == address:
                target_pii = addr_data.get('pii_data', {})
                break
        
        if not target_pii:
            return []
        
        # Find other addresses with matching PII
        for addr_data in all_addresses:
            if addr_data['address'] == address:
                continue
            
            other_pii = addr_data.get('pii_data', {})
            
            # Check for email matches
            if target_pii.get('email') and other_pii.get('email'):
                if set(target_pii['email']) & set(other_pii['email']):
                    related.append(addr_data['address'])
            
            # Check for phone matches
            if target_pii.get('phone') and other_pii.get('phone'):
                if set(target_pii['phone']) & set(other_pii['phone']):
                    related.append(addr_data['address'])
        
        return list(set(related))
    
    def create_cluster(self, addresses: List[str]) -> str:
        """Create a cluster of related addresses"""
        import uuid
        cluster_id = str(uuid.uuid4())
        
        self.clusters[cluster_id] = {
            'id': cluster_id,
            'addresses': addresses,
            'created_at': datetime.utcnow().isoformat(),
            'size': len(addresses)
        }
        
        return cluster_id
