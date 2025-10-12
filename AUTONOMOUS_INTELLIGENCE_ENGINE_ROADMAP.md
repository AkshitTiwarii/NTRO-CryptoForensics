# 🧠 Autonomous Intelligence Correlation Engine - Implementation Roadmap

## 🎯 Vision Statement
**"From raw internet noise to actionable intelligence — automatically."**

Position: **Autonomous Multi-Layer OSINT + Blockchain Fusion Engine** that learns and adapts on its own.

---

## ✅ What You Already Have (Don't Rebuild)

### Core Infrastructure ✅
- ✅ MongoDB database with crypto addresses
- ✅ FastAPI backend with JWT authentication
- ✅ React frontend with responsive UI
- ✅ Multi-source scraping (surface web)
- ✅ Tor scraper ready (dark web)
- ✅ Celery + Redis task queue
- ✅ ML categorizer (11 categories)
- ✅ Blockchair API integration (41 blockchains)
- ✅ Risk scoring (0-100)
- ✅ Pattern analysis (round numbers, rapid txs, large transfers)
- ✅ Basic network graph visualization
- ✅ CSV/JSON export
- ✅ Watchlist system
- ✅ Seed manager with 11+ sources

---

## 🚀 NEW FEATURES TO BUILD (In Priority Order)

### 🔴 **PHASE 1: Multi-Modal Data Fusion** (Week 1-2)

#### 1.1 Graph Database Integration (Neo4j)
**Purpose**: Link blockchain addresses → emails → usernames → forum profiles → Telegram handles

**Implementation**:

```bash
# Install Neo4j
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/cryptoforensics \
  neo4j:latest
```

**New File**: `backend/graph_db.py`
```python
from neo4j import GraphDatabase
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CryptoGraphDB:
    """Neo4j graph database for entity correlation"""
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="cryptoforensics"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("✅ Neo4j connection established")
    
    def create_address_node(self, address_data: Dict):
        """Create cryptocurrency address node"""
        with self.driver.session() as session:
            session.run("""
                MERGE (a:CryptoAddress {address: $address})
                SET a.crypto_type = $crypto_type,
                    a.category = $category,
                    a.risk_score = $risk_score,
                    a.balance = $balance,
                    a.first_seen = $first_seen,
                    a.last_updated = datetime()
                """,
                address=address_data["address"],
                crypto_type=address_data.get("crypto_type", "unknown"),
                category=address_data.get("category", "unknown"),
                risk_score=address_data.get("risk_score", 0),
                balance=address_data.get("balance", 0.0),
                first_seen=address_data.get("first_seen")
            )
    
    def link_address_to_email(self, address: str, email: str, confidence: float = 0.5):
        """Create relationship: Address → Email"""
        with self.driver.session() as session:
            session.run("""
                MERGE (a:CryptoAddress {address: $address})
                MERGE (e:Email {email: $email})
                MERGE (a)-[r:LINKED_TO {confidence: $confidence, discovered_at: datetime()}]->(e)
                """,
                address=address,
                email=email,
                confidence=confidence
            )
    
    def link_email_to_username(self, email: str, username: str, platform: str):
        """Create relationship: Email → Username (on platform)"""
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Email {email: $email})
                MERGE (u:Username {username: $username, platform: $platform})
                MERGE (e)-[r:OWNS_ACCOUNT]->(u)
                """,
                email=email,
                username=username,
                platform=platform
            )
    
    def link_username_to_forum_profile(self, username: str, forum_url: str, profile_data: Dict):
        """Create relationship: Username → Forum Profile"""
        with self.driver.session() as session:
            session.run("""
                MERGE (u:Username {username: $username})
                MERGE (f:ForumProfile {url: $forum_url})
                SET f.posts_count = $posts_count,
                    f.reputation = $reputation,
                    f.last_active = $last_active
                MERGE (u)-[r:HAS_PROFILE]->(f)
                """,
                username=username,
                forum_url=forum_url,
                posts_count=profile_data.get("posts_count", 0),
                reputation=profile_data.get("reputation", 0),
                last_active=profile_data.get("last_active")
            )
    
    def link_to_telegram(self, username: str, telegram_handle: str):
        """Create relationship: Username → Telegram Handle"""
        with self.driver.session() as session:
            session.run("""
                MERGE (u:Username {username: $username})
                MERGE (t:TelegramHandle {handle: $telegram_handle})
                MERGE (u)-[r:LINKED_TO]->(t)
                """,
                username=username,
                telegram_handle=telegram_handle
            )
    
    def link_transaction(self, from_addr: str, to_addr: str, amount: float, timestamp: str, tx_hash: str):
        """Create transaction relationship"""
        with self.driver.session() as session:
            session.run("""
                MERGE (a1:CryptoAddress {address: $from_addr})
                MERGE (a2:CryptoAddress {address: $to_addr})
                CREATE (a1)-[t:TRANSACTED {
                    amount: $amount,
                    timestamp: $timestamp,
                    tx_hash: $tx_hash,
                    recorded_at: datetime()
                }]->(a2)
                """,
                from_addr=from_addr,
                to_addr=to_addr,
                amount=amount,
                timestamp=timestamp,
                tx_hash=tx_hash
            )
    
    def find_entity_graph(self, address: str, max_depth: int = 3) -> List[Dict]:
        """Get complete entity graph from address"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (a:CryptoAddress {address: $address})-[*1..$max_depth]-(related)
                RETURN DISTINCT
                    labels(related)[0] as node_type,
                    properties(related) as props,
                    length(path) as distance
                ORDER BY distance
                LIMIT 100
                """,
                address=address,
                max_depth=max_depth
            )
            return [record.data() for record in result]
    
    def find_clusters(self, address: str, min_confidence: float = 0.3) -> List[str]:
        """Find address clusters using transaction patterns"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a1:CryptoAddress {address: $address})-[:TRANSACTED*1..3]-(a2:CryptoAddress)
                WHERE a1 <> a2
                WITH a2, count(*) as connection_strength
                WHERE connection_strength > 2
                RETURN a2.address as address, 
                       a2.risk_score as risk_score,
                       connection_strength
                ORDER BY connection_strength DESC
                LIMIT 20
                """,
                address=address
            )
            return [record["address"] for record in result]
    
    def close(self):
        self.driver.close()
```

**Integration in `server.py`**:
```python
from graph_db import CryptoGraphDB

# Initialize at startup
graph_db = CryptoGraphDB()

@api_router.get("/analytics/entity-graph/{address}")
async def get_entity_graph(address: str, current_user: dict = Depends(get_current_user)):
    """Get complete entity correlation graph"""
    entity_graph = graph_db.find_entity_graph(address, max_depth=3)
    return {
        "address": address,
        "entities": entity_graph,
        "total_connections": len(entity_graph)
    }

@api_router.get("/analytics/clusters/{address}")
async def get_address_clusters(address: str, current_user: dict = Depends(get_current_user)):
    """Get clustered addresses"""
    clusters = graph_db.find_clusters(address, min_confidence=0.3)
    return {
        "address": address,
        "clustered_addresses": clusters,
        "cluster_size": len(clusters)
    }
```

**Update `requirements.txt`**:
```
neo4j==5.14.0
```

---

### 🟠 **PHASE 2: Adaptive Autonomous Crawling** (Week 2-3)

#### 2.1 Reinforcement Learning for Source Prioritization

**Purpose**: Crawler "learns what to hunt" based on intelligence value

**New File**: `backend/adaptive_crawler.py`
```python
from datetime import datetime, timedelta
from typing import Dict, List
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

logger = logging.getLogger(__name__)

class AdaptiveCrawler:
    """Self-learning crawler that prioritizes high-value sources"""
    
    def __init__(self, db):
        self.db = db
        self.learning_window = timedelta(hours=24)
    
    async def calculate_source_value(self, source_url: str) -> float:
        """Calculate intelligence value score for a source"""
        # Get addresses found from this source in last 24h
        since = datetime.now() - self.learning_window
        
        addresses = await self.db.addresses.find({
            "source_url": source_url,
            "first_seen": {"$gte": since}
        }).to_list(None)
        
        if not addresses:
            return 0.5  # Neutral score for new sources
        
        # Calculate value metrics
        total_count = len(addresses)
        high_risk_count = len([a for a in addresses if a.get("risk_score", 0) > 70])
        unique_pii_count = len(set([a.get("notes", "") for a in addresses if a.get("notes")]))
        
        # Value formula (0.0 - 1.0)
        value_score = min(1.0, (
            (total_count / 100) * 0.4 +  # Volume weight
            (high_risk_count / max(total_count, 1)) * 0.5 +  # Risk weight
            (unique_pii_count / max(total_count, 1)) * 0.1  # PII weight
        ))
        
        logger.info(f"📊 Source value for {source_url}: {value_score:.2f}")
        return value_score
    
    async def auto_adjust_crawl_frequency(self):
        """Automatically adjust crawl frequency based on intelligence value"""
        seeds = await self.db.seeds.find({"enabled": True}).to_list(None)
        
        for seed in seeds:
            source_value = await self.calculate_source_value(seed["url"])
            
            # Adaptive frequency logic
            if source_value > 0.8:
                new_frequency = "every_30min"
                new_priority = 1
            elif source_value > 0.6:
                new_frequency = "hourly"
                new_priority = 2
            elif source_value > 0.4:
                new_frequency = "every_6hours"
                new_priority = 3
            else:
                new_frequency = "daily"
                new_priority = 4
            
            # Update seed priority
            await self.db.seeds.update_one(
                {"_id": seed["_id"]},
                {"$set": {
                    "priority": new_priority,
                    "frequency": new_frequency,
                    "intelligence_value": source_value,
                    "last_evaluated": datetime.now()
                }}
            )
            
            logger.info(f"🎯 Adjusted {seed['name']}: priority={new_priority}, frequency={new_frequency}, value={source_value:.2f}")
    
    async def detect_trending_phrases(self) -> List[str]:
        """Detect frequently appearing crypto addresses/phrases"""
        # Get addresses from last 24 hours
        since = datetime.now() - self.learning_window
        recent_addresses = await self.db.addresses.find({
            "first_seen": {"$gte": since}
        }).to_list(None)
        
        # Count source appearances
        source_counts = {}
        for addr in recent_addresses:
            source = addr.get("source_url", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Return top trending sources
        trending = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        logger.info(f"📈 Trending sources: {trending}")
        
        return [source for source, count in trending if count > 5]
    
    async def suggest_new_sources(self) -> List[Dict]:
        """AI-suggested new sources based on current intelligence"""
        trending_phrases = await self.detect_trending_phrases()
        
        suggestions = []
        for phrase in trending_phrases:
            # Suggest related forums/sites
            if "bitcointalk" in phrase:
                suggestions.append({
                    "url": "https://bitcointalk.org/index.php?board=159.0",
                    "reason": "Related to trending BitcoinTalk activity",
                    "confidence": 0.75
                })
            elif "reddit" in phrase:
                suggestions.append({
                    "url": "https://old.reddit.com/r/cryptocurrency/new",
                    "reason": "Related to trending Reddit crypto discussions",
                    "confidence": 0.70
                })
        
        return suggestions
```

**Add Celery task in `tasks.py`**:
```python
from adaptive_crawler import AdaptiveCrawler

@celery_app.task
def run_adaptive_learning():
    """Run adaptive learning to adjust crawl priorities"""
    from motor.motor_asyncio import AsyncIOMotorClient
    import asyncio
    
    async def _run():
        client = AsyncIOMotorClient(os.environ['MONGO_URL'])
        db = client[os.environ['DB_NAME']]
        
        crawler = AdaptiveCrawler(db)
        await crawler.auto_adjust_crawl_frequency()
        
        client.close()
    
    asyncio.run(_run())
    logger.info("✅ Adaptive learning completed")
```

**Schedule in `celery_app.py`**:
```python
# Run adaptive learning every 6 hours
celery_app.conf.beat_schedule['adaptive-learning'] = {
    'task': 'tasks.run_adaptive_learning',
    'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
}
```

---

### 🟡 **PHASE 3: Threat Persona Graphs** (Week 3-4)

#### 3.1 AI-Generated Entity Summaries

**Purpose**: Create dynamic "threat personas" - AI summaries connecting PII, wallet, darknet activity, linguistic style

**New File**: `backend/threat_persona.py`
```python
from typing import Dict, List, Optional
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

class ThreatPersonaGenerator:
    """Generate AI-powered threat personas from entity data"""
    
    def __init__(self, db, graph_db):
        self.db = db
        self.graph_db = graph_db
    
    async def generate_persona(self, address: str) -> Dict:
        """Generate comprehensive threat persona for an address"""
        # Get address data
        addr_data = await self.db.addresses.find_one({"address": address})
        if not addr_data:
            return None
        
        # Get entity graph
        entity_graph = self.graph_db.find_entity_graph(address, max_depth=3)
        
        # Extract connected entities
        emails = [e["props"].get("email") for e in entity_graph if e["node_type"] == "Email"]
        usernames = [u["props"].get("username") for u in entity_graph if u["node_type"] == "Username"]
        forums = [f["props"].get("url") for f in entity_graph if f["node_type"] == "ForumProfile"]
        telegram = [t["props"].get("handle") for t in entity_graph if t["node_type"] == "TelegramHandle"]
        
        # Get transaction patterns
        transactions = self.graph_db.driver.session().run("""
            MATCH (a:CryptoAddress {address: $address})-[t:TRANSACTED]-(other)
            RETURN count(t) as tx_count,
                   avg(t.amount) as avg_amount,
                   max(t.amount) as max_amount
            """, address=address
        ).single()
        
        # Behavioral analysis
        behavior_profile = self._analyze_behavior(addr_data, entity_graph)
        
        # Generate persona summary
        persona = {
            "address": address,
            "crypto_type": addr_data.get("crypto_type"),
            "risk_score": addr_data.get("risk_score", 0),
            "category": addr_data.get("category", "unknown"),
            "first_seen": addr_data.get("first_seen"),
            "last_updated": addr_data.get("last_updated"),
            
            # Identity cluster
            "identity": {
                "emails": emails,
                "usernames": usernames,
                "platforms": list(set([u["props"].get("platform") for u in entity_graph if e["node_type"] == "Username"])),
                "forum_profiles": forums,
                "telegram_handles": telegram,
                "confidence": self._calculate_identity_confidence(emails, usernames, forums)
            },
            
            # Activity profile
            "activity": {
                "total_transactions": transactions["tx_count"] if transactions else 0,
                "average_amount": float(transactions["avg_amount"]) if transactions and transactions["avg_amount"] else 0.0,
                "largest_transaction": float(transactions["max_amount"]) if transactions and transactions["max_amount"] else 0.0,
                "active_days": (datetime.now() - addr_data.get("first_seen", datetime.now())).days
            },
            
            # Behavioral indicators
            "behavioral_profile": behavior_profile,
            
            # Threat assessment
            "threat_assessment": self._generate_threat_assessment(addr_data, behavior_profile),
            
            # AI-generated summary
            "ai_summary": self._generate_ai_summary(addr_data, emails, usernames, behavior_profile),
            
            # Evidence chain
            "evidence_chain": self._build_evidence_chain(addr_data, entity_graph),
            
            "generated_at": datetime.now()
        }
        
        return persona
    
    def _analyze_behavior(self, addr_data: Dict, entity_graph: List) -> Dict:
        """Analyze behavioral patterns"""
        patterns = {
            "mixer_usage": addr_data.get("category") == "money_laundering",
            "darknet_activity": "tor" in addr_data.get("source_url", "").lower() or ".onion" in addr_data.get("source_url", ""),
            "forum_presence": len([e for e in entity_graph if e["node_type"] == "ForumProfile"]) > 0,
            "multi_platform": len(set([e["props"].get("platform") for e in entity_graph if e["node_type"] == "Username"])) > 1,
            "pii_exposure": bool(addr_data.get("notes")),
            "high_volume_trader": addr_data.get("transaction_count", 0) > 100
        }
        
        return patterns
    
    def _calculate_identity_confidence(self, emails: List, usernames: List, forums: List) -> float:
        """Calculate confidence in identity attribution"""
        score = 0.0
        
        if emails:
            score += 0.4
        if usernames:
            score += 0.3
        if forums:
            score += 0.2
        if len(set(usernames)) > 1:
            score += 0.1  # Cross-platform consistency
        
        return min(1.0, score)
    
    def _generate_threat_assessment(self, addr_data: Dict, behavior: Dict) -> str:
        """Generate threat level assessment"""
        risk = addr_data.get("risk_score", 0)
        
        if risk > 80:
            threat_level = "CRITICAL"
            description = "High confidence threat actor"
        elif risk > 60:
            threat_level = "HIGH"
            description = "Likely involved in illicit activity"
        elif risk > 40:
            threat_level = "MEDIUM"
            description = "Suspicious patterns detected"
        else:
            threat_level = "LOW"
            description = "Limited threat indicators"
        
        # Add context
        contexts = []
        if behavior.get("mixer_usage"):
            contexts.append("money laundering")
        if behavior.get("darknet_activity"):
            contexts.append("dark web presence")
        if behavior.get("high_volume_trader"):
            contexts.append("high transaction volume")
        
        context_str = ", ".join(contexts) if contexts else "minimal suspicious activity"
        
        return f"{threat_level}: {description}. Context: {context_str}"
    
    def _generate_ai_summary(self, addr_data: Dict, emails: List, usernames: List, behavior: Dict) -> str:
        """Generate natural language summary"""
        summary_parts = []
        
        # Address info
        summary_parts.append(f"This {addr_data.get('crypto_type', 'cryptocurrency')} address")
        
        # Category
        if addr_data.get("category") != "unknown":
            summary_parts.append(f"is categorized as {addr_data.get('category')}")
        
        # Identity
        if emails:
            summary_parts.append(f"and is linked to email(s): {', '.join(emails[:2])}")
        if usernames:
            summary_parts.append(f"with username(s): {', '.join(usernames[:2])}")
        
        # Behavior
        if behavior.get("darknet_activity"):
            summary_parts.append("Has been observed on dark web marketplaces.")
        if behavior.get("mixer_usage"):
            summary_parts.append("Shows mixing/tumbling patterns.")
        if behavior.get("high_volume_trader"):
            summary_parts.append(f"Conducted {addr_data.get('transaction_count', 0)}+ transactions.")
        
        # Risk
        summary_parts.append(f"Risk score: {addr_data.get('risk_score', 0)}/100.")
        
        return " ".join(summary_parts)
    
    def _build_evidence_chain(self, addr_data: Dict, entity_graph: List) -> List[Dict]:
        """Build prosecutable evidence chain"""
        evidence = []
        
        # Source evidence
        evidence.append({
            "type": "SOURCE_ATTRIBUTION",
            "timestamp": addr_data.get("first_seen"),
            "description": f"Address discovered on {addr_data.get('source_url', 'unknown source')}",
            "confidence": 1.0
        })
        
        # Identity evidence
        for entity in entity_graph:
            if entity["node_type"] in ["Email", "Username", "TelegramHandle"]:
                evidence.append({
                    "type": "IDENTITY_LINK",
                    "timestamp": datetime.now(),
                    "description": f"Linked to {entity['node_type'].lower()}: {list(entity['props'].values())[0]}",
                    "confidence": 0.7
                })
        
        # Transaction evidence
        if addr_data.get("transaction_count", 0) > 0:
            evidence.append({
                "type": "BLOCKCHAIN_ACTIVITY",
                "timestamp": addr_data.get("last_updated"),
                "description": f"{addr_data.get('transaction_count')} on-chain transactions recorded",
                "confidence": 1.0
            })
        
        return evidence
```

**API Endpoint in `server.py`**:
```python
from threat_persona import ThreatPersonaGenerator

threat_persona_gen = ThreatPersonaGenerator(db, graph_db)

@api_router.get("/intelligence/persona/{address}")
async def get_threat_persona(address: str, current_user: dict = Depends(get_current_user)):
    """Get comprehensive threat persona for an address"""
    persona = await threat_persona_gen.generate_persona(address)
    if not persona:
        raise HTTPException(status_code=404, detail="Address not found")
    return persona
```

---

### 🟢 **PHASE 4: Explainable AI Layer** (Week 4-5)

#### 4.1 LLM-Based Reasoning Engine

**Purpose**: Explain WHY an address was flagged (for legal/evidential reporting)

**New File**: `backend/explainable_ai.py`
```python
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class ExplainableAI:
    """Explainable AI layer for risk assessments"""
    
    def __init__(self, db):
        self.db = db
    
    async def explain_risk_score(self, address_data: Dict) -> Dict:
        """Generate explainable reasoning for risk score"""
        explanations = []
        risk_score = address_data.get("risk_score", 0)
        
        # Category-based reasoning
        category = address_data.get("category", "unknown")
        if category == "ransomware":
            explanations.append({
                "factor": "CATEGORY_RANSOMWARE",
                "weight": 40,
                "description": "Address categorized as ransomware payment wallet based on source intelligence",
                "evidence": f"Source: {address_data.get('source_url')}"
            })
        elif category == "darknet_market":
            explanations.append({
                "factor": "CATEGORY_DARKNET",
                "weight": 35,
                "description": "Address found on dark web marketplace",
                "evidence": f"Discovered on Tor hidden service"
            })
        elif category == "money_laundering":
            explanations.append({
                "factor": "CATEGORY_LAUNDERING",
                "weight": 35,
                "description": "Transaction patterns consistent with mixing/tumbling services",
                "evidence": "Multiple rapid small transactions followed by consolidation"
            })
        
        # Source-based reasoning
        source_url = address_data.get("source_url", "")
        if ".onion" in source_url:
            explanations.append({
                "factor": "SOURCE_DARKWEB",
                "weight": 20,
                "description": "Address discovered on Tor dark web (.onion site)",
                "evidence": f"Source URL: {source_url}"
            })
        elif "pastebin" in source_url or "paste" in source_url:
            explanations.append({
                "factor": "SOURCE_LEAK",
                "weight": 15,
                "description": "Address found in public data dump/paste",
                "evidence": "Potential leak or public disclosure"
            })
        
        # Transaction pattern reasoning
        if address_data.get("transaction_count", 0) > 100:
            explanations.append({
                "factor": "HIGH_VOLUME",
                "weight": 10,
                "description": f"High transaction volume: {address_data.get('transaction_count')} transactions",
                "evidence": "Consistent with commercial/criminal operation"
            })
        
        # PII association
        if address_data.get("notes"):
            explanations.append({
                "factor": "PII_ASSOCIATED",
                "weight": 5,
                "description": "Personally identifiable information associated with address",
                "evidence": "Names, emails, or contact information linked"
            })
        
        return {
            "address": address_data.get("address"),
            "risk_score": risk_score,
            "risk_level": "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW",
            "explanations": explanations,
            "total_weight": sum([e["weight"] for e in explanations]),
            "reasoning_chain": self._generate_reasoning_chain(explanations),
            "legal_admissibility": "HIGH" if len(explanations) >= 3 else "MEDIUM"
        }
    
    def _generate_reasoning_chain(self, explanations: List[Dict]) -> str:
        """Generate natural language reasoning"""
        if not explanations:
            return "No significant risk factors identified."
        
        chain = "This address was flagged because: "
        chain += "; ".join([f"{e['description']}" for e in explanations])
        chain += "."
        
        return chain
```

**API Endpoint**:
```python
from explainable_ai import ExplainableAI

explainable_ai = ExplainableAI(db)

@api_router.get("/intelligence/explain/{address}")
async def explain_risk(address: str, current_user: dict = Depends(get_current_user)):
    """Get explainable AI reasoning for address risk"""
    addr_data = await db.addresses.find_one({"address": address})
    if not addr_data:
        raise HTTPException(status_code=404, detail="Address not found")
    
    explanation = await explainable_ai.explain_risk_score(addr_data)
    return explanation
```

---

### 🔵 **PHASE 5: Real-Time Leak-to-Blockchain Tracing** (Week 5-6)

#### 5.1 Leak Monitoring & Instant Cross-Check

**Purpose**: Detect crypto addresses in fresh leaks/dumps → instantly check if wallet has suspicious activity

**New File**: `backend/leak_monitor.py`
```python
from datetime import datetime, timedelta
from typing import List, Dict
import re
import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class LeakMonitor:
    """Monitor for crypto addresses in fresh leaks"""
    
    def __init__(self, db, graph_db):
        self.db = db
        self.graph_db = graph_db
        
        # Crypto regex patterns
        self.patterns = {
            'bitcoin': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{39,59}',
            'ethereum': r'0x[a-fA-F0-9]{40}',
        }
        
        # Leak sources to monitor
        self.leak_sources = [
            "https://pastebin.com/archive",
            "https://ghostbin.com/browse",
            # Add more paste sites
        ]
    
    async def monitor_pastebin(self) -> List[Dict]:
        """Monitor pastebin for fresh crypto leaks"""
        found_addresses = []
        
        async with aiohttp.ClientSession() as session:
            for source in self.leak_sources:
                try:
                    async with session.get(source, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Extract recent pastes
                            paste_links = soup.find_all('a', href=re.compile(r'/\w{8}'))[:20]
                            
                            for link in paste_links:
                                paste_url = f"https://pastebin.com{link['href']}"
                                addresses = await self._scan_paste(session, paste_url)
                                found_addresses.extend(addresses)
                
                except Exception as e:
                    logger.error(f"Error monitoring {source}: {e}")
        
        return found_addresses
    
    async def _scan_paste(self, session, paste_url: str) -> List[Dict]:
        """Scan individual paste for crypto addresses"""
        addresses = []
        
        try:
            async with session.get(paste_url, timeout=10) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    # Search for crypto addresses
                    for crypto_type, pattern in self.patterns.items():
                        matches = re.findall(pattern, text)
                        for match in set(matches):  # Deduplicate
                            # Instant cross-check
                            analysis = await self._instant_analysis(match, crypto_type)
                            
                            addresses.append({
                                "address": match,
                                "crypto_type": crypto_type,
                                "source_url": paste_url,
                                "discovered_at": datetime.now(),
                                "leak_context": text[:200],  # First 200 chars
                                "instant_analysis": analysis
                            })
                            
                            logger.info(f"🚨 LEAK DETECTED: {match} on {paste_url}")
        
        except Exception as e:
            logger.error(f"Error scanning paste {paste_url}: {e}")
        
        return addresses
    
    async def _instant_analysis(self, address: str, crypto_type: str) -> Dict:
        """Instantly analyze if address has suspicious activity"""
        # Check if address already in database
        existing = await self.db.addresses.find_one({"address": address})
        
        if existing:
            return {
                "known_address": True,
                "risk_score": existing.get("risk_score", 0),
                "category": existing.get("category", "unknown"),
                "transaction_count": existing.get("transaction_count", 0),
                "alert_level": "HIGH" if existing.get("risk_score", 0) > 70 else "MEDIUM"
            }
        else:
            # New address - quick blockchain check
            # (Integrate with Blockchair API here)
            return {
                "known_address": False,
                "alert_level": "NEW_DISCOVERY",
                "requires_analysis": True
            }
    
    async def create_leak_alert(self, leak_data: Dict):
        """Create alert for high-value leak discovery"""
        await self.db.leak_alerts.insert_one({
            "address": leak_data["address"],
            "crypto_type": leak_data["crypto_type"],
            "source_url": leak_data["source_url"],
            "discovered_at": leak_data["discovered_at"],
            "analysis": leak_data["instant_analysis"],
            "status": "new",
            "created_at": datetime.now()
        })
        
        logger.warning(f"🚨 HIGH-VALUE LEAK ALERT: {leak_data['address']}")
```

**Celery Task**:
```python
@celery_app.task
def monitor_leaks():
    """Monitor for crypto addresses in fresh leaks"""
    from leak_monitor import LeakMonitor
    import asyncio
    
    async def _run():
        client = AsyncIOMotorClient(os.environ['MONGO_URL'])
        db = client[os.environ['DB_NAME']]
        graph_db = CryptoGraphDB()
        
        monitor = LeakMonitor(db, graph_db)
        found = await monitor.monitor_pastebin()
        
        # Create alerts for high-risk addresses
        for leak in found:
            if leak["instant_analysis"].get("alert_level") == "HIGH":
                await monitor.create_leak_alert(leak)
        
        client.close()
        logger.info(f"✅ Leak monitoring completed: {len(found)} addresses found")
    
    asyncio.run(_run())
```

**Schedule**:
```python
# Run every 15 minutes
celery_app.conf.beat_schedule['leak-monitoring'] = {
    'task': 'tasks.monitor_leaks',
    'schedule': 900.0,  # 15 minutes
}
```

---

### 🟣 **PHASE 6: Graph-Native Intelligence Export** (Week 6)

#### 6.1 Interactive Graph JSON Export

**Purpose**: Export intelligence as interactive graph (not static PDF) for agency tools

**API Endpoint in `server.py`**:
```python
@api_router.get("/export/graph/{address}")
async def export_entity_graph(
    address: str,
    format: str = "json",  # json, neo4j, graphml
    current_user: dict = Depends(get_current_user)
):
    """Export entity graph in agency-compatible formats"""
    from graph_db import CryptoGraphDB
    import json
    
    graph_db = CryptoGraphDB()
    entity_graph = graph_db.find_entity_graph(address, max_depth=4)
    
    if format == "json":
        # NetworkX-compatible JSON
        export_data = {
            "graph_type": "entity_correlation",
            "root_address": address,
            "nodes": [],
            "links": []
        }
        
        node_ids = set()
        for entity in entity_graph:
            node_id = list(entity["props"].values())[0]
            if node_id not in node_ids:
                export_data["nodes"].append({
                    "id": node_id,
                    "type": entity["node_type"],
                    "properties": entity["props"],
                    "distance": entity["distance"]
                })
                node_ids.add(node_id)
        
        # Get relationships
        with graph_db.driver.session() as session:
            result = session.run("""
                MATCH (a)-[r]->(b)
                WHERE a.address = $address OR b.address = $address
                RETURN type(r) as rel_type,
                       properties(a) as source,
                       properties(b) as target
                LIMIT 200
                """, address=address
            )
            
            for record in result:
                export_data["links"].append({
                    "source": list(record["source"].values())[0],
                    "target": list(record["target"].values())[0],
                    "relationship": record["rel_type"]
                })
        
        return export_data
    
    elif format == "neo4j":
        # Neo4j Cypher export
        cypher_query = f"""
        MATCH path = (a:CryptoAddress {{address: '{address}'}})-[*1..4]-(related)
        RETURN path
        """
        return {"cypher": cypher_query, "format": "neo4j"}
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
```

---

## 📊 Updated System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS INTELLIGENCE                   │
│                    CORRELATION ENGINE                        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼─────────┐
│  MULTI-MODAL   │  │   ADAPTIVE      │  │  THREAT PERSONA  │
│  DATA FUSION   │  │   CRAWLER       │  │    GENERATOR     │
├────────────────┤  ├─────────────────┤  ├──────────────────┤
│ • Neo4j Graph  │  │ • Reinforcement │  │ • AI Summaries   │
│ • Entity Links │  │ • Auto-Priority │  │ • Evidence Chain │
│ • PII Mapping  │  │ • Intelligence  │  │ • Behavioral     │
│ • Cross-Surface│  │   Value Scoring │  │   Profiling      │
└────────────────┘  └─────────────────┘  └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼─────────┐
│  EXPLAINABLE   │  │  REAL-TIME      │  │  GRAPH-NATIVE    │
│      AI        │  │  LEAK TRACE     │  │    EXPORT        │
├────────────────┤  ├─────────────────┤  ├──────────────────┤
│ • LLM Reasoning│  │ • Pastebin Mon  │  │ • JSON-LD        │
│ • Legal Report │  │ • Instant Check │  │ • Neo4j Cypher   │
│ • Risk Explain │  │ • Alert System  │  │ • NetworkX       │
└────────────────┘  └─────────────────┘  └──────────────────┘
```

---

## 🎯 USP Narrative (For Pitching)

**"NTRO-CryptoForensics is not a simple blockchain analyzer — it's an autonomous intelligence correlation engine that connects the blockchain, dark web, and surface internet into one evolving graph of threats, personas, and financial traces. It transforms raw, unstructured data into explainable, actionable intelligence — autonomously."**

### Key Differentiators:
1. ✅ **Multi-Modal Fusion**: Links wallet → email → forum → Telegram (competitors stop at blockchain)
2. ✅ **Self-Learning Crawler**: Auto-prioritizes high-value sources (not static scraping)
3. ✅ **Threat Personas**: AI-generated entity summaries (graph-based profiling)
4. ✅ **On + Off-Chain Clustering**: Combines blockchain + behavioral analysis
5. ✅ **Real-Time Leak Tracing**: Instant cross-check of addresses in dumps
6. ✅ **Explainable AI**: LLM reasoning for legal admissibility
7. ✅ **Graph-Native Export**: Interoperable intelligence (not static PDFs)

---

## 📅 Implementation Timeline

| Phase | Feature | Duration | Status |
|-------|---------|----------|--------|
| 1 | Neo4j Multi-Modal Fusion | Week 1-2 | ⏳ TODO |
| 2 | Adaptive Autonomous Crawling | Week 2-3 | ⏳ TODO |
| 3 | Threat Persona Graphs | Week 3-4 | ⏳ TODO |
| 4 | Explainable AI Layer | Week 4-5 | ⏳ TODO |
| 5 | Real-Time Leak Monitoring | Week 5-6 | ⏳ TODO |
| 6 | Graph-Native Export | Week 6 | ⏳ TODO |

**Total Time**: 6 weeks to full "Autonomous Intelligence Correlation Engine"

---

## 🚀 Getting Started

### Install Neo4j
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/cryptoforensics \
  neo4j:latest
```

### Update Requirements
```bash
cd backend
pip install neo4j==5.14.0
```

### Start Building
1. Implement `backend/graph_db.py` (Phase 1)
2. Test entity linking with existing addresses
3. Move to adaptive crawler (Phase 2)
4. Build incrementally

---

## 📈 Long-Term Vision (Post-SIH)

1. **Autonomous Analyst Agents**: LLM agents that suggest next investigation steps
2. **Law Enforcement API Integration**: Connect with Chainalysis, Elliptic, Interpol
3. **Threat Simulation Mode**: Predict suspect movements through mixers
4. **Cyber Deception Layer**: Deploy honeypot wallets to attract attackers
5. **Multi-Language NLP**: Extract PII in Russian, Chinese, Arabic
6. **Federated Learning**: Collaborate with agencies while preserving privacy

---

**This roadmap transforms your project from "crypto tracker" to "autonomous intelligence platform" — positioning you as the next-gen forensics solution!** 🚀
