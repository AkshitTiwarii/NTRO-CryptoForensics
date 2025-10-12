# 🚀 Quick Start: Phase 1 Implementation

## Goal: Multi-Modal Data Fusion with Neo4j

**Time**: 1-2 weeks  
**Priority**: HIGH - This is the foundation for your USP

---

## Step 1: Install Neo4j (5 minutes)

### Using Docker (Recommended):
```powershell
# Pull and run Neo4j container
docker run -d `
  --name neo4j `
  -p 7474:7474 -p 7687:7687 `
  -e NEO4J_AUTH=neo4j/cryptoforensics `
  -v neo4j-data:/data `
  neo4j:latest

# Verify it's running
docker ps | findstr neo4j
```

### Access Neo4j Browser:
1. Open browser: http://localhost:7474
2. Login: `neo4j` / `cryptoforensics`
3. You should see Neo4j Browser UI

---

## Step 2: Install Python Dependencies

```powershell
cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend

# Add to requirements.txt
echo neo4j==5.14.0 >> requirements.txt

# Install
pip install neo4j==5.14.0
```

---

## Step 3: Create Graph Database Module

**File**: `backend/graph_db.py`

```python
from neo4j import GraphDatabase
from typing import List, Dict, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoGraphDB:
    """Neo4j graph database for entity correlation"""
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="cryptoforensics"):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ Neo4j connection established")
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            raise
    
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
                address=address_data.get("address"),
                crypto_type=address_data.get("crypto_type", "unknown"),
                category=address_data.get("category", "unknown"),
                risk_score=address_data.get("risk_score", 0),
                balance=address_data.get("balance", 0.0),
                first_seen=str(address_data.get("first_seen", datetime.now()))
            )
            logger.info(f"✅ Created node for {address_data.get('address')[:16]}...")
    
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
            logger.info(f"✅ Linked {address[:16]}... → {email}")
    
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
            entities = [record.data() for record in result]
            logger.info(f"✅ Found {len(entities)} connected entities")
            return entities
    
    def close(self):
        self.driver.close()
        logger.info("👋 Neo4j connection closed")


# Test function
if __name__ == "__main__":
    # Test the connection
    graph_db = CryptoGraphDB()
    
    # Create test address
    test_address = {
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "crypto_type": "BTC",
        "category": "exchange",
        "risk_score": 25,
        "balance": 0.0,
        "first_seen": datetime.now()
    }
    
    graph_db.create_address_node(test_address)
    
    # Link to email
    graph_db.link_address_to_email(
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "satoshi@example.com",
        confidence=0.8
    )
    
    # Query entity graph
    entities = graph_db.find_entity_graph("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    print(f"\n📊 Entity Graph:")
    for entity in entities:
        print(f"  - {entity['node_type']}: {entity['props']} (distance: {entity['distance']})")
    
    graph_db.close()
    print("\n✅ Test completed successfully!")
```

---

## Step 4: Test the Graph Database

```powershell
cd backend
python graph_db.py
```

**Expected Output**:
```
INFO:__main__:✅ Neo4j connection established
INFO:__main__:✅ Created node for 1A1zP1eP5QGefi2...
INFO:__main__:✅ Linked 1A1zP1eP5QGefi2... → satoshi@example.com
INFO:__main__:✅ Found 1 connected entities

📊 Entity Graph:
  - Email: {'email': 'satoshi@example.com'} (distance: 1)

INFO:__main__:👋 Neo4j connection closed
✅ Test completed successfully!
```

---

## Step 5: Integrate with Existing System

### Update `server.py`:

```python
from graph_db import CryptoGraphDB

# Initialize at startup
graph_db = CryptoGraphDB()

# Add new endpoint
@api_router.get("/analytics/entity-graph/{address}")
async def get_entity_graph(address: str, current_user: dict = Depends(get_current_user)):
    """Get complete entity correlation graph"""
    try:
        entity_graph = graph_db.find_entity_graph(address, max_depth=3)
        return {
            "address": address,
            "entities": entity_graph,
            "total_connections": len(entity_graph),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error getting entity graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Update address creation to sync with Neo4j
@api_router.post("/addresses", response_model=CryptoAddress)
async def create_address_endpoint(
    data: AddressCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new cryptocurrency address with graph sync"""
    # Create in MongoDB (existing code)
    address = CryptoAddress(**data.model_dump())
    result = await db.addresses.insert_one(address.model_dump())
    
    # NEW: Also create in Neo4j
    try:
        graph_db.create_address_node(address.model_dump())
        logger.info(f"✅ Synced to Neo4j: {address.address}")
    except Exception as e:
        logger.error(f"Neo4j sync failed: {e}")
    
    return address
```

---

## Step 6: Verify in Neo4j Browser

1. Go to http://localhost:7474
2. Run this query:
```cypher
MATCH (a:CryptoAddress)-[r]-(e)
RETURN a, r, e
LIMIT 25
```

You should see a visual graph of addresses and connected entities!

---

## Step 7: Automatic PII Extraction & Linking

### Update `crypto_collector.py` to auto-link entities:

```python
from graph_db import CryptoGraphDB

class CryptocurrencyAddressCollector:
    def __init__(self):
        # ... existing code ...
        self.graph_db = CryptoGraphDB()
    
    async def collect_and_link(self, source_url: str, html_content: str):
        """Collect addresses and automatically link to PII"""
        addresses = self.extract_addresses(html_content)
        pii_data = self.extract_pii(html_content)
        
        for addr in addresses:
            # Create in MongoDB
            await db.addresses.insert_one(addr)
            
            # Create in Neo4j
            self.graph_db.create_address_node(addr)
            
            # Link to any emails found nearby
            for email in pii_data.get('emails', []):
                self.graph_db.link_address_to_email(
                    addr['address'], 
                    email, 
                    confidence=0.6  # Medium confidence
                )
                logger.info(f"🔗 Linked {addr['address'][:16]}... → {email}")
```

---

## Step 8: Visualize in Frontend

### Add new component: `frontend/src/components/EntityGraph.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import { Network } from 'lucide-react';
import api from '../services/api';

function EntityGraph({ address }) {
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (address) {
      loadEntityGraph();
    }
  }, [address]);

  const loadEntityGraph = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/analytics/entity-graph/${address}`);
      setEntities(response.data.entities);
    } catch (error) {
      console.error('Error loading entity graph:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-slate-400">Loading entity graph...</div>;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <Network className="w-5 h-5 text-purple-400" />
        <h3 className="text-lg font-semibold text-white">Entity Correlation Graph</h3>
      </div>

      <div className="space-y-3">
        {entities.length === 0 ? (
          <p className="text-slate-500 text-sm">No connected entities found</p>
        ) : (
          entities.map((entity, idx) => (
            <div key={idx} className="bg-slate-800 rounded-md p-3 border border-slate-700">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs text-purple-400 font-medium">{entity.node_type}</span>
                  <p className="text-sm text-white mt-1">
                    {JSON.stringify(entity.props, null, 2)}
                  </p>
                </div>
                <div className="text-xs text-slate-400">
                  Distance: {entity.distance}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-4 p-3 bg-blue-900/20 border border-blue-800 rounded-md">
        <p className="text-xs text-blue-300">
          💡 <strong>Multi-Modal Fusion:</strong> This graph shows connections across blockchain addresses, 
          emails, usernames, and forum profiles — giving you cross-surface correlation.
        </p>
      </div>
    </div>
  );
}

export default EntityGraph;
```

---

## Step 9: Test End-to-End

1. **Start Backend**:
```powershell
cd backend
python server.py
```

2. **Start Frontend**:
```powershell
cd frontend
npm start
```

3. **Create Test Address** (via API or UI):
   - Address: `1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2`
   - Add email in notes: `criminal@darkweb.onion`

4. **Check Neo4j**:
```cypher
MATCH (a:CryptoAddress {address: "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"})-[r]-(e)
RETURN a, r, e
```

5. **View in Frontend**: Entity graph should show the address linked to email!

---

## ✅ Success Criteria

You've successfully implemented Phase 1 if:

- ✅ Neo4j running on Docker
- ✅ `graph_db.py` connects successfully
- ✅ Addresses sync to both MongoDB AND Neo4j
- ✅ API endpoint `/analytics/entity-graph/{address}` works
- ✅ PII automatically linked to addresses
- ✅ Frontend displays entity connections
- ✅ Neo4j Browser shows visual graph

---

## 🎯 Next Steps

Once Phase 1 is working:

1. **Week 2**: Implement adaptive crawler (Phase 2)
2. **Week 3**: Add threat persona generator (Phase 3)
3. **Week 4**: Build explainable AI (Phase 4)
4. **Week 5**: Real-time leak monitoring (Phase 5)
5. **Week 6**: Graph export (Phase 6)

---

## 🚨 Common Issues & Fixes

### Neo4j won't start:
```powershell
# Check if port is in use
netstat -an | findstr 7474

# Remove old container
docker rm -f neo4j

# Start fresh
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/cryptoforensics neo4j:latest
```

### Connection timeout:
- Wait 30 seconds for Neo4j to fully start
- Check `docker logs neo4j`

### Import errors:
```powershell
pip install --upgrade neo4j
```

---

**Ready to build your "Autonomous Intelligence Correlation Engine"! Start with Phase 1 this week! 🚀**
