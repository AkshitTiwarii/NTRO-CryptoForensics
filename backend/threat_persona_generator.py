"""
👤 NTRO-CryptoForensics: Threat Persona Graph Generator
======================================================

AI-powered system that generates dynamic threat personas by linking:
- PII (Personal Identifiable Information)
- Wallet clusters and transaction patterns
- Dark-net activity and forum profiles
- Linguistic style analysis
- Behavioral pattern recognition

Creates actionable intelligence profiles for threat attribution.
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import hashlib
import logging
from enum import Enum

import networkx as nx
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ConfidenceLevel(Enum):
    VERY_LOW = 0.2
    LOW = 0.4
    MEDIUM = 0.6
    HIGH = 0.8
    VERY_HIGH = 0.95

@dataclass
class PersonaAttribute:
    """Individual attribute of a threat persona"""
    attribute_type: str  # 'crypto_wallet', 'email', 'username', 'linguistic_pattern'
    value: str
    confidence: float
    sources: List[str]
    first_seen: datetime
    last_seen: datetime
    frequency: int = 1

@dataclass
class ThreatPersona:
    """Complete threat actor persona"""
    persona_id: str
    primary_identifier: str
    threat_level: ThreatLevel
    confidence_score: float
    
    # Core attributes
    crypto_wallets: List[PersonaAttribute] = field(default_factory=list)
    email_addresses: List[PersonaAttribute] = field(default_factory=list)
    usernames: List[PersonaAttribute] = field(default_factory=list)
    social_profiles: List[PersonaAttribute] = field(default_factory=list)
    onion_profiles: List[PersonaAttribute] = field(default_factory=list)
    telegram_handles: List[PersonaAttribute] = field(default_factory=list)
    
    # Behavioral patterns
    linguistic_profile: Dict[str, Any] = field(default_factory=dict)
    activity_patterns: Dict[str, Any] = field(default_factory=dict)
    transaction_patterns: Dict[str, Any] = field(default_factory=dict)
    communication_patterns: Dict[str, Any] = field(default_factory=dict)
    
    # Intelligence summary
    attack_vectors: List[str] = field(default_factory=list)
    target_sectors: List[str] = field(default_factory=list)
    geographical_indicators: List[str] = field(default_factory=list)
    modus_operandi: List[str] = field(default_factory=list)
    
    # Timeline and evolution
    first_activity: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    activity_timeline: List[Dict] = field(default_factory=list)
    evolution_score: float = 0.0  # How much the persona has evolved
    
    # Threat assessment
    risk_factors: List[str] = field(default_factory=list)
    capability_assessment: Dict[str, float] = field(default_factory=dict)
    intent_indicators: List[str] = field(default_factory=list)
    
    # Investigation aids
    recommended_actions: List[str] = field(default_factory=list)
    intelligence_gaps: List[str] = field(default_factory=list)
    correlation_leads: List[str] = field(default_factory=list)

class LinguisticProfiler:
    """Analyzes writing patterns to build linguistic profiles"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.language_patterns = {}
    
    def analyze_text_corpus(self, texts: List[str], author_id: str) -> Dict[str, Any]:
        """Analyze a corpus of texts to build linguistic profile"""
        if not texts:
            return {}
        
        combined_text = ' '.join(texts)
        
        profile = {
            'total_text_length': len(combined_text),
            'average_sentence_length': self._calculate_avg_sentence_length(texts),
            'vocabulary_richness': self._calculate_vocabulary_richness(combined_text),
            'sentiment_profile': self._analyze_sentiment_profile(texts),
            'writing_style': self._analyze_writing_style(combined_text),
            'technical_terminology': self._extract_technical_terms(combined_text),
            'linguistic_markers': self._extract_linguistic_markers(combined_text),
            'communication_frequency': self._analyze_communication_frequency(texts),
            'topic_preferences': self._extract_topic_preferences(combined_text)
        }
        
        return profile
    
    def _calculate_avg_sentence_length(self, texts: List[str]) -> float:
        """Calculate average sentence length"""
        total_sentences = 0
        total_words = 0
        
        for text in texts:
            blob = TextBlob(text)
            sentences = blob.sentences
            total_sentences += len(sentences)
            total_words += len(blob.words)
        
        return total_words / max(total_sentences, 1)
    
    def _calculate_vocabulary_richness(self, text: str) -> float:
        """Calculate type-token ratio (vocabulary richness)"""
        blob = TextBlob(text)
        words = [word.lower() for word in blob.words if word.isalpha()]
        unique_words = set(words)
        
        return len(unique_words) / max(len(words), 1)
    
    def _analyze_sentiment_profile(self, texts: List[str]) -> Dict[str, float]:
        """Analyze sentiment patterns"""
        sentiments = []
        
        for text in texts:
            blob = TextBlob(text)
            sentiments.append({
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            })
        
        if not sentiments:
            return {'avg_polarity': 0.0, 'avg_subjectivity': 0.0, 'sentiment_variance': 0.0}
        
        polarities = [s['polarity'] for s in sentiments]
        subjectivities = [s['subjectivity'] for s in sentiments]
        
        return {
            'avg_polarity': np.mean(polarities),
            'avg_subjectivity': np.mean(subjectivities),
            'sentiment_variance': np.var(polarities),
            'dominant_sentiment': 'positive' if np.mean(polarities) > 0.1 else 'negative' if np.mean(polarities) < -0.1 else 'neutral'
        }
    
    def _analyze_writing_style(self, text: str) -> Dict[str, Any]:
        """Analyze writing style characteristics"""
        # Punctuation usage
        punctuation_density = len([c for c in text if c in '!?.,;:']) / max(len(text), 1)
        
        # Capitalization patterns
        caps_density = len([c for c in text if c.isupper()]) / max(len(text), 1)
        
        # Number usage
        number_density = len(re.findall(r'\d+', text)) / max(len(text.split()), 1)
        
        # Profanity/aggressive language (basic detection)
        aggressive_words = ['hack', 'attack', 'steal', 'scam', 'fraud', 'kill', 'destroy', 'pwn']
        aggressive_count = sum(1 for word in aggressive_words if word in text.lower())
        
        return {
            'punctuation_density': punctuation_density,
            'capitalization_density': caps_density,
            'number_usage': number_density,
            'aggressive_language_score': aggressive_count / max(len(text.split()), 1),
            'avg_word_length': np.mean([len(word) for word in text.split()]) if text.split() else 0
        }
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract cryptocurrency and cybercrime technical terms"""
        crypto_terms = [
            'bitcoin', 'ethereum', 'monero', 'zcash', 'mixer', 'tumbler',
            'wallet', 'private key', 'public key', 'blockchain', 'mining',
            'exchange', 'satoshi', 'hash', 'transaction', 'address'
        ]
        
        cyber_terms = [
            'malware', 'ransomware', 'trojan', 'backdoor', 'exploit',
            'phishing', 'ddos', 'botnet', 'keylogger', 'rootkit',
            'vulnerability', 'zero-day', 'payload', 'c2', 'tor'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in crypto_terms + cyber_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _extract_linguistic_markers(self, text: str) -> Dict[str, Any]:
        """Extract linguistic markers that might indicate origin or background"""
        # Time zone references
        time_zones = re.findall(r'\b(EST|PST|GMT|UTC|CET|JST)\b', text.upper())
        
        # Currency mentions
        currencies = re.findall(r'\$|\€|£|¥|₽', text)
        
        # Language mixing (non-English words/phrases)
        foreign_patterns = [
            r'\b(да|нет|сука|блять)\b',  # Russian
            r'\b(sí|no|gracias|por favor)\b',  # Spanish
            r'\b(oui|non|merci|s\'il vous plaît)\b',  # French
            r'\b(ja|nein|danke|bitte)\b',  # German
        ]
        
        foreign_words = []
        for pattern in foreign_patterns:
            foreign_words.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return {
            'time_zones_mentioned': time_zones,
            'currencies_mentioned': currencies,
            'foreign_language_indicators': foreign_words,
            'possible_origin_hints': self._infer_origin_hints(time_zones, currencies, foreign_words)
        }
    
    def _infer_origin_hints(self, time_zones: List[str], currencies: List[str], foreign_words: List[str]) -> List[str]:
        """Infer possible geographical/cultural origins"""
        hints = []
        
        if 'EST' in time_zones or '$' in currencies:
            hints.append('North America')
        if 'CET' in time_zones or '€' in currencies:
            hints.append('Europe')
        if 'JST' in time_zones or '¥' in currencies:
            hints.append('Asia')
        if '₽' in currencies or any('да' in w or 'нет' in w for w in foreign_words):
            hints.append('Russia/Eastern Europe')
        
        return hints
    
    def _analyze_communication_frequency(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze communication patterns and frequency"""
        # This would be enhanced with actual timestamp data
        return {
            'total_communications': len(texts),
            'avg_message_length': np.mean([len(text) for text in texts]) if texts else 0,
            'communication_style': 'verbose' if np.mean([len(text) for text in texts]) > 500 else 'concise'
        }
    
    def _extract_topic_preferences(self, text: str) -> List[str]:
        """Extract topic preferences from text"""
        topic_keywords = {
            'cryptocurrency': ['bitcoin', 'crypto', 'mining', 'wallet', 'exchange'],
            'hacking': ['hack', 'exploit', 'vulnerability', 'breach', 'attack'],
            'fraud': ['scam', 'fraud', 'phishing', 'social engineering'],
            'marketplace': ['selling', 'buying', 'price', 'deal', 'vendor'],
            'technology': ['software', 'hardware', 'server', 'network', 'system'],
            'drugs': ['mdma', 'cocaine', 'cannabis', 'pills', 'dealer'],
            'weapons': ['gun', 'weapon', 'ammunition', 'firearm']
        }
        
        text_lower = text.lower()
        topic_scores = {}
        
        for topic, keywords in topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                topic_scores[topic] = score
        
        # Return top topics
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, score in sorted_topics[:3]]

class BehavioralAnalyzer:
    """Analyzes behavioral patterns from various data sources"""
    
    def analyze_transaction_patterns(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze cryptocurrency transaction patterns"""
        if not transactions:
            return {}
        
        amounts = [tx.get('amount', 0) for tx in transactions]
        timestamps = [tx.get('timestamp') for tx in transactions if tx.get('timestamp')]
        
        patterns = {
            'total_transactions': len(transactions),
            'total_volume': sum(amounts),
            'avg_transaction_amount': np.mean(amounts) if amounts else 0,
            'transaction_frequency': self._calculate_transaction_frequency(timestamps),
            'amount_patterns': self._analyze_amount_patterns(amounts),
            'timing_patterns': self._analyze_timing_patterns(timestamps),
            'suspicious_indicators': self._detect_suspicious_patterns(transactions)
        }
        
        return patterns
    
    def _calculate_transaction_frequency(self, timestamps: List[str]) -> Dict[str, float]:
        """Calculate transaction frequency patterns"""
        if len(timestamps) < 2:
            return {'daily_average': 0, 'peak_hours': []}
        
        # Convert timestamps to datetime objects
        try:
            datetimes = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps if ts]
            
            # Calculate daily frequency
            date_counts = defaultdict(int)
            hour_counts = defaultdict(int)
            
            for dt in datetimes:
                date_counts[dt.date()] += 1
                hour_counts[dt.hour] += 1
            
            daily_avg = np.mean(list(date_counts.values()))
            peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            return {
                'daily_average': daily_avg,
                'peak_hours': [hour for hour, count in peak_hours],
                'activity_span_days': len(date_counts)
            }
        except:
            return {'daily_average': 0, 'peak_hours': [], 'activity_span_days': 0}
    
    def _analyze_amount_patterns(self, amounts: List[float]) -> Dict[str, Any]:
        """Analyze transaction amount patterns"""
        if not amounts:
            return {}
        
        amounts_array = np.array(amounts)
        
        return {
            'median_amount': np.median(amounts_array),
            'amount_variance': np.var(amounts_array),
            'round_number_preference': sum(1 for amt in amounts if amt == round(amt, 0)) / len(amounts),
            'micro_transactions': sum(1 for amt in amounts if amt < 0.01),
            'large_transactions': sum(1 for amt in amounts if amt > 1.0),
            'amount_clustering': self._detect_amount_clustering(amounts)
        }
    
    def _detect_amount_clustering(self, amounts: List[float]) -> bool:
        """Detect if transaction amounts cluster around specific values"""
        if len(amounts) < 5:
            return False
        
        # Check if many transactions are similar amounts
        rounded_amounts = [round(amt, 2) for amt in amounts]
        amount_counts = Counter(rounded_amounts)
        
        # If any amount appears more than 20% of the time, consider it clustering
        max_frequency = max(amount_counts.values())
        return max_frequency > len(amounts) * 0.2
    
    def _analyze_timing_patterns(self, timestamps: List[str]) -> Dict[str, Any]:
        """Analyze timing patterns in activities"""
        if not timestamps:
            return {}
        
        try:
            datetimes = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps if ts]
            
            if len(datetimes) < 2:
                return {}
            
            # Calculate intervals between activities
            intervals = []
            for i in range(1, len(datetimes)):
                interval = (datetimes[i] - datetimes[i-1]).total_seconds() / 3600  # hours
                intervals.append(interval)
            
            return {
                'avg_interval_hours': np.mean(intervals),
                'interval_variance': np.var(intervals),
                'regular_timing': np.var(intervals) < 12,  # Low variance suggests regular timing
                'burst_activity': any(interval < 1 for interval in intervals)  # Activities within an hour
            }
        except:
            return {}
    
    def _detect_suspicious_patterns(self, transactions: List[Dict]) -> List[str]:
        """Detect suspicious transaction patterns"""
        indicators = []
        
        amounts = [tx.get('amount', 0) for tx in transactions]
        
        # Structuring (avoiding reporting thresholds)
        threshold_amounts = [9999, 9900, 9500, 4999, 2999]
        for threshold in threshold_amounts:
            if sum(1 for amt in amounts if abs(amt - threshold) < 100) > 2:
                indicators.append(f"Possible structuring around ${threshold}")
        
        # Rapid succession of transactions
        timestamps = [tx.get('timestamp') for tx in transactions if tx.get('timestamp')]
        if len(timestamps) > 5:
            try:
                datetimes = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                for i in range(1, len(datetimes)):
                    if (datetimes[i] - datetimes[i-1]).total_seconds() < 300:  # 5 minutes
                        indicators.append("Rapid succession transactions detected")
                        break
            except:
                pass
        
        # Unusual amount precision
        precise_amounts = [amt for amt in amounts if len(str(amt).split('.')[-1]) > 6]
        if len(precise_amounts) > len(amounts) * 0.3:
            indicators.append("Unusually precise transaction amounts")
        
        return indicators

class ThreatPersonaGenerator:
    """Main class for generating threat personas"""
    
    def __init__(self, mongo_db=None):
        self.db = mongo_db
        self.linguistic_profiler = LinguisticProfiler()
        self.behavioral_analyzer = BehavioralAnalyzer()
        self.personas: Dict[str, ThreatPersona] = {}
        self.entity_graph = nx.Graph()
    
    async def generate_persona(self, entity_data: Dict[str, Any]) -> ThreatPersona:
        """Generate a comprehensive threat persona from entity data"""
        logger.info(f"🔍 Generating threat persona for entity: {entity_data.get('primary_id', 'unknown')}")
        
        # Create base persona
        persona_id = self._generate_persona_id(entity_data)
        persona = ThreatPersona(
            persona_id=persona_id,
            primary_identifier=entity_data.get('primary_id', 'unknown'),
            threat_level=ThreatLevel.MEDIUM,  # Will be calculated
            confidence_score=0.5  # Will be calculated
        )
        
        # Extract and analyze all attributes
        await self._extract_persona_attributes(persona, entity_data)
        
        # Perform linguistic analysis
        await self._analyze_linguistic_patterns(persona, entity_data)
        
        # Analyze behavioral patterns
        await self._analyze_behavioral_patterns(persona, entity_data)
        
        # Build activity timeline
        await self._build_activity_timeline(persona, entity_data)
        
        # Assess threat level and confidence
        await self._assess_threat_level(persona)
        await self._calculate_confidence_score(persona)
        
        # Generate intelligence summary
        await self._generate_intelligence_summary(persona)
        
        # Store persona
        self.personas[persona_id] = persona
        
        logger.info(f"✅ Generated {persona.threat_level.value} threat persona: {persona_id}")
        return persona
    
    def _generate_persona_id(self, entity_data: Dict[str, Any]) -> str:
        """Generate unique persona ID"""
        primary_id = entity_data.get('primary_id', 'unknown')
        hash_input = f"{primary_id}_{datetime.utcnow().date()}"
        return f"persona_{hashlib.md5(hash_input.encode()).hexdigest()[:8]}"
    
    async def _extract_persona_attributes(self, persona: ThreatPersona, entity_data: Dict[str, Any]):
        """Extract all persona attributes from entity data"""
        current_time = datetime.utcnow()
        
        # Crypto wallets
        for wallet in entity_data.get('crypto_addresses', []):
            attr = PersonaAttribute(
                attribute_type='crypto_wallet',
                value=wallet,
                confidence=0.8,
                sources=['blockchain_analysis'],
                first_seen=current_time,
                last_seen=current_time
            )
            persona.crypto_wallets.append(attr)
        
        # Email addresses
        for email in entity_data.get('email_addresses', []):
            attr = PersonaAttribute(
                attribute_type='email',
                value=email,
                confidence=0.7,
                sources=['leak_analysis'],
                first_seen=current_time,
                last_seen=current_time
            )
            persona.email_addresses.append(attr)
        
        # Usernames
        for username in entity_data.get('usernames', []):
            attr = PersonaAttribute(
                attribute_type='username',
                value=username,
                confidence=0.6,
                sources=['social_media', 'forum_analysis'],
                first_seen=current_time,
                last_seen=current_time
            )
            persona.usernames.append(attr)
        
        # Telegram handles
        for handle in entity_data.get('telegram_handles', []):
            attr = PersonaAttribute(
                attribute_type='telegram_handle',
                value=handle,
                confidence=0.8,
                sources=['telegram_monitoring'],
                first_seen=current_time,
                last_seen=current_time
            )
            persona.telegram_handles.append(attr)
    
    async def _analyze_linguistic_patterns(self, persona: ThreatPersona, entity_data: Dict[str, Any]):
        """Analyze linguistic patterns from communications"""
        text_corpus = []
        
        # Collect text data from various sources
        for post in entity_data.get('forum_posts', []):
            text_corpus.append(post.get('content', ''))
        
        for message in entity_data.get('telegram_messages', []):
            text_corpus.append(message.get('text', ''))
        
        for email in entity_data.get('email_contents', []):
            text_corpus.append(email.get('body', ''))
        
        if text_corpus:
            persona.linguistic_profile = self.linguistic_profiler.analyze_text_corpus(
                text_corpus, persona.persona_id
            )
    
    async def _analyze_behavioral_patterns(self, persona: ThreatPersona, entity_data: Dict[str, Any]):
        """Analyze behavioral patterns"""
        # Transaction pattern analysis
        transactions = entity_data.get('transactions', [])
        if transactions:
            persona.transaction_patterns = self.behavioral_analyzer.analyze_transaction_patterns(transactions)
        
        # Activity patterns
        persona.activity_patterns = {
            'total_activities': len(entity_data.get('activities', [])),
            'preferred_platforms': self._identify_preferred_platforms(entity_data),
            'communication_style': self._analyze_communication_style(entity_data),
            'operational_security': self._assess_operational_security(entity_data)
        }
    
    def _identify_preferred_platforms(self, entity_data: Dict[str, Any]) -> List[str]:
        """Identify preferred platforms based on activity"""
        platform_activity = defaultdict(int)
        
        platform_activity['telegram'] = len(entity_data.get('telegram_messages', []))
        platform_activity['forums'] = len(entity_data.get('forum_posts', []))
        platform_activity['email'] = len(entity_data.get('email_addresses', []))
        platform_activity['blockchain'] = len(entity_data.get('transactions', []))
        
        # Return platforms with significant activity
        return [platform for platform, count in platform_activity.items() if count > 0]
    
    def _analyze_communication_style(self, entity_data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze communication style characteristics"""
        all_text = []
        
        for post in entity_data.get('forum_posts', []):
            all_text.append(post.get('content', ''))
        
        combined_text = ' '.join(all_text)
        
        if not combined_text:
            return {'style': 'unknown'}
        
        # Basic style analysis
        avg_length = len(combined_text) / max(len(all_text), 1)
        
        style_indicators = {
            'verbosity': 'verbose' if avg_length > 500 else 'concise',
            'formality': 'formal' if '.' in combined_text and avg_length > 100 else 'informal',
            'technical_level': 'high' if len(self.linguistic_profiler._extract_technical_terms(combined_text)) > 5 else 'low'
        }
        
        return style_indicators
    
    def _assess_operational_security(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess operational security practices"""
        opsec_score = 0.0
        indicators = []
        
        # Check for Tor usage
        if any('onion' in url for url in entity_data.get('urls_visited', [])):
            opsec_score += 0.3
            indicators.append('Tor usage detected')
        
        # Check for encrypted communications
        if entity_data.get('telegram_handles'):
            opsec_score += 0.2
            indicators.append('Encrypted messaging')
        
        # Check for cryptocurrency mixing
        transactions = entity_data.get('transactions', [])
        mixer_addresses = ['mixer', 'tumbler', 'join']  # Known mixer patterns
        for tx in transactions:
            if any(pattern in tx.get('address', '').lower() for pattern in mixer_addresses):
                opsec_score += 0.3
                indicators.append('Cryptocurrency mixing')
                break
        
        # Check for VPN/proxy usage patterns
        ip_addresses = entity_data.get('ip_addresses', [])
        if len(set(ip_addresses)) > 5:  # Multiple IPs suggest VPN/proxy usage
            opsec_score += 0.2
            indicators.append('Multiple IP addresses')
        
        return {
            'opsec_score': min(opsec_score, 1.0),
            'security_indicators': indicators,
            'security_level': 'high' if opsec_score > 0.7 else 'medium' if opsec_score > 0.4 else 'low'
        }
    
    async def _build_activity_timeline(self, persona: ThreatPersona, entity_data: Dict[str, Any]):
        """Build chronological activity timeline"""
        timeline_events = []
        
        # Collect timestamped events
        for tx in entity_data.get('transactions', []):
            if tx.get('timestamp'):
                timeline_events.append({
                    'timestamp': tx['timestamp'],
                    'event_type': 'transaction',
                    'description': f"Transaction of {tx.get('amount', 0)} to {tx.get('address', 'unknown')}",
                    'significance': 'medium'
                })
        
        for post in entity_data.get('forum_posts', []):
            if post.get('timestamp'):
                timeline_events.append({
                    'timestamp': post['timestamp'],
                    'event_type': 'communication',
                    'description': f"Forum post: {post.get('content', '')[:100]}...",
                    'significance': 'low'
                })
        
        # Sort by timestamp
        timeline_events.sort(key=lambda x: x['timestamp'])
        
        persona.activity_timeline = timeline_events[-20:]  # Keep last 20 events
        
        # Set first and last activity
        if timeline_events:
            persona.first_activity = datetime.fromisoformat(timeline_events[0]['timestamp'].replace('Z', '+00:00'))
            persona.last_activity = datetime.fromisoformat(timeline_events[-1]['timestamp'].replace('Z', '+00:00'))
    
    async def _assess_threat_level(self, persona: ThreatPersona):
        """Assess overall threat level"""
        threat_score = 0.0
        
        # Cryptocurrency involvement
        if persona.crypto_wallets:
            threat_score += 0.2
        
        # Dark web presence
        if persona.onion_profiles:
            threat_score += 0.3
        
        # Technical sophistication
        if persona.linguistic_profile.get('technical_terminology'):
            threat_score += 0.2
        
        # Operational security
        opsec_score = persona.activity_patterns.get('operational_security', {}).get('opsec_score', 0)
        threat_score += opsec_score * 0.3
        
        # Communication patterns indicating malicious intent
        if persona.linguistic_profile.get('topic_preferences'):
            malicious_topics = ['hacking', 'fraud', 'weapons', 'drugs']
            if any(topic in malicious_topics for topic in persona.linguistic_profile['topic_preferences']):
                threat_score += 0.4
        
        # Determine threat level
        if threat_score >= 0.8:
            persona.threat_level = ThreatLevel.CRITICAL
        elif threat_score >= 0.6:
            persona.threat_level = ThreatLevel.HIGH
        elif threat_score >= 0.4:
            persona.threat_level = ThreatLevel.MEDIUM
        else:
            persona.threat_level = ThreatLevel.LOW
    
    async def _calculate_confidence_score(self, persona: ThreatPersona):
        """Calculate confidence in persona assessment"""
        confidence_factors = []
        
        # Number of data sources
        total_attributes = (
            len(persona.crypto_wallets) + len(persona.email_addresses) +
            len(persona.usernames) + len(persona.telegram_handles)
        )
        
        if total_attributes >= 5:
            confidence_factors.append(0.3)
        elif total_attributes >= 3:
            confidence_factors.append(0.2)
        else:
            confidence_factors.append(0.1)
        
        # Linguistic analysis completeness
        if persona.linguistic_profile:
            confidence_factors.append(0.2)
        
        # Behavioral analysis completeness
        if persona.transaction_patterns:
            confidence_factors.append(0.2)
        
        # Timeline completeness
        if len(persona.activity_timeline) > 5:
            confidence_factors.append(0.2)
        
        # Correlation strength
        if persona.correlation_leads:
            confidence_factors.append(0.1)
        
        persona.confidence_score = min(sum(confidence_factors), 1.0)
    
    async def _generate_intelligence_summary(self, persona: ThreatPersona):
        """Generate actionable intelligence summary"""
        # Attack vectors
        if persona.crypto_wallets:
            persona.attack_vectors.append('Cryptocurrency-based operations')
        if persona.onion_profiles:
            persona.attack_vectors.append('Dark web activities')
        if persona.telegram_handles:
            persona.attack_vectors.append('Encrypted communications')
        
        # Recommended actions
        persona.recommended_actions = [
            'Monitor all associated cryptocurrency addresses',
            'Track communication patterns across platforms',
            'Cross-reference with known threat databases',
            'Analyze transaction patterns for money laundering indicators'
        ]
        
        if persona.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            persona.recommended_actions.extend([
                'Escalate to specialized cybercrime unit',
                'Consider law enforcement coordination',
                'Implement enhanced monitoring protocols'
            ])
        
        # Intelligence gaps
        persona.intelligence_gaps = []
        if not persona.crypto_wallets:
            persona.intelligence_gaps.append('Cryptocurrency wallet associations')
        if not persona.linguistic_profile:
            persona.intelligence_gaps.append('Communication pattern analysis')
        if not persona.activity_timeline:
            persona.intelligence_gaps.append('Temporal activity patterns')
        
        # Risk factors
        persona.risk_factors = []
        if persona.activity_patterns.get('operational_security', {}).get('opsec_score', 0) > 0.7:
            persona.risk_factors.append('High operational security suggests sophistication')
        if persona.linguistic_profile.get('topic_preferences'):
            malicious_topics = set(persona.linguistic_profile['topic_preferences']) & {'hacking', 'fraud', 'weapons'}
            if malicious_topics:
                persona.risk_factors.append(f'Interest in malicious activities: {", ".join(malicious_topics)}')

    async def generate_persona_report(self, persona_id: str) -> Dict[str, Any]:
        """Generate comprehensive persona report"""
        if persona_id not in self.personas:
            return {'error': 'Persona not found'}
        
        persona = self.personas[persona_id]
        
        report = {
            'persona_overview': {
                'persona_id': persona.persona_id,
                'primary_identifier': persona.primary_identifier,
                'threat_level': persona.threat_level.value,
                'confidence_score': persona.confidence_score,
                'first_activity': persona.first_activity.isoformat() if persona.first_activity else None,
                'last_activity': persona.last_activity.isoformat() if persona.last_activity else None
            },
            'digital_footprint': {
                'crypto_wallets': [attr.value for attr in persona.crypto_wallets],
                'email_addresses': [attr.value for attr in persona.email_addresses],
                'usernames': [attr.value for attr in persona.usernames],
                'telegram_handles': [attr.value for attr in persona.telegram_handles]
            },
            'behavioral_analysis': {
                'linguistic_profile': persona.linguistic_profile,
                'activity_patterns': persona.activity_patterns,
                'transaction_patterns': persona.transaction_patterns
            },
            'threat_assessment': {
                'attack_vectors': persona.attack_vectors,
                'risk_factors': persona.risk_factors,
                'capability_assessment': persona.capability_assessment,
                'modus_operandi': persona.modus_operandi
            },
            'investigative_leads': {
                'recommended_actions': persona.recommended_actions,
                'intelligence_gaps': persona.intelligence_gaps,
                'correlation_leads': persona.correlation_leads
            },
            'activity_timeline': persona.activity_timeline[-10:],  # Last 10 events
            'report_metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'confidence_level': 'HIGH' if persona.confidence_score > 0.8 else 'MEDIUM' if persona.confidence_score > 0.6 else 'LOW',
                'data_sources_count': len(set(
                    source for attr_list in [persona.crypto_wallets, persona.email_addresses, persona.usernames, persona.telegram_handles]
                    for attr in attr_list
                    for source in attr.sources
                ))
            }
        }
        
        return report

# Example usage and API integration
async def generate_demo_persona():
    """Generate a demo threat persona for testing"""
    generator = ThreatPersonaGenerator()
    
    demo_entity_data = {
        'primary_id': 'cryptoking99@protonmail.com',
        'crypto_addresses': ['1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'],
        'email_addresses': ['cryptoking99@protonmail.com', 'darktrader@tutanota.com'],
        'usernames': ['cryptoking99', 'dark_trader_001'],
        'telegram_handles': ['@cryptoking99_official'],
        'forum_posts': [
            {
                'content': 'Looking to sell high-quality cryptocurrency mixing services. Privacy guaranteed. Bitcoin and Monero supported.',
                'timestamp': '2024-01-15T10:30:00Z'
            }
        ],
        'transactions': [
            {
                'amount': 2.5,
                'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                'timestamp': '2024-01-15T11:00:00Z'
            }
        ]
    }
    
    persona = await generator.generate_persona(demo_entity_data)
    report = await generator.generate_persona_report(persona.persona_id)
    
    return report

if __name__ == "__main__":
    print("👤 Threat Persona Graph Generator")
    print("AI-powered threat actor profiling system ready!")
    
    # Demo execution
    # import asyncio
    # demo_report = asyncio.run(generate_demo_persona())
    # print(json.dumps(demo_report, indent=2))