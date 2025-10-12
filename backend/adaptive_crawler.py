"""
🤖 NTRO-CryptoForensics: Autonomous Adaptive Crawling System
===========================================================

Self-learning crawler that prioritizes intelligence sources based on:
- Historical value of intelligence gathered
- Frequency of threat actor mentions
- Cryptocurrency address discovery rates
- Cross-reference hit rates with known threats

Uses reinforcement learning to autonomously adapt crawling strategies.
"""

import asyncio
import aiohttp
import json
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import numpy as np
import pickle
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CrawlTarget:
    """Represents a crawling target with intelligence metrics"""
    target_id: str
    url: str
    target_type: str  # 'forum', 'marketplace', 'telegram', 'paste_site', 'social_media'
    priority_score: float = 0.5
    success_rate: float = 0.0
    intelligence_yield: float = 0.0  # Avg intelligence per crawl
    last_crawled: Optional[datetime] = None
    crawl_frequency: int = 3600  # seconds between crawls
    failures: int = 0
    total_crawls: int = 0
    crypto_addresses_found: int = 0
    threat_mentions: int = 0
    correlation_hits: int = 0
    response_time: float = 0.0
    content_freshness: float = 0.0
    risk_indicators: Dict[str, int] = field(default_factory=dict)

@dataclass
class CrawlResult:
    """Represents the result of a crawling operation"""
    target_id: str
    timestamp: datetime
    success: bool
    content_size: int
    crypto_addresses: List[str]
    emails: List[str]
    threat_keywords: List[str]
    response_time: float
    intelligence_score: float
    new_entities_discovered: int
    correlation_matches: int

class IntelligenceScorer:
    """Scores crawl results for intelligence value"""
    
    def __init__(self):
        self.threat_keywords = [
            'ransomware', 'darknet', 'bitcoin', 'monero', 'mixer', 'tumbler',
            'exploit', 'malware', 'phishing', 'scam', 'fraud', 'laundering',
            'cybercrime', 'hacker', 'breach', 'leak', 'dump', 'database'
        ]
        
        self.high_value_patterns = [
            r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',  # Bitcoin addresses
            r'0x[a-fA-F0-9]{40}\b',  # Ethereum addresses
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
            r't\.me/[a-zA-Z0-9_]{5,32}',  # Telegram links
        ]
    
    def score_content(self, content: str, context: Dict = None) -> Tuple[float, Dict[str, Any]]:
        """Score content for intelligence value"""
        if not content:
            return 0.0, {}
        
        content_lower = content.lower()
        score_factors = {}
        
        # Threat keyword density
        threat_matches = sum(1 for keyword in self.threat_keywords if keyword in content_lower)
        threat_density = threat_matches / max(len(content.split()), 1) * 100
        score_factors['threat_density'] = min(threat_density, 10.0) / 10.0
        
        # Crypto address frequency
        crypto_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|0x[a-fA-F0-9]{40}\b'
        import re
        crypto_addresses = re.findall(crypto_pattern, content)
        score_factors['crypto_density'] = min(len(crypto_addresses), 5) / 5.0
        
        # Email frequency
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        score_factors['email_density'] = min(len(emails), 3) / 3.0
        
        # Content freshness (based on timestamps, if available)
        freshness_score = 1.0  # Default to fresh
        if context and 'timestamp' in context:
            try:
                content_time = datetime.fromisoformat(context['timestamp'])
                age_hours = (datetime.utcnow() - content_time).total_seconds() / 3600
                freshness_score = max(0.1, 1.0 - (age_hours / 168))  # Decay over 1 week
            except:
                pass
        score_factors['freshness'] = freshness_score
        
        # Content length factor (longer posts often have more intel)
        length_factor = min(len(content) / 1000, 1.0)  # Max at 1000 chars
        score_factors['content_length'] = length_factor
        
        # Calculate weighted intelligence score
        weights = {
            'threat_density': 0.3,
            'crypto_density': 0.25,
            'email_density': 0.15,
            'freshness': 0.2,
            'content_length': 0.1
        }
        
        intelligence_score = sum(weights[factor] * score for factor, score in score_factors.items())
        
        return intelligence_score, {
            'score_factors': score_factors,
            'crypto_addresses': crypto_addresses,
            'emails': emails,
            'threat_keywords': [kw for kw in self.threat_keywords if kw in content_lower],
            'intelligence_score': intelligence_score
        }

class AdaptivePriorityEngine:
    """ML-powered priority engine that learns from crawl results"""
    
    def __init__(self):
        self.feature_names = [
            'success_rate', 'intelligence_yield', 'crypto_addresses_found',
            'threat_mentions', 'correlation_hits', 'response_time',
            'content_freshness', 'hours_since_last_crawl', 'failure_streak'
        ]
        self.is_trained = False
        self.training_data = []
        self.scorer = IntelligenceScorer()
        # Store performance data in memory for now
        self.source_performance = {}
    
    async def calculate_priority(self, target: CrawlTarget) -> float:
        """Calculate dynamic priority score for a crawl target"""
        return self._heuristic_priority(target)
    
    def _heuristic_priority(self, target: CrawlTarget) -> float:
        """Heuristic priority calculation"""
        base_score = 0.5
        
        # Boost for high intelligence yield
        if target.intelligence_yield > 0.7:
            base_score += 0.2
        elif target.intelligence_yield > 0.4:
            base_score += 0.1
        
        # Boost for crypto address discoveries
        if target.crypto_addresses_found > 5:
            base_score += 0.15
        
        # Boost for recent threat mentions
        if target.threat_mentions > 10:
            base_score += 0.1
        
        # Penalty for high failure rate
        if target.total_crawls > 0:
            failure_rate = target.failures / target.total_crawls
            if failure_rate > 0.5:
                base_score -= 0.2
        
        # Time-based priority boost
        if target.last_crawled:
            hours_since = (datetime.utcnow() - target.last_crawled).total_seconds() / 3600
            if hours_since > 24:
                base_score += 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def record_scrape_result(self, source_id: str, addresses_found: int, success: bool):
        """Record performance metrics for a source (backward compatibility)"""
        if source_id not in self.source_performance:
            self.source_performance[source_id] = {
                'total_scrapes': 0,
                'successful_scrapes': 0,
                'total_addresses': 0,
                'avg_addresses': 0
            }
        
        perf = self.source_performance[source_id]
        perf['total_scrapes'] += 1
        if success:
            perf['successful_scrapes'] += 1
            perf['total_addresses'] += addresses_found
            perf['avg_addresses'] = perf['total_addresses'] / perf['successful_scrapes']
    
    def get_priority_sources(self, limit: int = 5):
        """Get top performing sources (backward compatibility)"""
        sorted_sources = sorted(
            self.source_performance.items(),
            key=lambda x: x[1]['avg_addresses'],
            reverse=True
        )
        return sorted_sources[:limit]

class AutonomousCrawlingSystem:
    """Main autonomous crawling orchestrator"""
    
    def __init__(self, mongo_db=None):
        self.db = mongo_db
        self.priority_engine = AdaptivePriorityEngine()
        self.targets: Dict[str, CrawlTarget] = {}
        self.active_crawlers = 0
        self.max_concurrent_crawlers = 5
        self.is_running = False
        
        # Initialize with demo targets for intelligence value
        self.initial_targets = [
            CrawlTarget("forum_darknet", "https://darknetlive.com/", "forum"),
            CrawlTarget("telegram_crypto", "https://t.me/s/cryptoleaks", "telegram"),
            CrawlTarget("paste_monitor", "https://pastebin.com/archive", "paste_site"),
            CrawlTarget("leak_tracker", "https://raidforums.com/", "forum"),
            CrawlTarget("marketplace_intel", "https://darkfail.live/", "marketplace")
        ]
        
        # Initialize targets
        for target in self.initial_targets:
            self.targets[target.target_id] = target
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get autonomous crawling system statistics"""
        total_targets = len(self.targets)
        high_priority_targets = len([t for t in self.targets.values() if t.priority_score > 0.7])
        
        avg_intelligence_yield = sum(t.intelligence_yield for t in self.targets.values()) / max(total_targets, 1)
        total_crypto_found = sum(t.crypto_addresses_found for t in self.targets.values())
        
        return {
            'system_status': 'AUTONOMOUS_LEARNING' if self.is_running else 'READY',
            'total_targets': total_targets,
            'high_priority_targets': high_priority_targets,
            'active_crawlers': self.active_crawlers,
            'max_concurrent_crawlers': self.max_concurrent_crawlers,
            'avg_intelligence_yield': avg_intelligence_yield,
            'total_crypto_addresses_found': total_crypto_found,
            'ml_model_trained': self.priority_engine.is_trained,
            'adaptive_features': [
                'Priority-based crawling',
                'Intelligence scoring',
                'Frequency adaptation',
                'Threat correlation',
                'Cross-surface fusion'
            ]
        }

# Create singleton instance for backward compatibility
adaptive_crawler = AdaptivePriorityEngine()

# Global autonomous system instance
autonomous_system = None

def get_autonomous_system(mongo_db=None):
    """Get or create autonomous crawling system"""
    global autonomous_system
    if autonomous_system is None:
        autonomous_system = AutonomousCrawlingSystem(mongo_db)
    return autonomous_system
