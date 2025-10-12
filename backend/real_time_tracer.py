"""
⚡ NTRO-CryptoForensics: Real-Time Leak-to-Blockchain Tracing
============================================================

Advanced monitoring system that:
- Monitors fresh leaks/dumps from Telegram, dark-web, paste sites
- Instantly extracts cryptocurrency addresses from new content
- Cross-checks addresses against blockchain activity in real-time
- Generates immediate alerts for suspicious wallet connections
- Tracks address propagation across multiple leak sources

Provides real-time threat intelligence for cryptocurrency forensics.
"""

import asyncio
import aiohttp
import re
import json
from typing import Dict, List, Optional, Set, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib
import logging
from enum import Enum

import websockets
from motor.motor_asyncio import AsyncIOMotorDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class LeakSource(Enum):
    TELEGRAM = "telegram"
    PASTE_SITE = "paste_site"
    DARK_WEB = "dark_web"
    FORUM = "forum"
    SOCIAL_MEDIA = "social_media"
    DATA_BREACH = "data_breach"

@dataclass
class CryptoAddress:
    """Cryptocurrency address with metadata"""
    address: str
    currency_type: str  # 'bitcoin', 'ethereum', 'monero', etc.
    first_seen: datetime
    confidence_score: float
    validation_status: str  # 'valid', 'invalid', 'pending'
    
@dataclass
class LeakEvent:
    """Represents a leak or dump event"""
    event_id: str
    source: LeakSource
    source_url: str
    title: str
    content: str
    timestamp: datetime
    crypto_addresses: List[CryptoAddress] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)
    usernames: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BlockchainAlert:
    """Alert for suspicious blockchain activity"""
    alert_id: str
    severity: AlertSeverity
    address: str
    alert_type: str
    description: str
    timestamp: datetime
    evidence: List[str] = field(default_factory=list)
    correlated_leaks: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    investigation_priority: int = 5  # 1-10 scale

@dataclass
class TraceResult:
    """Result of leak-to-blockchain trace"""
    trace_id: str
    leak_event: LeakEvent
    blockchain_matches: List[Dict] = field(default_factory=list)
    correlation_score: float = 0.0
    timeline_analysis: Dict[str, Any] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    generated_alerts: List[BlockchainAlert] = field(default_factory=list)

class CryptoAddressExtractor:
    """Advanced cryptocurrency address extraction and validation"""
    
    def __init__(self):
        # Regex patterns for different cryptocurrencies
        self.patterns = {
            'bitcoin': [
                r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',  # Legacy addresses
                r'\bbc1[a-z0-9]{39,59}\b',  # Bech32 addresses
            ],
            'ethereum': [
                r'0x[a-fA-F0-9]{40}\b',  # Ethereum addresses
            ],
            'monero': [
                r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b',  # Monero addresses
            ],
            'litecoin': [
                r'\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b',  # Litecoin addresses
            ],
            'dogecoin': [
                r'\bD{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}\b',  # Dogecoin addresses
            ],
            'ripple': [
                r'\br[a-zA-Z0-9]{24,34}\b',  # Ripple addresses
            ]
        }
        
        # Compiled patterns for performance
        self.compiled_patterns = {
            currency: [re.compile(pattern) for pattern in patterns]
            for currency, patterns in self.patterns.items()
        }
    
    def extract_addresses(self, text: str) -> List[CryptoAddress]:
        """Extract all cryptocurrency addresses from text"""
        addresses = []
        current_time = datetime.utcnow()
        
        for currency, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.findall(text)
                for match in matches:
                    # Validate address format
                    if self._validate_address_format(match, currency):
                        addr = CryptoAddress(
                            address=match,
                            currency_type=currency,
                            first_seen=current_time,
                            confidence_score=self._calculate_confidence(match, currency, text),
                            validation_status='pending'
                        )
                        addresses.append(addr)
        
        # Remove duplicates
        unique_addresses = {}
        for addr in addresses:
            if addr.address not in unique_addresses:
                unique_addresses[addr.address] = addr
            else:
                # Keep the one with higher confidence
                if addr.confidence_score > unique_addresses[addr.address].confidence_score:
                    unique_addresses[addr.address] = addr
        
        return list(unique_addresses.values())
    
    def _validate_address_format(self, address: str, currency: str) -> bool:
        """Basic format validation for cryptocurrency addresses"""
        if currency == 'bitcoin':
            return len(address) >= 26 and len(address) <= 62
        elif currency == 'ethereum':
            return len(address) == 42 and address.startswith('0x')
        elif currency == 'monero':
            return len(address) == 95 and address.startswith('4')
        # Add more validation as needed
        return True
    
    def _calculate_confidence(self, address: str, currency: str, context: str) -> float:
        """Calculate confidence score for extracted address"""
        confidence = 0.5  # Base confidence
        
        # Context-based confidence boosting
        context_lower = context.lower()
        
        # High confidence indicators
        high_confidence_terms = [
            'wallet', 'address', 'send to', 'receive at', 'payment',
            'transaction', 'transfer', 'deposit', 'withdraw'
        ]
        
        medium_confidence_terms = [
            'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'coin'
        ]
        
        # Boost confidence based on context
        for term in high_confidence_terms:
            if term in context_lower:
                confidence += 0.2
                break
        
        for term in medium_confidence_terms:
            if term in context_lower:
                confidence += 0.1
                break
        
        # Reduce confidence for suspicious contexts
        suspicious_terms = ['example', 'test', 'demo', 'sample']
        for term in suspicious_terms:
            if term in context_lower:
                confidence -= 0.3
                break
        
        # Length-based confidence (properly formatted addresses)
        if currency == 'bitcoin' and 26 <= len(address) <= 35:
            confidence += 0.1
        elif currency == 'ethereum' and len(address) == 42:
            confidence += 0.1
        
        return max(0.1, min(1.0, confidence))

class LeakMonitor:
    """Monitors various sources for fresh leaks and dumps"""
    
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.db = mongo_db
        self.extractor = CryptoAddressExtractor()
        self.monitored_sources = {}
        self.alert_callbacks: List[Callable] = []
        self.is_monitoring = False
        
        # Initialize monitoring sources
        self._initialize_sources()
    
    def _initialize_sources(self):
        """Initialize monitoring sources"""
        self.monitored_sources = {
            # Telegram channels
            'telegram_crypto_leaks': {
                'source': LeakSource.TELEGRAM,
                'url': 'https://t.me/s/cryptoleaks',
                'check_interval': 300,  # 5 minutes
                'last_checked': None
            },
            'telegram_darknet_dumps': {
                'source': LeakSource.TELEGRAM,
                'url': 'https://t.me/s/darknetdumps',
                'check_interval': 600,  # 10 minutes
                'last_checked': None
            },
            
            # Paste sites
            'pastebin_recent': {
                'source': LeakSource.PASTE_SITE,
                'url': 'https://pastebin.com/archive',
                'check_interval': 180,  # 3 minutes
                'last_checked': None
            },
            'paste_ubuntu': {
                'source': LeakSource.PASTE_SITE,
                'url': 'https://paste.ubuntu.com/',
                'check_interval': 300,  # 5 minutes
                'last_checked': None
            },
            
            # Dark web monitoring
            'darknet_live': {
                'source': LeakSource.DARK_WEB,
                'url': 'https://darknetlive.com/',
                'check_interval': 900,  # 15 minutes
                'last_checked': None
            },
            
            # Forums
            'raidforums_leaks': {
                'source': LeakSource.FORUM,
                'url': 'https://raidforums.com/forumdisplay.php?fid=18',
                'check_interval': 1800,  # 30 minutes
                'last_checked': None
            }
        }
    
    async def start_monitoring(self):
        """Start monitoring all sources"""
        if self.is_monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        logger.info("⚡ Starting real-time leak monitoring...")
        
        # Start monitoring tasks for each source
        tasks = []
        for source_id, config in self.monitored_sources.items():
            task = asyncio.create_task(self._monitor_source(source_id, config))
            tasks.append(task)
        
        # Wait for all monitoring tasks
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        logger.info("Stopping leak monitoring...")
    
    async def _monitor_source(self, source_id: str, config: Dict):
        """Monitor a specific source for new content"""
        while self.is_monitoring:
            try:
                current_time = datetime.utcnow()
                last_checked = config.get('last_checked')
                
                # Check if it's time to monitor this source
                if (last_checked is None or 
                    (current_time - last_checked).total_seconds() >= config['check_interval']):
                    
                    logger.info(f"🔍 Checking {source_id} for new leaks...")
                    
                    # Fetch and analyze content
                    leak_events = await self._fetch_and_analyze(source_id, config)
                    
                    # Process any discovered leak events
                    for event in leak_events:
                        await self._process_leak_event(event)
                    
                    config['last_checked'] = current_time
                
                # Sleep briefly before next check
                await asyncio.sleep(30)  # Check every 30 seconds for timing
                
            except Exception as e:
                logger.error(f"Error monitoring {source_id}: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _fetch_and_analyze(self, source_id: str, config: Dict) -> List[LeakEvent]:
        """Fetch content from source and analyze for crypto addresses"""
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(config['url']) as response:
                    if response.status == 200:
                        content = await response.text()
                        return await self._analyze_content_for_leaks(content, config)
                    else:
                        logger.warning(f"Failed to fetch {source_id}: HTTP {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching {source_id}: {e}")
            return []
    
    async def _analyze_content_for_leaks(self, content: str, config: Dict) -> List[LeakEvent]:
        """Analyze content for potential leak events"""
        leak_events = []
        
        # Extract crypto addresses
        crypto_addresses = self.extractor.extract_addresses(content)
        
        # Only create event if crypto addresses are found
        if crypto_addresses:
            # Extract other relevant information
            emails = self._extract_emails(content)
            usernames = self._extract_usernames(content)
            
            # Create leak event
            event = LeakEvent(
                event_id=f"leak_{hashlib.md5(content[:1000].encode()).hexdigest()[:8]}",
                source=config['source'],
                source_url=config['url'],
                title=f"Crypto addresses detected in {config['source'].value}",
                content=content[:2000],  # Store first 2000 chars
                timestamp=datetime.utcnow(),
                crypto_addresses=crypto_addresses,
                emails=emails,
                usernames=usernames,
                metadata={
                    'content_length': len(content),
                    'address_count': len(crypto_addresses),
                    'confidence_scores': [addr.confidence_score for addr in crypto_addresses]
                }
            )
            
            leak_events.append(event)
            logger.info(f"💰 Found {len(crypto_addresses)} crypto addresses in {config['source'].value}")
        
        return leak_events
    
    def _extract_emails(self, content: str) -> List[str]:
        """Extract email addresses from content"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(email_pattern, content)))
    
    def _extract_usernames(self, content: str) -> List[str]:
        """Extract usernames from content"""
        username_patterns = [
            r'@[a-zA-Z0-9_]{3,20}\b',  # Social media handles
            r'\busername[:\s]+([a-zA-Z0-9_]{3,20})',  # Explicit username labels
            r'\buser[:\s]+([a-zA-Z0-9_]{3,20})',  # User labels
        ]
        
        usernames = []
        for pattern in username_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            usernames.extend(matches)
        
        return list(set(usernames))
    
    async def _process_leak_event(self, event: LeakEvent):
        """Process a detected leak event"""
        logger.info(f"⚡ Processing leak event: {event.event_id}")
        
        # Store leak event in database
        await self._store_leak_event(event)
        
        # Trigger real-time blockchain tracing
        for callback in self.alert_callbacks:
            try:
                await callback(event)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")
    
    async def _store_leak_event(self, event: LeakEvent):
        """Store leak event in database"""
        try:
            event_doc = {
                'event_id': event.event_id,
                'source': event.source.value,
                'source_url': event.source_url,
                'title': event.title,
                'content': event.content,
                'timestamp': event.timestamp,
                'crypto_addresses': [
                    {
                        'address': addr.address,
                        'currency_type': addr.currency_type,
                        'confidence_score': addr.confidence_score,
                        'validation_status': addr.validation_status
                    }
                    for addr in event.crypto_addresses
                ],
                'emails': event.emails,
                'usernames': event.usernames,
                'metadata': event.metadata
            }
            
            await self.db.leak_events.insert_one(event_doc)
            logger.info(f"💾 Stored leak event: {event.event_id}")
            
        except Exception as e:
            logger.error(f"Error storing leak event: {e}")
    
    def add_alert_callback(self, callback: Callable):
        """Add callback for leak alerts"""
        self.alert_callbacks.append(callback)

class BlockchainTracer:
    """Real-time blockchain tracing and correlation"""
    
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.db = mongo_db
        self.active_traces: Dict[str, TraceResult] = {}
        self.blockchain_apis = self._initialize_blockchain_apis()
        
    def _initialize_blockchain_apis(self) -> Dict[str, str]:
        """Initialize blockchain API endpoints"""
        return {
            'blockchair': 'https://api.blockchair.com',
            'blockchain_info': 'https://blockchain.info/rawaddr',
            'etherscan': 'https://api.etherscan.io/api',
            'blockstream': 'https://blockstream.info/api'
        }
    
    async def trace_addresses(self, leak_event: LeakEvent) -> TraceResult:
        """Trace cryptocurrency addresses from leak event"""
        trace_id = f"trace_{leak_event.event_id}_{int(datetime.utcnow().timestamp())}"
        
        trace_result = TraceResult(
            trace_id=trace_id,
            leak_event=leak_event
        )
        
        logger.info(f"🔗 Starting blockchain trace: {trace_id}")
        
        # Trace each address
        for crypto_addr in leak_event.crypto_addresses:
            blockchain_data = await self._query_blockchain_apis(crypto_addr)
            
            if blockchain_data:
                trace_result.blockchain_matches.append({
                    'address': crypto_addr.address,
                    'currency': crypto_addr.currency_type,
                    'blockchain_data': blockchain_data,
                    'suspicious_indicators': self._analyze_blockchain_data(blockchain_data)
                })
        
        # Calculate correlation score
        trace_result.correlation_score = self._calculate_correlation_score(trace_result)
        
        # Perform timeline analysis
        trace_result.timeline_analysis = await self._analyze_timeline(trace_result)
        
        # Assess risk
        trace_result.risk_assessment = self._assess_risk(trace_result)
        
        # Generate alerts if necessary
        trace_result.generated_alerts = await self._generate_alerts(trace_result)
        
        # Store trace result
        self.active_traces[trace_id] = trace_result
        await self._store_trace_result(trace_result)
        
        logger.info(f"✅ Completed blockchain trace: {trace_id} (correlation: {trace_result.correlation_score:.2f})")
        return trace_result
    
    async def _query_blockchain_apis(self, crypto_addr: CryptoAddress) -> Optional[Dict]:
        """Query blockchain APIs for address information"""
        try:
            if crypto_addr.currency_type == 'bitcoin':
                return await self._query_bitcoin_apis(crypto_addr.address)
            elif crypto_addr.currency_type == 'ethereum':
                return await self._query_ethereum_apis(crypto_addr.address)
            # Add more currency support as needed
            
        except Exception as e:
            logger.error(f"Error querying blockchain APIs for {crypto_addr.address}: {e}")
            
        return None
    
    async def _query_bitcoin_apis(self, address: str) -> Optional[Dict]:
        """Query Bitcoin blockchain APIs"""
        try:
            # Use Blockchair API (free tier)
            url = f"{self.blockchain_apis['blockchair']}/bitcoin/dashboards/address/{address}"
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'data' in data and address in data['data']:
                            addr_data = data['data'][address]
                            
                            return {
                                'balance': addr_data.get('address', {}).get('balance', 0),
                                'transaction_count': addr_data.get('address', {}).get('transaction_count', 0),
                                'first_seen': addr_data.get('address', {}).get('first_seen_receiving'),
                                'last_seen': addr_data.get('address', {}).get('last_seen_spending'),
                                'total_received': addr_data.get('address', {}).get('received', 0),
                                'total_sent': addr_data.get('address', {}).get('spent', 0),
                                'api_source': 'blockchair'
                            }
                            
        except Exception as e:
            logger.error(f"Error querying Bitcoin APIs: {e}")
            
        return None
    
    async def _query_ethereum_apis(self, address: str) -> Optional[Dict]:
        """Query Ethereum blockchain APIs"""
        # Placeholder for Ethereum API queries
        # Would implement actual Etherscan API calls here
        return {
            'balance': 0,
            'transaction_count': 0,
            'api_source': 'placeholder'
        }
    
    def _analyze_blockchain_data(self, blockchain_data: Dict) -> List[str]:
        """Analyze blockchain data for suspicious indicators"""
        indicators = []
        
        # High transaction volume
        tx_count = blockchain_data.get('transaction_count', 0)
        if tx_count > 100:
            indicators.append(f"High transaction activity ({tx_count} transactions)")
        
        # Large balance
        balance = blockchain_data.get('balance', 0)
        if balance > 100000000:  # > 1 BTC in satoshis
            indicators.append(f"Large balance ({balance / 100000000:.2f} BTC)")
        
        # Recent activity
        last_seen = blockchain_data.get('last_seen')
        if last_seen:
            try:
                last_activity = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                hours_since = (datetime.utcnow() - last_activity).total_seconds() / 3600
                if hours_since < 24:
                    indicators.append("Recent activity (within 24 hours)")
            except:
                pass
        
        # High throughput
        total_received = blockchain_data.get('total_received', 0)
        total_sent = blockchain_data.get('total_sent', 0)
        
        if total_received > 1000000000:  # > 10 BTC
            indicators.append(f"High total received ({total_received / 100000000:.2f} BTC)")
        
        if total_sent > 1000000000:  # > 10 BTC
            indicators.append(f"High total sent ({total_sent / 100000000:.2f} BTC)")
        
        return indicators
    
    def _calculate_correlation_score(self, trace_result: TraceResult) -> float:
        """Calculate correlation score between leak and blockchain activity"""
        score = 0.0
        
        # Base score for having blockchain matches
        if trace_result.blockchain_matches:
            score += 0.3
        
        # Score based on suspicious indicators
        total_indicators = sum(
            len(match['suspicious_indicators']) 
            for match in trace_result.blockchain_matches
        )
        score += min(total_indicators * 0.1, 0.4)
        
        # Score based on timing correlation
        leak_time = trace_result.leak_event.timestamp
        for match in trace_result.blockchain_matches:
            last_seen = match['blockchain_data'].get('last_seen')
            if last_seen:
                try:
                    activity_time = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                    time_diff = abs((leak_time - activity_time).total_seconds() / 3600)
                    
                    # Higher score for recent correlation
                    if time_diff < 24:
                        score += 0.2
                    elif time_diff < 168:  # Within a week
                        score += 0.1
                except:
                    pass
        
        # Score based on address confidence
        avg_confidence = sum(
            addr.confidence_score for addr in trace_result.leak_event.crypto_addresses
        ) / max(len(trace_result.leak_event.crypto_addresses), 1)
        score += avg_confidence * 0.2
        
        return min(score, 1.0)
    
    async def _analyze_timeline(self, trace_result: TraceResult) -> Dict[str, Any]:
        """Analyze timeline correlation between leak and blockchain activity"""
        timeline = {
            'leak_timestamp': trace_result.leak_event.timestamp.isoformat(),
            'blockchain_activities': [],
            'correlation_windows': []
        }
        
        leak_time = trace_result.leak_event.timestamp
        
        for match in trace_result.blockchain_matches:
            blockchain_data = match['blockchain_data']
            
            # Add blockchain activity timestamps
            for time_field in ['first_seen', 'last_seen']:
                if blockchain_data.get(time_field):
                    try:
                        activity_time = datetime.fromisoformat(
                            blockchain_data[time_field].replace('Z', '+00:00')
                        )
                        
                        timeline['blockchain_activities'].append({
                            'address': match['address'],
                            'activity_type': time_field,
                            'timestamp': activity_time.isoformat(),
                            'time_from_leak': (activity_time - leak_time).total_seconds() / 3600
                        })
                    except:
                        pass
        
        # Identify correlation windows
        for activity in timeline['blockchain_activities']:
            time_diff = abs(activity['time_from_leak'])
            if time_diff < 24:
                timeline['correlation_windows'].append({
                    'window': '24_hours',
                    'activity': activity,
                    'significance': 'high'
                })
            elif time_diff < 168:
                timeline['correlation_windows'].append({
                    'window': '1_week',
                    'activity': activity,
                    'significance': 'medium'
                })
        
        return timeline
    
    def _assess_risk(self, trace_result: TraceResult) -> Dict[str, Any]:
        """Assess overall risk level of the trace"""
        risk_factors = []
        risk_score = 0.0
        
        # High correlation score
        if trace_result.correlation_score > 0.7:
            risk_factors.append("High correlation between leak and blockchain activity")
            risk_score += 0.3
        
        # Multiple addresses
        if len(trace_result.leak_event.crypto_addresses) > 3:
            risk_factors.append("Multiple cryptocurrency addresses in single leak")
            risk_score += 0.2
        
        # Suspicious blockchain indicators
        total_indicators = sum(
            len(match['suspicious_indicators']) 
            for match in trace_result.blockchain_matches
        )
        if total_indicators > 2:
            risk_factors.append(f"Multiple suspicious blockchain indicators ({total_indicators})")
            risk_score += 0.2
        
        # Recent timeline correlation
        recent_activities = [
            activity for activity in trace_result.timeline_analysis.get('blockchain_activities', [])
            if abs(activity['time_from_leak']) < 24
        ]
        if recent_activities:
            risk_factors.append("Blockchain activity within 24 hours of leak")
            risk_score += 0.3
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = "CRITICAL"
        elif risk_score >= 0.6:
            risk_level = "HIGH"
        elif risk_score >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'requires_investigation': risk_score >= 0.6
        }
    
    async def _generate_alerts(self, trace_result: TraceResult) -> List[BlockchainAlert]:
        """Generate alerts based on trace results"""
        alerts = []
        
        # High correlation alert
        if trace_result.correlation_score > 0.7:
            alert = BlockchainAlert(
                alert_id=f"alert_{trace_result.trace_id}_correlation",
                severity=AlertSeverity.HIGH,
                address=trace_result.leak_event.crypto_addresses[0].address if trace_result.leak_event.crypto_addresses else "multiple",
                alert_type="high_correlation",
                description=f"High correlation ({trace_result.correlation_score:.2f}) between leak event and blockchain activity",
                timestamp=datetime.utcnow(),
                evidence=[
                    f"Leak source: {trace_result.leak_event.source.value}",
                    f"Addresses found: {len(trace_result.leak_event.crypto_addresses)}",
                    f"Blockchain matches: {len(trace_result.blockchain_matches)}"
                ],
                correlated_leaks=[trace_result.leak_event.event_id],
                recommended_actions=[
                    "Monitor all associated addresses for future activity",
                    "Cross-reference with known threat databases",
                    "Investigate source of leaked information"
                ],
                investigation_priority=8
            )
            alerts.append(alert)
        
        # Suspicious blockchain activity alert
        for match in trace_result.blockchain_matches:
            if len(match['suspicious_indicators']) > 2:
                alert = BlockchainAlert(
                    alert_id=f"alert_{trace_result.trace_id}_{match['address'][:8]}",
                    severity=AlertSeverity.MEDIUM,
                    address=match['address'],
                    alert_type="suspicious_activity",
                    description=f"Suspicious blockchain activity detected for address {match['address']}",
                    timestamp=datetime.utcnow(),
                    evidence=match['suspicious_indicators'],
                    correlated_leaks=[trace_result.leak_event.event_id],
                    recommended_actions=[
                        "Monitor address for future transactions",
                        "Check for mixer/tumbler usage",
                        "Investigate transaction patterns"
                    ],
                    investigation_priority=6
                )
                alerts.append(alert)
        
        return alerts
    
    async def _store_trace_result(self, trace_result: TraceResult):
        """Store trace result in database"""
        try:
            trace_doc = {
                'trace_id': trace_result.trace_id,
                'leak_event_id': trace_result.leak_event.event_id,
                'blockchain_matches': trace_result.blockchain_matches,
                'correlation_score': trace_result.correlation_score,
                'timeline_analysis': trace_result.timeline_analysis,
                'risk_assessment': trace_result.risk_assessment,
                'generated_alerts': [
                    {
                        'alert_id': alert.alert_id,
                        'severity': alert.severity.value,
                        'alert_type': alert.alert_type,
                        'description': alert.description,
                        'investigation_priority': alert.investigation_priority
                    }
                    for alert in trace_result.generated_alerts
                ],
                'timestamp': datetime.utcnow()
            }
            
            await self.db.trace_results.insert_one(trace_doc)
            logger.info(f"💾 Stored trace result: {trace_result.trace_id}")
            
        except Exception as e:
            logger.error(f"Error storing trace result: {e}")

class RealTimeLeakTracer:
    """Main orchestrator for real-time leak-to-blockchain tracing"""
    
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.db = mongo_db
        self.leak_monitor = LeakMonitor(mongo_db)
        self.blockchain_tracer = BlockchainTracer(mongo_db)
        self.active_alerts: List[BlockchainAlert] = []
        
        # Register leak event callback
        self.leak_monitor.add_alert_callback(self._handle_leak_event)
    
    async def start_real_time_tracing(self):
        """Start the complete real-time tracing system"""
        logger.info("🚀 Starting real-time leak-to-blockchain tracing system...")
        
        # Start leak monitoring
        await self.leak_monitor.start_monitoring()
    
    async def _handle_leak_event(self, leak_event: LeakEvent):
        """Handle detected leak event with blockchain tracing"""
        logger.info(f"⚡ Processing leak event for blockchain tracing: {leak_event.event_id}")
        
        try:
            # Perform blockchain tracing
            trace_result = await self.blockchain_tracer.trace_addresses(leak_event)
            
            # Handle generated alerts
            for alert in trace_result.generated_alerts:
                self.active_alerts.append(alert)
                await self._handle_alert(alert)
            
            logger.info(f"✅ Completed tracing for leak event: {leak_event.event_id}")
            
        except Exception as e:
            logger.error(f"Error processing leak event {leak_event.event_id}: {e}")
    
    async def _handle_alert(self, alert: BlockchainAlert):
        """Handle generated alerts"""
        logger.warning(f"🚨 {alert.severity.value} ALERT: {alert.description}")
        
        # Store alert in database
        await self._store_alert(alert)
        
        # High priority alerts get additional processing
        if alert.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]:
            await self._escalate_alert(alert)
    
    async def _store_alert(self, alert: BlockchainAlert):
        """Store alert in database"""
        try:
            alert_doc = {
                'alert_id': alert.alert_id,
                'severity': alert.severity.value,
                'address': alert.address,
                'alert_type': alert.alert_type,
                'description': alert.description,
                'timestamp': alert.timestamp,
                'evidence': alert.evidence,
                'correlated_leaks': alert.correlated_leaks,
                'recommended_actions': alert.recommended_actions,
                'investigation_priority': alert.investigation_priority,
                'status': 'active'
            }
            
            await self.db.blockchain_alerts.insert_one(alert_doc)
            
        except Exception as e:
            logger.error(f"Error storing alert: {e}")
    
    async def _escalate_alert(self, alert: BlockchainAlert):
        """Escalate high-priority alerts"""
        logger.critical(f"🚨 ESCALATING {alert.severity.value} ALERT: {alert.alert_id}")
        
        # Additional escalation logic would go here
        # - Email notifications
        # - Webhook calls
        # - Integration with SIEM systems
        # - Automatic investigation triggers
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get real-time tracing system status"""
        return {
            'monitoring_status': 'ACTIVE' if self.leak_monitor.is_monitoring else 'INACTIVE',
            'monitored_sources': len(self.leak_monitor.monitored_sources),
            'active_traces': len(self.blockchain_tracer.active_traces),
            'active_alerts': len(self.active_alerts),
            'critical_alerts': len([a for a in self.active_alerts if a.severity == AlertSeverity.CRITICAL]),
            'high_alerts': len([a for a in self.active_alerts if a.severity == AlertSeverity.HIGH]),
            'system_capabilities': [
                'Real-time leak monitoring',
                'Cryptocurrency address extraction',
                'Blockchain correlation analysis',
                'Timeline analysis',
                'Risk assessment',
                'Automated alerting'
            ]
        }

# Example usage
if __name__ == "__main__":
    print("⚡ Real-Time Leak-to-Blockchain Tracing System")
    print("Advanced threat intelligence for cryptocurrency forensics!")
    
    # Demo execution would go here
    # async def demo():
    #     tracer = RealTimeLeakTracer(mongo_db)
    #     await tracer.start_real_time_tracing()
    
    # asyncio.run(demo())