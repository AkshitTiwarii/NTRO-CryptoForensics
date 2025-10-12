"""
Neo4j Graph Database Integration for Cryptocurrency Forensics
Visualizes relationships between addresses, transactions, and entities
"""

import os
import logging
from typing import Dict, List, Optional
from neo4j import GraphDatabase
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoGraphDB:
    """Neo4j graph database manager for cryptocurrency forensics"""
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j bolt URI (default: bolt://localhost:7687)
            user: Database username (default: neo4j)
            password: Database password (default: password)
        """
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = user or os.getenv('NEO4J_USER', 'neo4j')
        self.password = password or os.getenv('NEO4J_PASSWORD', 'password')
        
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ Neo4j connection established")
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            self.driver = None
    
    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()
            logger.info("👋 Neo4j connection closed")
    
    def create_address_node(self, address_data: Dict) -> bool:
        """
        Create or update an address node in the graph
        
        Args:
            address_data: Dictionary with address, crypto_type, category, etc.
            
        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            logger.warning("⚠️ Neo4j not connected - skipping node creation")
            return False
        
        try:
            with self.driver.session() as session:
                # Map 'currency' to 'crypto_type' for Neo4j compatibility
                crypto_type = address_data.get('crypto_type') or address_data.get('currency', 'UNKNOWN')
                
                query = """
                MERGE (a:Address {address: $address})
                SET a.crypto_type = $crypto_type,
                    a.category = $category,
                    a.risk_score = $risk_score,
                    a.balance = $balance,
                    a.total_received = $total_received,
                    a.total_sent = $total_sent,
                    a.first_seen = $first_seen,
                    a.last_seen = $last_seen,
                    a.updated_at = datetime()
                RETURN a
                """
                
                result = session.run(query, 
                    address=address_data.get('address'),
                    crypto_type=crypto_type,
                    category=address_data.get('category', 'unknown'),
                    risk_score=address_data.get('risk_score', 0),
                    balance=address_data.get('balance', 0),
                    total_received=address_data.get('total_received', 0),
                    total_sent=address_data.get('total_sent', 0),
                    first_seen=address_data.get('first_seen', datetime.utcnow().isoformat()),
                    last_seen=address_data.get('last_seen', datetime.utcnow().isoformat())
                )
                
                logger.info(f"✅ Created Neo4j node: {address_data.get('address')[:15]}...")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to create Neo4j node: {e}")
            return False
    
    def create_transaction_relationship(self, from_address: str, to_address: str, 
                                       amount: float, tx_hash: str = None) -> bool:
        """
        Create a transaction relationship between two addresses
        
        Args:
            from_address: Sender address
            to_address: Receiver address
            amount: Transaction amount
            tx_hash: Transaction hash (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            logger.warning("⚠️ Neo4j not connected - skipping relationship")
            return False
        
        try:
            with self.driver.session() as session:
                query = """
                MATCH (a1:Address {address: $from_address})
                MATCH (a2:Address {address: $to_address})
                MERGE (a1)-[r:SENT_TO {tx_hash: $tx_hash}]->(a2)
                SET r.amount = $amount,
                    r.timestamp = datetime()
                RETURN r
                """
                
                session.run(query,
                    from_address=from_address,
                    to_address=to_address,
                    amount=amount,
                    tx_hash=tx_hash or f"tx_{datetime.utcnow().timestamp()}"
                )
                
                logger.info(f"✅ Created transaction: {from_address[:10]}... → {to_address[:10]}...")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to create transaction relationship: {e}")
            return False
    
    def get_address_network(self, address: str, depth: int = 2) -> Dict:
        """
        Get network of addresses connected to a given address
        
        Args:
            address: Center address
            depth: How many hops to traverse
            
        Returns:
            Dictionary with nodes and edges
        """
        if not self.driver:
            return {'nodes': [], 'edges': []}
        
        try:
            with self.driver.session() as session:
                query = """
                MATCH path = (a:Address {address: $address})-[*1..$depth]-(connected)
                WITH collect(path) as paths
                CALL apoc.convert.toTree(paths) YIELD value
                RETURN value
                """
                
                result = session.run(query, address=address, depth=depth)
                record = result.single()
                
                if record:
                    return record['value']
                return {'nodes': [], 'edges': []}
                
        except Exception as e:
            logger.error(f"❌ Failed to get address network: {e}")
            return {'nodes': [], 'edges': []}
    
    def find_clusters(self, min_cluster_size: int = 3) -> List[Dict]:
        """
        Find clusters of connected addresses (potential wallets/entities)
        
        Args:
            min_cluster_size: Minimum number of addresses in a cluster
            
        Returns:
            List of clusters with their addresses
        """
        if not self.driver:
            return []
        
        try:
            with self.driver.session() as session:
                query = """
                CALL gds.louvain.stream('addressGraph')
                YIELD nodeId, communityId
                WITH communityId, collect(gds.util.asNode(nodeId).address) as addresses
                WHERE size(addresses) >= $min_size
                RETURN communityId, addresses, size(addresses) as cluster_size
                ORDER BY cluster_size DESC
                """
                
                result = session.run(query, min_size=min_cluster_size)
                
                clusters = []
                for record in result:
                    clusters.append({
                        'cluster_id': record['communityId'],
                        'addresses': record['addresses'],
                        'size': record['cluster_size']
                    })
                
                logger.info(f"✅ Found {len(clusters)} clusters")
                return clusters
                
        except Exception as e:
            logger.warning(f"⚠️ Cluster detection requires GDS plugin: {e}")
            return []
    
    def get_high_risk_paths(self, from_address: str, to_address: str, 
                           max_hops: int = 5) -> List[Dict]:
        """
        Find paths between two addresses (for tracing funds)
        
        Args:
            from_address: Starting address
            to_address: Destination address
            max_hops: Maximum path length
            
        Returns:
            List of paths with details
        """
        if not self.driver:
            return []
        
        try:
            with self.driver.session() as session:
                query = """
                MATCH path = shortestPath(
                    (a1:Address {address: $from})-[*..$max_hops]->(a2:Address {address: $to})
                )
                RETURN path, length(path) as hops,
                       reduce(total = 0, r in relationships(path) | total + r.amount) as total_amount
                LIMIT 10
                """
                
                result = session.run(query, 
                    **{'from': from_address, 'to': to_address, 'max_hops': max_hops}
                )
                
                paths = []
                for record in result:
                    paths.append({
                        'hops': record['hops'],
                        'total_amount': record['total_amount'],
                        'path': record['path']
                    })
                
                logger.info(f"✅ Found {len(paths)} paths")
                return paths
                
        except Exception as e:
            logger.error(f"❌ Failed to find paths: {e}")
            return []
    
    def get_graph_stats(self) -> Dict:
        """Get overall graph statistics"""
        if not self.driver:
            return {}
        
        try:
            with self.driver.session() as session:
                query = """
                MATCH (a:Address)
                OPTIONAL MATCH ()-[r:SENT_TO]->()
                RETURN count(DISTINCT a) as total_addresses,
                       count(r) as total_transactions,
                       avg(a.risk_score) as avg_risk_score
                """
                
                result = session.run(query)
                record = result.single()
                
                return {
                    'total_addresses': record['total_addresses'],
                    'total_transactions': record['total_transactions'],
                    'avg_risk_score': record['avg_risk_score'] or 0
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get graph stats: {e}")
            return {}


# Testing
if __name__ == "__main__":
    # Initialize database
    db = CryptoGraphDB()
    
    # Test address creation
    test_address = {
        'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Genesis Bitcoin address
        'crypto_type': 'BITCOIN',
        'category': 'genesis',
        'risk_score': 0,
        'balance': 0
    }
    
    db.create_address_node(test_address)
    
    # Get stats
    stats = db.get_graph_stats()
    print(f"\n📊 Graph Stats: {stats}")
    
    # Cleanup
    db.close()
