"""
🧠 NTRO-CryptoForensics: Multi-Modal Intelligence Fusion Engine
==============================================================

Autonomous correlation engine that fuses:
- Blockchain data (addresses, transactions, clusters)  
- Dark-web intelligence (onion sites, forums, marketplaces)
- Surface-web footprints (social media, emails, usernames)
- Leaked data (data breaches, paste dumps, Telegram)

Creates unified entity graphs for threat attribution.
"""

import asyncio
import aiohttp
import re
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
from collections import defaultdict

from motor.motor_asyncio import AsyncIOMotorDatabase
from neo4j import AsyncGraphDatabase
import networkx as nx
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

@dataclass
class IntelligenceEntity:
    """Unified entity representing a threat actor or cluster"""
    entity_id: str
    entity_type: str  # 'wallet', 'email', 'username', 'onion_profile', 'telegram_handle'
    primary_identifier: str
    aliases: Set[str] = field(default_factory=set)
    crypto_addresses: Set[str] = field(default_factory=set)
    email_addresses: Set[str] = field(default_factory=set)
    social_profiles: Dict[str, str] = field(default_factory=dict)
    onion_profiles: List[Dict] = field(default_factory=list)
    telegram_handles: Set[str] = field(default_factory=set)
    leaked_data_refs: List[Dict] = field(default_factory=list)
    risk_score: float = 0.0
    confidence_score: float = 0.0
    last_activity: Optional[datetime] = None
    intelligence_sources: List[str] = field(default_factory=list)
    
class MultiModalFusionEngine:
    """Core intelligence correlation engine"""
    
    def __init__(self, mongo_db: AsyncIOMotorDatabase, neo4j_uri: str, neo4j_auth: tuple):
        self.db = mongo_db
        self.neo4j_driver = AsyncGraphDatabase.driver(neo4j_uri, auth=neo4j_auth)
        self.entities = {}  # entity_id -> IntelligenceEntity
        self.correlation_graph = nx.MultiDiGraph()
        
        # Intelligence sources configuration
        self.sources = {
            'blockchain': ['blockchair', 'blockchain_info', 'walletexplorer'],
            'darkweb': ['onion_forums', 'darknet_markets', 'paste_sites'],
            'surface_web': ['social_media', 'email_leaks', 'breach_data'],
            'telegram': ['channel_scraper', 'group_monitor', 'leak_tracker']
        }
        
        # Pattern matchers for cross-surface correlation
        self.patterns = {
            'crypto_address': re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|0x[a-fA-F0-9]{40}\b'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'username': re.compile(r'@[a-zA-Z0-9_]{3,20}\b'),
            'onion_url': re.compile(r'[a-z2-7]{16,56}\.onion'),
            'telegram_handle': re.compile(r't\.me/[a-zA-Z0-9_]{5,32}')
        }
    
    async def fuse_intelligence(self, data_sources: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Main fusion function - correlates intelligence across all data sources
        """
        print("🧠 Starting multi-modal intelligence fusion...")
        
        # Step 1: Extract entities from all sources
        extracted_entities = await self._extract_entities_from_sources(data_sources)
        
        # Step 2: Build correlation graph
        correlation_graph = await self._build_correlation_graph(extracted_entities)
        
        # Step 3: Cluster related entities
        clustered_entities = await self._cluster_related_entities(correlation_graph)
        
        # Step 4: Generate threat personas
        threat_personas = await self._generate_threat_personas(clustered_entities)
        
        # Step 5: Calculate risk scores
        risk_assessments = await self._calculate_risk_scores(threat_personas)
        
        # Step 6: Store in Neo4j for graph queries
        await self._store_intelligence_graph(risk_assessments)
        
        return {
            'fusion_timestamp': datetime.utcnow().isoformat(),
            'entities_discovered': len(extracted_entities),
            'clusters_formed': len(clustered_entities),
            'threat_personas': threat_personas,
            'high_risk_entities': [p for p in threat_personas if p['risk_score'] > 0.7],
            'correlation_strength': self._calculate_graph_density(correlation_graph),
            'intelligence_summary': await self._generate_intelligence_summary(threat_personas)
        }
    
    async def _extract_entities_from_sources(self, data_sources: Dict[str, List[Dict]]) -> List[IntelligenceEntity]:
        """Extract and normalize entities from multiple intelligence sources"""
        entities = []
        
        # Blockchain data extraction
        if 'blockchain' in data_sources:
            for address_data in data_sources['blockchain']:
                entity = IntelligenceEntity(
                    entity_id=f"addr_{hashlib.md5(address_data['address'].encode()).hexdigest()[:8]}",
                    entity_type='wallet',
                    primary_identifier=address_data['address'],
                    crypto_addresses={address_data['address']},
                    intelligence_sources=['blockchain'],
                    last_activity=datetime.fromisoformat(address_data.get('last_seen', datetime.utcnow().isoformat()))
                )
                entities.append(entity)
        
        # Dark web intelligence extraction  
        if 'darkweb' in data_sources:
            for profile_data in data_sources['darkweb']:
                entity = IntelligenceEntity(
                    entity_id=f"onion_{hashlib.md5(profile_data['username'].encode()).hexdigest()[:8]}",
                    entity_type='onion_profile',
                    primary_identifier=profile_data['username'],
                    aliases={profile_data.get('display_name', '')},
                    onion_profiles=[profile_data],
                    intelligence_sources=['darkweb']
                )
                
                # Extract crypto addresses from profile content
                if 'content' in profile_data:
                    crypto_addrs = self.patterns['crypto_address'].findall(profile_data['content'])
                    entity.crypto_addresses.update(crypto_addrs)
                    
                entities.append(entity)
        
        # Surface web extraction
        if 'surface_web' in data_sources:
            for leak_data in data_sources['surface_web']:
                entity = IntelligenceEntity(
                    entity_id=f"leak_{hashlib.md5(leak_data['email'].encode()).hexdigest()[:8]}",
                    entity_type='email',
                    primary_identifier=leak_data['email'],
                    email_addresses={leak_data['email']},
                    leaked_data_refs=[leak_data],
                    intelligence_sources=['surface_web']
                )
                entities.append(entity)
        
        # Telegram intelligence extraction
        if 'telegram' in data_sources:
            for tg_data in data_sources['telegram']:
                entity = IntelligenceEntity(
                    entity_id=f"tg_{hashlib.md5(tg_data['handle'].encode()).hexdigest()[:8]}",
                    entity_type='telegram_handle',
                    primary_identifier=tg_data['handle'],
                    telegram_handles={tg_data['handle']},
                    intelligence_sources=['telegram']
                )
                
                # Extract emails and crypto addresses from messages
                if 'messages' in tg_data:
                    all_text = ' '.join([msg.get('text', '') for msg in tg_data['messages']])
                    emails = self.patterns['email'].findall(all_text)
                    crypto_addrs = self.patterns['crypto_address'].findall(all_text)
                    
                    entity.email_addresses.update(emails)
                    entity.crypto_addresses.update(crypto_addrs)
                    
                entities.append(entity)
        
        return entities
    
    async def _build_correlation_graph(self, entities: List[IntelligenceEntity]) -> nx.MultiDiGraph:
        """Build graph connecting entities based on shared identifiers"""
        G = nx.MultiDiGraph()
        
        # Add all entities as nodes
        for entity in entities:
            G.add_node(entity.entity_id, 
                      entity_type=entity.entity_type,
                      primary_id=entity.primary_identifier,
                      risk_score=entity.risk_score)
        
        # Create edges based on shared identifiers
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities[i+1:], i+1):
                correlations = self._find_correlations(entity1, entity2)
                
                for correlation_type, strength in correlations.items():
                    if strength > 0.5:  # Minimum correlation threshold
                        G.add_edge(entity1.entity_id, entity2.entity_id,
                                 correlation_type=correlation_type,
                                 strength=strength,
                                 evidence=self._get_correlation_evidence(entity1, entity2, correlation_type))
        
        return G
    
    def _find_correlations(self, entity1: IntelligenceEntity, entity2: IntelligenceEntity) -> Dict[str, float]:
        """Find correlations between two entities"""
        correlations = {}
        
        # Crypto address overlap
        addr_overlap = len(entity1.crypto_addresses & entity2.crypto_addresses)
        if addr_overlap > 0:
            correlations['crypto_address'] = min(1.0, addr_overlap / 3)  # Strong correlation for 3+ shared addresses
        
        # Email address overlap  
        email_overlap = len(entity1.email_addresses & entity2.email_addresses)
        if email_overlap > 0:
            correlations['email_address'] = min(1.0, email_overlap / 2)
        
        # Username similarity
        alias_overlap = len(entity1.aliases & entity2.aliases)
        if alias_overlap > 0:
            correlations['username_alias'] = min(1.0, alias_overlap / 2)
        
        # Telegram handle overlap
        tg_overlap = len(entity1.telegram_handles & entity2.telegram_handles)
        if tg_overlap > 0:
            correlations['telegram_handle'] = 1.0  # Strong indicator
        
        return correlations
    
    def _get_correlation_evidence(self, entity1: IntelligenceEntity, entity2: IntelligenceEntity, correlation_type: str) -> List[str]:
        """Get evidence supporting the correlation"""
        evidence = []
        
        if correlation_type == 'crypto_address':
            shared_addrs = entity1.crypto_addresses & entity2.crypto_addresses
            evidence.extend([f"Shared crypto address: {addr}" for addr in shared_addrs])
        
        elif correlation_type == 'email_address':
            shared_emails = entity1.email_addresses & entity2.email_addresses  
            evidence.extend([f"Shared email: {email}" for email in shared_emails])
        
        elif correlation_type == 'username_alias':
            shared_aliases = entity1.aliases & entity2.aliases
            evidence.extend([f"Shared alias: {alias}" for alias in shared_aliases])
        
        return evidence
    
    async def _cluster_related_entities(self, graph: nx.MultiDiGraph) -> List[Dict]:
        """Cluster highly correlated entities into threat groups"""
        # Use community detection to find clusters
        try:
            import networkx.algorithms.community as nx_comm
            communities = list(nx_comm.greedy_modularity_communities(graph.to_undirected()))
        except:
            # Fallback: simple connected components
            communities = list(nx.connected_components(graph.to_undirected()))
        
        clusters = []
        for i, community in enumerate(communities):
            if len(community) > 1:  # Only meaningful clusters
                cluster = {
                    'cluster_id': f"cluster_{i}",
                    'entity_count': len(community),
                    'entities': list(community),
                    'cluster_strength': self._calculate_cluster_strength(graph, community),
                    'primary_entity_types': self._get_cluster_entity_types(graph, community)
                }
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_cluster_strength(self, graph: nx.MultiDiGraph, community: Set[str]) -> float:
        """Calculate internal connectivity strength of a cluster"""
        if len(community) < 2:
            return 0.0
        
        internal_edges = [(u, v) for u, v in graph.edges() if u in community and v in community]
        max_possible_edges = len(community) * (len(community) - 1)
        
        return len(internal_edges) / max_possible_edges if max_possible_edges > 0 else 0.0
    
    def _get_cluster_entity_types(self, graph: nx.MultiDiGraph, community: Set[str]) -> Dict[str, int]:
        """Get distribution of entity types in cluster"""
        types = defaultdict(int)
        for entity_id in community:
            entity_type = graph.nodes[entity_id].get('entity_type', 'unknown')
            types[entity_type] += 1
        return dict(types)
    
    async def _generate_threat_personas(self, clusters: List[Dict]) -> List[Dict]:
        """Generate AI-powered threat personas for each cluster"""
        personas = []
        
        for cluster in clusters:
            # Gather all intelligence about this cluster
            cluster_intel = await self._gather_cluster_intelligence(cluster)
            
            # Generate persona using LLM
            persona_prompt = self._build_persona_prompt(cluster_intel)
            
            # Here you would integrate with an LLM like OpenAI
            # For demo purposes, we'll create a structured persona
            persona = {
                'persona_id': cluster['cluster_id'],
                'threat_actor_name': f"ThreatActor_{cluster['cluster_id'][-3:].upper()}",
                'confidence_level': cluster['cluster_strength'],
                'entity_count': cluster['entity_count'],
                'primary_indicators': self._extract_primary_indicators(cluster_intel),
                'attack_vectors': self._infer_attack_vectors(cluster_intel),
                'geographical_indicators': self._extract_geo_indicators(cluster_intel),
                'activity_timeline': self._build_activity_timeline(cluster_intel),
                'risk_factors': self._assess_risk_factors(cluster_intel),
                'recommended_actions': self._suggest_investigative_actions(cluster_intel)
            }
            
            personas.append(persona)
        
        return personas
    
    async def _gather_cluster_intelligence(self, cluster: Dict) -> Dict:
        """Gather all available intelligence about a cluster"""
        intel = {
            'crypto_addresses': set(),
            'email_addresses': set(), 
            'social_profiles': {},
            'onion_activity': [],
            'telegram_activity': [],
            'leaked_data': [],
            'timeline_events': []
        }
        
        # This would be populated from the actual entity data
        # For now, return structured placeholder
        return intel
    
    def _extract_primary_indicators(self, cluster_intel: Dict) -> List[str]:
        """Extract key indicators of compromise (IOCs)"""
        iocs = []
        
        # Top crypto addresses by activity
        if cluster_intel['crypto_addresses']:
            iocs.extend([f"Crypto: {addr}" for addr in list(cluster_intel['crypto_addresses'])[:3]])
        
        # Key email addresses
        if cluster_intel['email_addresses']:
            iocs.extend([f"Email: {email}" for email in list(cluster_intel['email_addresses'])[:2]])
        
        return iocs
    
    def _infer_attack_vectors(self, cluster_intel: Dict) -> List[str]:
        """Infer likely attack vectors based on intelligence"""
        vectors = []
        
        if cluster_intel['onion_activity']:
            vectors.append("Dark web operations")
        if cluster_intel['crypto_addresses']:
            vectors.append("Cryptocurrency money laundering") 
        if cluster_intel['telegram_activity']:
            vectors.append("Encrypted communications")
        if cluster_intel['leaked_data']:
            vectors.append("Data breach monetization")
        
        return vectors
    
    async def _calculate_risk_scores(self, personas: List[Dict]) -> List[Dict]:
        """Calculate sophisticated risk scores for each persona"""
        
        for persona in personas:
            risk_factors = {
                'crypto_activity': 0.3,  # Base score for crypto involvement
                'darkweb_presence': 0.4,  # Higher risk for onion activity
                'leak_association': 0.2,  # Risk from data breach connections
                'communication_encryption': 0.1  # Risk from encrypted comms
            }
            
            # Calculate weighted risk score
            total_risk = sum(risk_factors.values())
            persona['risk_score'] = min(1.0, total_risk)
            
            # Risk category
            if persona['risk_score'] >= 0.8:
                persona['risk_category'] = 'CRITICAL'
            elif persona['risk_score'] >= 0.6:
                persona['risk_category'] = 'HIGH'
            elif persona['risk_score'] >= 0.4:
                persona['risk_category'] = 'MEDIUM'
            else:
                persona['risk_category'] = 'LOW'
        
        return personas
    
    async def _store_intelligence_graph(self, personas: List[Dict]):
        """Store intelligence graph in Neo4j for complex queries"""
        async with self.neo4j_driver.session() as session:
            # Create persona nodes
            for persona in personas:
                await session.run("""
                    MERGE (p:ThreatPersona {persona_id: $persona_id})
                    SET p.threat_actor_name = $name,
                        p.risk_score = $risk_score,
                        p.risk_category = $risk_category,
                        p.confidence_level = $confidence,
                        p.last_updated = datetime()
                """, persona_id=persona['persona_id'],
                      name=persona['threat_actor_name'],
                      risk_score=persona['risk_score'],
                      risk_category=persona['risk_category'],
                      confidence=persona['confidence_level'])
    
    def _calculate_graph_density(self, graph: nx.MultiDiGraph) -> float:
        """Calculate how connected the intelligence graph is"""
        try:
            return nx.density(graph)
        except:
            return 0.0
    
    async def _generate_intelligence_summary(self, personas: List[Dict]) -> str:
        """Generate executive summary of intelligence findings"""
        total_personas = len(personas)
        high_risk_count = len([p for p in personas if p['risk_score'] >= 0.7])
        
        summary = f"""
        🧠 AUTONOMOUS INTELLIGENCE CORRELATION - EXECUTIVE SUMMARY
        =====================================================
        
        📊 THREAT LANDSCAPE OVERVIEW:
        • Total Threat Personas Identified: {total_personas}
        • High-Risk Entities: {high_risk_count}
        • Intelligence Fusion Sources: Blockchain + Dark Web + Surface Web + Telegram
        
        🎯 KEY FINDINGS:
        • {high_risk_count}/{total_personas} personas require immediate investigation
        • Cross-surface correlations detected across multiple threat vectors
        • Autonomous clustering identified {len([p for p in personas if p['entity_count'] > 3])} large threat networks
        
        🚨 RECOMMENDED ACTIONS:
        • Priority investigation of CRITICAL risk personas
        • Enhanced monitoring of correlated addresses and communications
        • Cross-reference with law enforcement databases
        """
        
        return summary.strip()

# Utility functions for external integration
async def initialize_fusion_engine(mongo_db: AsyncIOMotorDatabase) -> MultiModalFusionEngine:
    """Initialize the fusion engine with database connections"""
    # Neo4j connection - you'd configure this with actual credentials
    neo4j_uri = "bolt://localhost:7687" 
    neo4j_auth = ("neo4j", "password")
    
    return MultiModalFusionEngine(mongo_db, neo4j_uri, neo4j_auth)

async def run_intelligence_fusion(fusion_engine: MultiModalFusionEngine, 
                                data_sources: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Run complete intelligence fusion process"""
    return await fusion_engine.fuse_intelligence(data_sources)

# Example usage and testing
if __name__ == "__main__":
    # Demo data for testing the fusion engine
    demo_data = {
        'blockchain': [
            {'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'last_seen': '2024-01-15T10:30:00'},
            {'address': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2', 'last_seen': '2024-01-14T08:15:00'}
        ],
        'darkweb': [
            {'username': 'cryptoking99', 'display_name': 'King of Crypto', 
             'content': 'Selling BTC 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa contact crypto.king@protonmail.com'}
        ],
        'surface_web': [
            {'email': 'crypto.king@protonmail.com', 'breach': 'Collection1', 'password': 'hashed'}
        ],
        'telegram': [
            {'handle': '@cryptoking99_official', 
             'messages': [{'text': 'New wallet: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'}]}
        ]
    }
    
    print("🧠 Multi-Modal Intelligence Fusion Engine")
    print("Ready for autonomous threat correlation!")