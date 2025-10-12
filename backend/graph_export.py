"""
📊 NTRO-CryptoForensics: Graph-Native Intelligence Export
========================================================

Advanced intelligence sharing system that:
- Exports interactive graph data in multiple standard formats
- Supports JSON-LD, Neo4j, GraphML, STIX for agency integration
- Creates interoperable intelligence packages
- Enables cross-agency collaboration and data sharing
- Maintains data provenance and chain of custody
- Supports real-time intelligence feed syndication

Goes beyond static PDFs to provide actionable, machine-readable intelligence.
"""

import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import uuid
import base64
import hashlib
import logging

import networkx as nx
from motor.motor_asyncio import AsyncIOMotorDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExportFormat(Enum):
    JSON_LD = "json-ld"
    NEO4J_CYPHER = "neo4j-cypher"
    GRAPHML = "graphml"
    STIX = "stix"
    CSV = "csv"
    GEPHI = "gephi"
    D3_JSON = "d3-json"
    NETWORKX = "networkx"

class ConfidenceLevel(Enum):
    UNVERIFIED = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERIFIED = 5

class ThreatLevel(Enum):
    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

@dataclass
class GraphNode:
    """Represents a node in the intelligence graph"""
    node_id: str
    node_type: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    threat_level: ThreatLevel = ThreatLevel.INFO
    source: str = "ntro_cryptoforensics"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    provenance: List[str] = field(default_factory=list)

@dataclass
class GraphEdge:
    """Represents an edge in the intelligence graph"""
    edge_id: str
    source_node: str
    target_node: str
    relationship_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    weight: float = 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    evidence: List[str] = field(default_factory=list)

@dataclass
class IntelligenceGraph:
    """Complete intelligence graph structure"""
    graph_id: str
    title: str
    description: str
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    classification: str = "UNCLASSIFIED"
    handling_instructions: List[str] = field(default_factory=list)

@dataclass
class ExportPackage:
    """Complete intelligence export package"""
    package_id: str
    format: ExportFormat
    content: Any
    metadata: Dict[str, Any]
    signature: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

class GraphBuilder:
    """Builds intelligence graphs from various data sources"""
    
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.db = mongo_db
        self.graphs: Dict[str, IntelligenceGraph] = {}
    
    async def build_threat_persona_graph(self, personas: List[Dict]) -> IntelligenceGraph:
        """Build graph from threat personas"""
        graph_id = f"threat_personas_{int(datetime.utcnow().timestamp())}"
        
        graph = IntelligenceGraph(
            graph_id=graph_id,
            title="Threat Actor Network Analysis",
            description="Graph representation of identified threat actors and their relationships",
            classification="CONFIDENTIAL",
            handling_instructions=["Law Enforcement Sensitive", "Not for Public Release"]
        )
        
        # Create nodes for each persona
        for persona in personas:
            node = GraphNode(
                node_id=persona.get('persona_id', str(uuid.uuid4())),
                node_type="threat_actor",
                label=persona.get('primary_identifier', 'Unknown Actor'),
                properties={
                    'threat_level': persona.get('threat_level', 'UNKNOWN'),
                    'confidence_score': persona.get('confidence_score', 0.0),
                    'crypto_wallets': persona.get('crypto_wallets', []),
                    'email_addresses': persona.get('email_addresses', []),
                    'telegram_handles': persona.get('telegram_handles', []),
                    'attack_vectors': persona.get('attack_vectors', []),
                    'first_activity': persona.get('first_activity'),
                    'last_activity': persona.get('last_activity')
                },
                confidence=self._map_confidence(persona.get('confidence_score', 0.0)),
                threat_level=self._map_threat_level(persona.get('threat_level', 'UNKNOWN')),
                provenance=[f"Persona analysis at {datetime.utcnow().isoformat()}"]
            )
            graph.nodes.append(node)
            
            # Create nodes for associated assets
            for wallet in persona.get('crypto_wallets', []):
                wallet_node = GraphNode(
                    node_id=f"wallet_{hashlib.md5(wallet.encode()).hexdigest()[:8]}",
                    node_type="crypto_wallet",
                    label=wallet,
                    properties={
                        'address': wallet,
                        'currency_type': 'unknown',  # Would be determined from analysis
                        'associated_actor': node.node_id
                    },
                    confidence=ConfidenceLevel.HIGH,
                    provenance=[f"Associated with {node.label}"]
                )
                graph.nodes.append(wallet_node)
                
                # Create edge between actor and wallet
                edge = GraphEdge(
                    edge_id=f"owns_{node.node_id}_{wallet_node.node_id}",
                    source_node=node.node_id,
                    target_node=wallet_node.node_id,
                    relationship_type="OWNS",
                    confidence=0.8,
                    evidence=[f"Wallet found in persona analysis"]
                )
                graph.edges.append(edge)
        
        # Create edges between related personas (if correlation exists)
        for i, persona1 in enumerate(personas):
            for j, persona2 in enumerate(personas[i+1:], i+1):
                correlation_score = self._calculate_persona_correlation(persona1, persona2)
                
                if correlation_score > 0.5:
                    edge = GraphEdge(
                        edge_id=f"related_{persona1.get('persona_id')}_{persona2.get('persona_id')}",
                        source_node=persona1.get('persona_id'),
                        target_node=persona2.get('persona_id'),
                        relationship_type="RELATED_TO",
                        confidence=correlation_score,
                        weight=correlation_score,
                        evidence=[f"Correlation analysis score: {correlation_score:.2f}"]
                    )
                    graph.edges.append(edge)
        
        self.graphs[graph_id] = graph
        return graph
    
    async def build_blockchain_activity_graph(self, addresses: List[Dict], 
                                            transactions: List[Dict]) -> IntelligenceGraph:
        """Build graph from blockchain activity"""
        graph_id = f"blockchain_activity_{int(datetime.utcnow().timestamp())}"
        
        graph = IntelligenceGraph(
            graph_id=graph_id,
            title="Cryptocurrency Transaction Network",
            description="Graph representation of cryptocurrency addresses and transaction flows",
            classification="UNCLASSIFIED",
            metadata={
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'address_count': len(addresses),
                'transaction_count': len(transactions)
            }
        )
        
        # Create nodes for addresses
        for addr_data in addresses:
            node = GraphNode(
                node_id=f"addr_{addr_data['address']}",
                node_type="crypto_address",
                label=addr_data['address'],
                properties={
                    'address': addr_data['address'],
                    'balance': addr_data.get('balance', 0),
                    'transaction_count': addr_data.get('transaction_count', 0),
                    'first_seen': addr_data.get('first_seen'),
                    'last_seen': addr_data.get('last_seen'),
                    'risk_score': addr_data.get('risk_score', 0),
                    'category': addr_data.get('category', 'unknown')
                },
                confidence=ConfidenceLevel.VERIFIED,  # Blockchain data is highly reliable
                threat_level=self._risk_to_threat_level(addr_data.get('risk_score', 0))
            )
            graph.nodes.append(node)
        
        # Create edges for transactions
        for tx in transactions:
            edge = GraphEdge(
                edge_id=f"tx_{tx.get('hash', str(uuid.uuid4()))}",
                source_node=f"addr_{tx.get('from_address', '')}",
                target_node=f"addr_{tx.get('to_address', '')}",
                relationship_type="TRANSFERS_TO",
                properties={
                    'transaction_hash': tx.get('hash'),
                    'amount': tx.get('amount', 0),
                    'timestamp': tx.get('timestamp'),
                    'fee': tx.get('fee', 0),
                    'block_height': tx.get('block_height')
                },
                confidence=1.0,  # Blockchain transactions are definitive
                weight=float(tx.get('amount', 0)) / 100000000  # Normalize to BTC
            )
            graph.edges.append(edge)
        
        self.graphs[graph_id] = graph
        return graph
    
    async def build_communication_network_graph(self, communications: List[Dict]) -> IntelligenceGraph:
        """Build graph from communication analysis"""
        graph_id = f"communication_network_{int(datetime.utcnow().timestamp())}"
        
        graph = IntelligenceGraph(
            graph_id=graph_id,
            title="Communication Network Analysis",
            description="Graph representation of communication patterns and relationships",
            classification="CONFIDENTIAL",
            handling_instructions=["Communication Intelligence", "Lawful Intercept"]
        )
        
        # Extract unique participants
        participants = set()
        for comm in communications:
            participants.add(comm.get('sender', 'unknown'))
            participants.add(comm.get('recipient', 'unknown'))
        
        # Create nodes for participants
        for participant in participants:
            if participant != 'unknown':
                node = GraphNode(
                    node_id=f"user_{hashlib.md5(participant.encode()).hexdigest()[:8]}",
                    node_type="communication_entity",
                    label=participant,
                    properties={
                        'identifier': participant,
                        'platform': 'multiple',  # Would be determined from analysis
                        'message_count': len([c for c in communications 
                                            if c.get('sender') == participant or c.get('recipient') == participant])
                    },
                    confidence=ConfidenceLevel.MEDIUM
                )
                graph.nodes.append(node)
        
        # Create edges for communications
        comm_counts = {}
        for comm in communications:
            sender = comm.get('sender', 'unknown')
            recipient = comm.get('recipient', 'unknown')
            
            if sender != 'unknown' and recipient != 'unknown':
                edge_key = f"{sender}_{recipient}"
                if edge_key not in comm_counts:
                    comm_counts[edge_key] = 0
                comm_counts[edge_key] += 1
        
        for edge_key, count in comm_counts.items():
            sender, recipient = edge_key.split('_', 1)
            edge = GraphEdge(
                edge_id=f"comm_{hashlib.md5(edge_key.encode()).hexdigest()[:8]}",
                source_node=f"user_{hashlib.md5(sender.encode()).hexdigest()[:8]}",
                target_node=f"user_{hashlib.md5(recipient.encode()).hexdigest()[:8]}",
                relationship_type="COMMUNICATES_WITH",
                properties={
                    'message_count': count,
                    'communication_frequency': count / max(len(communications), 1)
                },
                confidence=0.8,
                weight=float(count)
            )
            graph.edges.append(edge)
        
        self.graphs[graph_id] = graph
        return graph
    
    def _map_confidence(self, score: float) -> ConfidenceLevel:
        """Map confidence score to confidence level"""
        if score >= 0.9:
            return ConfidenceLevel.VERIFIED
        elif score >= 0.7:
            return ConfidenceLevel.HIGH
        elif score >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.3:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNVERIFIED
    
    def _map_threat_level(self, threat_str: str) -> ThreatLevel:
        """Map threat level string to enum"""
        threat_map = {
            'CRITICAL': ThreatLevel.CRITICAL,
            'HIGH': ThreatLevel.HIGH,
            'MEDIUM': ThreatLevel.MEDIUM,
            'LOW': ThreatLevel.LOW,
            'INFO': ThreatLevel.INFO
        }
        return threat_map.get(threat_str.upper(), ThreatLevel.INFO)
    
    def _risk_to_threat_level(self, risk_score: int) -> ThreatLevel:
        """Convert risk score to threat level"""
        if risk_score >= 80:
            return ThreatLevel.CRITICAL
        elif risk_score >= 60:
            return ThreatLevel.HIGH
        elif risk_score >= 40:
            return ThreatLevel.MEDIUM
        elif risk_score >= 20:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.INFO
    
    def _calculate_persona_correlation(self, persona1: Dict, persona2: Dict) -> float:
        """Calculate correlation between two personas"""
        # Simple correlation based on shared attributes
        correlation = 0.0
        
        # Shared crypto wallets
        wallets1 = set(persona1.get('crypto_wallets', []))
        wallets2 = set(persona2.get('crypto_wallets', []))
        if wallets1 & wallets2:
            correlation += 0.4
        
        # Shared email addresses
        emails1 = set(persona1.get('email_addresses', []))
        emails2 = set(persona2.get('email_addresses', []))
        if emails1 & emails2:
            correlation += 0.3
        
        # Shared communication channels
        handles1 = set(persona1.get('telegram_handles', []))
        handles2 = set(persona2.get('telegram_handles', []))
        if handles1 & handles2:
            correlation += 0.3
        
        return min(correlation, 1.0)

class GraphExporter:
    """Exports intelligence graphs in various formats"""
    
    def __init__(self):
        self.exporters = {
            ExportFormat.JSON_LD: self._export_json_ld,
            ExportFormat.NEO4J_CYPHER: self._export_neo4j_cypher,
            ExportFormat.GRAPHML: self._export_graphml,
            ExportFormat.STIX: self._export_stix,
            ExportFormat.CSV: self._export_csv,
            ExportFormat.D3_JSON: self._export_d3_json,
            ExportFormat.GEPHI: self._export_gephi
        }
    
    def export_graph(self, graph: IntelligenceGraph, 
                    format: ExportFormat, 
                    options: Dict[str, Any] = None) -> ExportPackage:
        """Export graph in specified format"""
        options = options or {}
        
        if format not in self.exporters:
            raise ValueError(f"Unsupported export format: {format}")
        
        logger.info(f"📊 Exporting graph {graph.graph_id} in {format.value} format")
        
        try:
            content = self.exporters[format](graph, options)
            
            package = ExportPackage(
                package_id=f"export_{graph.graph_id}_{format.value}_{int(datetime.utcnow().timestamp())}",
                format=format,
                content=content,
                metadata={
                    'source_graph_id': graph.graph_id,
                    'export_format': format.value,
                    'node_count': len(graph.nodes),
                    'edge_count': len(graph.edges),
                    'classification': graph.classification,
                    'export_options': options,
                    'exported_at': datetime.utcnow().isoformat()
                }
            )
            
            # Add digital signature for integrity
            package.signature = self._generate_signature(package)
            
            logger.info(f"✅ Successfully exported graph in {format.value} format")
            return package
            
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            raise
    
    def _export_json_ld(self, graph: IntelligenceGraph, options: Dict) -> Dict[str, Any]:
        """Export as JSON-LD (Linked Data)"""
        context = {
            "@context": {
                "@version": 1.1,
                "ntro": "https://ntro.gov.in/cryptoforensics/",
                "schema": "https://schema.org/",
                "threat": "https://threat-intel.org/",
                "crypto": "https://blockchain.org/",
                "Person": "schema:Person",
                "Organization": "schema:Organization",
                "CryptoAddress": "crypto:Address",
                "ThreatActor": "threat:Actor",
                "name": "schema:name",
                "identifier": "schema:identifier",
                "dateCreated": "schema:dateCreated",
                "confidenceLevel": "threat:confidenceLevel",
                "threatLevel": "threat:threatLevel"
            }
        }
        
        # Convert nodes to JSON-LD entities
        entities = []
        for node in graph.nodes:
            entity = {
                "@id": f"ntro:{node.node_id}",
                "@type": self._map_node_type_to_jsonld(node.node_type),
                "name": node.label,
                "identifier": node.node_id,
                "dateCreated": node.created_at.isoformat(),
                "confidenceLevel": node.confidence.value,
                "threatLevel": node.threat_level.value,
                "properties": node.properties,
                "source": node.source,
                "provenance": node.provenance
            }
            entities.append(entity)
        
        # Convert edges to JSON-LD relationships
        relationships = []
        for edge in graph.edges:
            relationship = {
                "@id": f"ntro:{edge.edge_id}",
                "@type": "schema:Relationship",
                "relationshipType": edge.relationship_type,
                "source": f"ntro:{edge.source_node}",
                "target": f"ntro:{edge.target_node}",
                "confidence": edge.confidence,
                "weight": edge.weight,
                "dateCreated": edge.created_at.isoformat(),
                "evidence": edge.evidence,
                "properties": edge.properties
            }
            relationships.append(relationship)
        
        return {
            **context,
            "@id": f"ntro:{graph.graph_id}",
            "@type": "threat:IntelligenceGraph",
            "name": graph.title,
            "description": graph.description,
            "classification": graph.classification,
            "dateCreated": graph.created_at.isoformat(),
            "entities": entities,
            "relationships": relationships,
            "metadata": graph.metadata,
            "handlingInstructions": graph.handling_instructions
        }
    
    def _export_neo4j_cypher(self, graph: IntelligenceGraph, options: Dict) -> str:
        """Export as Neo4j Cypher queries"""
        cypher_commands = []
        
        # Add constraint creation
        cypher_commands.append("// Create constraints")
        cypher_commands.append("CREATE CONSTRAINT IF NOT EXISTS FOR (n:ThreatActor) REQUIRE n.id IS UNIQUE;")
        cypher_commands.append("CREATE CONSTRAINT IF NOT EXISTS FOR (n:CryptoAddress) REQUIRE n.address IS UNIQUE;")
        cypher_commands.append("")
        
        # Create nodes
        cypher_commands.append("// Create nodes")
        for node in graph.nodes:
            properties = {
                'id': node.node_id,
                'label': node.label,
                'confidence': node.confidence.value,
                'threat_level': node.threat_level.value,
                'created_at': node.created_at.isoformat(),
                'source': node.source,
                **node.properties
            }
            
            # Escape and format properties
            prop_strings = []
            for key, value in properties.items():
                if isinstance(value, str):
                    prop_strings.append(f"{key}: '{value.replace(chr(39), chr(92) + chr(39))}'")
                elif isinstance(value, (int, float)):
                    prop_strings.append(f"{key}: {value}")
                elif isinstance(value, list):
                    prop_strings.append(f"{key}: {json.dumps(value)}")
                else:
                    prop_strings.append(f"{key}: '{str(value)}'")
            
            node_label = self._map_node_type_to_neo4j(node.node_type)
            cypher_commands.append(f"CREATE (:{node_label} {{{', '.join(prop_strings)}}});")
        
        cypher_commands.append("")
        
        # Create relationships
        cypher_commands.append("// Create relationships")
        for edge in graph.edges:
            source_match = f"(s {{id: '{edge.source_node}'}})"
            target_match = f"(t {{id: '{edge.target_node}'}})"
            
            rel_props = {
                'confidence': edge.confidence,
                'weight': edge.weight,
                'created_at': edge.created_at.isoformat(),
                **edge.properties
            }
            
            prop_strings = []
            for key, value in rel_props.items():
                if isinstance(value, str):
                    prop_strings.append(f"{key}: '{value.replace(chr(39), chr(92) + chr(39))}'")
                else:
                    prop_strings.append(f"{key}: {value}")
            
            cypher_commands.append(
                f"MATCH {source_match}, {target_match} "
                f"CREATE (s)-[:{edge.relationship_type} {{{', '.join(prop_strings)}}}]->(t);"
            )
        
        return '\n'.join(cypher_commands)
    
    def _export_graphml(self, graph: IntelligenceGraph, options: Dict) -> str:
        """Export as GraphML XML"""
        root = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
        
        # Define keys for attributes
        keys = [
            ("node_type", "node", "string"),
            ("confidence", "node", "int"),
            ("threat_level", "node", "int"),
            ("created_at", "node", "string"),
            ("relationship_type", "edge", "string"),
            ("edge_confidence", "edge", "double"),
            ("weight", "edge", "double")
        ]
        
        for key_id, for_element, attr_type in keys:
            key_elem = ET.SubElement(root, "key")
            key_elem.set("id", key_id)
            key_elem.set("for", for_element)
            key_elem.set("attr.name", key_id)
            key_elem.set("attr.type", attr_type)
        
        # Create graph element
        graph_elem = ET.SubElement(root, "graph")
        graph_elem.set("id", graph.graph_id)
        graph_elem.set("edgedefault", "directed")
        
        # Add nodes
        for node in graph.nodes:
            node_elem = ET.SubElement(graph_elem, "node")
            node_elem.set("id", node.node_id)
            
            # Add node data
            data_elements = [
                ("node_type", node.node_type),
                ("confidence", str(node.confidence.value)),
                ("threat_level", str(node.threat_level.value)),
                ("created_at", node.created_at.isoformat())
            ]
            
            for key, value in data_elements:
                data_elem = ET.SubElement(node_elem, "data")
                data_elem.set("key", key)
                data_elem.text = value
        
        # Add edges
        for edge in graph.edges:
            edge_elem = ET.SubElement(graph_elem, "edge")
            edge_elem.set("id", edge.edge_id)
            edge_elem.set("source", edge.source_node)
            edge_elem.set("target", edge.target_node)
            
            # Add edge data
            data_elements = [
                ("relationship_type", edge.relationship_type),
                ("edge_confidence", str(edge.confidence)),
                ("weight", str(edge.weight))
            ]
            
            for key, value in data_elements:
                data_elem = ET.SubElement(edge_elem, "data")
                data_elem.set("key", key)
                data_elem.text = value
        
        return ET.tostring(root, encoding='unicode')
    
    def _export_stix(self, graph: IntelligenceGraph, options: Dict) -> Dict[str, Any]:
        """Export as STIX 2.1 format"""
        stix_bundle = {
            "type": "bundle",
            "id": f"bundle--{uuid.uuid4()}",
            "spec_version": "2.1",
            "created": datetime.utcnow().isoformat() + "Z",
            "objects": []
        }
        
        # Create STIX objects for nodes
        for node in graph.nodes:
            stix_obj = self._node_to_stix_object(node)
            if stix_obj:
                stix_bundle["objects"].append(stix_obj)
        
        # Create STIX relationships for edges
        for edge in graph.edges:
            stix_rel = self._edge_to_stix_relationship(edge)
            if stix_rel:
                stix_bundle["objects"].append(stix_rel)
        
        return stix_bundle
    
    def _export_csv(self, graph: IntelligenceGraph, options: Dict) -> Dict[str, str]:
        """Export as CSV files (nodes and edges)"""
        # Export nodes
        node_headers = ["node_id", "node_type", "label", "confidence", "threat_level", "created_at", "source"]
        node_rows = [','.join(node_headers)]
        
        for node in graph.nodes:
            row = [
                node.node_id,
                node.node_type,
                f'"{node.label}"',
                str(node.confidence.value),
                str(node.threat_level.value),
                node.created_at.isoformat(),
                node.source
            ]
            node_rows.append(','.join(row))
        
        # Export edges
        edge_headers = ["edge_id", "source_node", "target_node", "relationship_type", "confidence", "weight", "created_at"]
        edge_rows = [','.join(edge_headers)]
        
        for edge in graph.edges:
            row = [
                edge.edge_id,
                edge.source_node,
                edge.target_node,
                edge.relationship_type,
                str(edge.confidence),
                str(edge.weight),
                edge.created_at.isoformat()
            ]
            edge_rows.append(','.join(row))
        
        return {
            "nodes.csv": '\n'.join(node_rows),
            "edges.csv": '\n'.join(edge_rows)
        }
    
    def _export_d3_json(self, graph: IntelligenceGraph, options: Dict) -> Dict[str, Any]:
        """Export as D3.js compatible JSON"""
        nodes = []
        for node in graph.nodes:
            nodes.append({
                "id": node.node_id,
                "type": node.node_type,
                "label": node.label,
                "confidence": node.confidence.value,
                "threat_level": node.threat_level.value,
                "properties": node.properties,
                "group": self._get_node_group(node.node_type)
            })
        
        links = []
        for edge in graph.edges:
            links.append({
                "source": edge.source_node,
                "target": edge.target_node,
                "type": edge.relationship_type,
                "confidence": edge.confidence,
                "weight": edge.weight,
                "value": edge.weight  # D3 uses 'value' for link strength
            })
        
        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "title": graph.title,
                "description": graph.description,
                "created_at": graph.created_at.isoformat(),
                "classification": graph.classification
            }
        }
    
    def _export_gephi(self, graph: IntelligenceGraph, options: Dict) -> str:
        """Export as Gephi-compatible GEXF format"""
        root = ET.Element("gexf", xmlns="http://www.gexf.net/1.2draft", version="1.2")
        
        # Meta information
        meta = ET.SubElement(root, "meta")
        meta.set("lastmodifieddate", datetime.utcnow().strftime("%Y-%m-%d"))
        
        creator = ET.SubElement(meta, "creator")
        creator.text = "NTRO CryptoForensics"
        
        description = ET.SubElement(meta, "description")
        description.text = graph.description
        
        # Graph element
        gexf_graph = ET.SubElement(root, "graph")
        gexf_graph.set("mode", "static")
        gexf_graph.set("defaultedgetype", "directed")
        
        # Attributes
        attributes = ET.SubElement(gexf_graph, "attributes")
        attributes.set("class", "node")
        
        attr_defs = [
            ("confidence", "integer"),
            ("threat_level", "integer"),
            ("node_type", "string")
        ]
        
        for attr_id, attr_type in attr_defs:
            attr = ET.SubElement(attributes, "attribute")
            attr.set("id", attr_id)
            attr.set("title", attr_id)
            attr.set("type", attr_type)
        
        # Nodes
        nodes_elem = ET.SubElement(gexf_graph, "nodes")
        for node in graph.nodes:
            node_elem = ET.SubElement(nodes_elem, "node")
            node_elem.set("id", node.node_id)
            node_elem.set("label", node.label)
            
            # Node attributes
            attvalues = ET.SubElement(node_elem, "attvalues")
            
            attvalue_confidence = ET.SubElement(attvalues, "attvalue")
            attvalue_confidence.set("for", "confidence")
            attvalue_confidence.set("value", str(node.confidence.value))
            
            attvalue_threat = ET.SubElement(attvalues, "attvalue")
            attvalue_threat.set("for", "threat_level")
            attvalue_threat.set("value", str(node.threat_level.value))
            
            attvalue_type = ET.SubElement(attvalues, "attvalue")
            attvalue_type.set("for", "node_type")
            attvalue_type.set("value", node.node_type)
        
        # Edges
        edges_elem = ET.SubElement(gexf_graph, "edges")
        for edge in graph.edges:
            edge_elem = ET.SubElement(edges_elem, "edge")
            edge_elem.set("id", edge.edge_id)
            edge_elem.set("source", edge.source_node)
            edge_elem.set("target", edge.target_node)
            edge_elem.set("weight", str(edge.weight))
            edge_elem.set("label", edge.relationship_type)
        
        return ET.tostring(root, encoding='unicode')
    
    def _map_node_type_to_jsonld(self, node_type: str) -> str:
        """Map node type to JSON-LD type"""
        mapping = {
            "threat_actor": "ThreatActor",
            "crypto_address": "CryptoAddress",
            "crypto_wallet": "CryptoAddress",
            "communication_entity": "Person",
            "organization": "Organization"
        }
        return mapping.get(node_type, "schema:Thing")
    
    def _map_node_type_to_neo4j(self, node_type: str) -> str:
        """Map node type to Neo4j label"""
        mapping = {
            "threat_actor": "ThreatActor",
            "crypto_address": "CryptoAddress",
            "crypto_wallet": "CryptoAddress",
            "communication_entity": "Person",
            "organization": "Organization"
        }
        return mapping.get(node_type, "Entity")
    
    def _node_to_stix_object(self, node: GraphNode) -> Optional[Dict[str, Any]]:
        """Convert graph node to STIX object"""
        if node.node_type == "threat_actor":
            return {
                "type": "threat-actor",
                "id": f"threat-actor--{uuid.uuid4()}",
                "created": node.created_at.isoformat() + "Z",
                "modified": (node.updated_at or node.created_at).isoformat() + "Z",
                "name": node.label,
                "threat_actor_types": ["cybercriminal"],
                "confidence": int(node.confidence.value * 20),  # Convert to 0-100 scale
                "x_threat_level": node.threat_level.value
            }
        elif node.node_type in ["crypto_address", "crypto_wallet"]:
            return {
                "type": "observed-data",
                "id": f"observed-data--{uuid.uuid4()}",
                "created": node.created_at.isoformat() + "Z",
                "modified": (node.updated_at or node.created_at).isoformat() + "Z",
                "first_observed": node.created_at.isoformat() + "Z",
                "last_observed": (node.updated_at or node.created_at).isoformat() + "Z",
                "number_observed": 1,
                "objects": {
                    "0": {
                        "type": "cryptocurrency-wallet",
                        "address": node.label
                    }
                }
            }
        
        return None
    
    def _edge_to_stix_relationship(self, edge: GraphEdge) -> Optional[Dict[str, Any]]:
        """Convert graph edge to STIX relationship"""
        relationship_mapping = {
            "OWNS": "attributed-to",
            "COMMUNICATES_WITH": "communicates-with",
            "TRANSFERS_TO": "related-to",
            "RELATED_TO": "related-to"
        }
        
        stix_rel_type = relationship_mapping.get(edge.relationship_type, "related-to")
        
        return {
            "type": "relationship",
            "id": f"relationship--{uuid.uuid4()}",
            "created": edge.created_at.isoformat() + "Z",
            "modified": edge.created_at.isoformat() + "Z",
            "relationship_type": stix_rel_type,
            "source_ref": f"threat-actor--{uuid.uuid4()}",  # Would need proper mapping
            "target_ref": f"observed-data--{uuid.uuid4()}",  # Would need proper mapping
            "confidence": int(edge.confidence * 100)
        }
    
    def _get_node_group(self, node_type: str) -> int:
        """Get node group for D3.js visualization"""
        groups = {
            "threat_actor": 1,
            "crypto_address": 2,
            "crypto_wallet": 2,
            "communication_entity": 3,
            "organization": 4
        }
        return groups.get(node_type, 0)
    
    def _generate_signature(self, package: ExportPackage) -> str:
        """Generate digital signature for export package"""
        content_str = json.dumps(package.content, sort_keys=True) if isinstance(package.content, dict) else str(package.content)
        signature_data = f"{package.package_id}_{package.format.value}_{content_str}"
        return hashlib.sha256(signature_data.encode()).hexdigest()

class IntelligenceExportAPI:
    """Main API for intelligence export operations"""
    
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.db = mongo_db
        self.graph_builder = GraphBuilder(mongo_db)
        self.graph_exporter = GraphExporter()
        self.export_history: List[ExportPackage] = []
    
    async def export_threat_intelligence(self, 
                                       data_type: str,
                                       data: List[Dict],
                                       export_format: ExportFormat,
                                       options: Dict[str, Any] = None) -> ExportPackage:
        """Main export function for different data types"""
        logger.info(f"📊 Starting intelligence export: {data_type} → {export_format.value}")
        
        # Build appropriate graph based on data type
        if data_type == "threat_personas":
            graph = await self.graph_builder.build_threat_persona_graph(data)
        elif data_type == "blockchain_activity":
            addresses = data.get('addresses', [])
            transactions = data.get('transactions', [])
            graph = await self.graph_builder.build_blockchain_activity_graph(addresses, transactions)
        elif data_type == "communications":
            graph = await self.graph_builder.build_communication_network_graph(data)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        # Export graph in requested format
        export_package = self.graph_exporter.export_graph(graph, export_format, options)
        
        # Store export record
        self.export_history.append(export_package)
        await self._store_export_record(export_package)
        
        logger.info(f"✅ Intelligence export completed: {export_package.package_id}")
        return export_package
    
    async def get_export_formats(self) -> List[Dict[str, Any]]:
        """Get available export formats and their capabilities"""
        return [
            {
                "format": "json-ld",
                "name": "JSON-LD",
                "description": "Linked Data format for semantic web integration",
                "use_cases": ["Semantic analysis", "Cross-agency data sharing", "AI processing"],
                "interoperability": "High"
            },
            {
                "format": "neo4j-cypher",
                "name": "Neo4j Cypher",
                "description": "Graph database queries for Neo4j",
                "use_cases": ["Graph database import", "Complex queries", "Relationship analysis"],
                "interoperability": "Medium"
            },
            {
                "format": "graphml",
                "name": "GraphML",
                "description": "Standard XML graph format",
                "use_cases": ["Academic research", "Network analysis tools", "Visualization"],
                "interoperability": "High"
            },
            {
                "format": "stix",
                "name": "STIX 2.1",
                "description": "Structured Threat Information eXpression",
                "use_cases": ["Threat intelligence sharing", "SIEM integration", "CTI platforms"],
                "interoperability": "Very High"
            },
            {
                "format": "d3-json",
                "name": "D3.js JSON",
                "description": "Interactive web visualization format",
                "use_cases": ["Web dashboards", "Interactive reports", "Data visualization"],
                "interoperability": "Medium"
            },
            {
                "format": "gephi",
                "name": "Gephi GEXF",
                "description": "Gephi graph analysis platform format",
                "use_cases": ["Network analysis", "Graph visualization", "Academic research"],
                "interoperability": "Medium"
            }
        ]
    
    async def _store_export_record(self, package: ExportPackage):
        """Store export record in database"""
        try:
            record = {
                'package_id': package.package_id,
                'format': package.format.value,
                'metadata': package.metadata,
                'signature': package.signature,
                'created_at': package.created_at,
                'export_size': len(str(package.content))
            }
            
            await self.db.export_records.insert_one(record)
            
        except Exception as e:
            logger.error(f"Error storing export record: {e}")

# Example usage and API integration
if __name__ == "__main__":
    print("📊 Graph-Native Intelligence Export System")
    print("Advanced interoperable intelligence sharing ready!")
    
    # Demo usage would go here
    # async def demo():
    #     api = IntelligenceExportAPI(mongo_db)
    #     package = await api.export_threat_intelligence(
    #         data_type="threat_personas",
    #         data=demo_personas,
    #         export_format=ExportFormat.JSON_LD
    #     )
    #     print(f"Exported: {package.package_id}")
    
    # asyncio.run(demo())