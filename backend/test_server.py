from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(__file__))

# Import our custom modules
try:
    from crypto_collector import CryptocurrencyAddressCollector, ScraperJobManager
    from ml_categorizer import AddressCategorizer, AddressClusterer
    from blockchair_api import BlockchairAPI
    ADVANCED_FEATURES = True
except ImportError as e:
    ADVANCED_FEATURES = False
    print(f"Warning: Advanced features not available: {e}")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database (for testing only)
users_db = {}
addresses_db = []
scraper_jobs = []

# Initialize advanced features if available
if ADVANCED_FEATURES:
    collector = CryptocurrencyAddressCollector()
    job_manager = ScraperJobManager()
    categorizer = AddressCategorizer()
    clusterer = AddressClusterer()
    blockchair = BlockchairAPI()  # Initialize Blockchair API

JWT_SECRET = "test-secret-key-for-development"
JWT_ALGORITHM = "HS256"

# Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: dict
    user: dict

class User(BaseModel):
    id: str
    username: str
    email: str
    role: str = "analyst"

class AddressCreate(BaseModel):
    address: str
    crypto_type: str
    category: Optional[str] = None
    source_url: Optional[str] = None
    tags: List[str] = []
    notes: Optional[str] = None

class ScraperJobConfig(BaseModel):
    sources: List[str]
    crypto_types: Optional[List[str]] = None
    
class AddressAnalysisRequest(BaseModel):
    address: str
    crypto_type: str

# Helper functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, username: str) -> str:
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        
        # Find user by user_id
        for username, user_data in users_db.items():
            if user_data['id'] == payload['user_id']:
                return user_data
        
        raise HTTPException(status_code=401, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Routes
@app.get("/api")
async def root():
    return {"message": "Crypto Forensics API - Test Server", "version": "1.0.0-test"}

@app.post("/api/auth/signup")
async def signup(user_data: UserCreate):
    if user_data.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = str(len(users_db) + 1)
    users_db[user_data.username] = {
        'id': user_id,
        'username': user_data.username,
        'email': user_data.email,
        'password': hash_password(user_data.password),
        'role': 'analyst',
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    
    token = create_token(user_id, user_data.username)
    user = {
        'id': user_id,
        'username': user_data.username,
        'email': user_data.email,
        'role': 'analyst'
    }
    
    return {"token": token, "user": user}

@app.post("/api/auth/login")
async def login(credentials: UserLogin):
    user = users_db.get(credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user['id'], user['username'])
    user_data = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role']
    }
    
    return {"token": token, "user": user_data}

@app.get("/api/auth/me")
async def get_me(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    # Remove password from response
    return {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'role': user['role'],
        'created_at': user['created_at']
    }

@app.get("/api/analytics/dashboard")
async def get_dashboard():
    return {
        "total_addresses": len(addresses_db),
        "high_risk_addresses": 0,
        "watched_addresses": 0,
        "recent_activity": []
    }

@app.get("/api/addresses")
async def get_addresses():
    return addresses_db

@app.get("/api/analytics/categories")
async def get_categories():
    category_counts = {}
    for addr in addresses_db:
        cat = addr.get('category', 'unknown')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return category_counts

@app.post("/api/addresses")
async def create_address(address_data: AddressCreate, authorization: Optional[str] = Header(None)):
    """Add a new cryptocurrency address"""
    try:
        # Verify authentication
        get_current_user(authorization)
        
        # Check if address exists
        existing = next((a for a in addresses_db if a['address'] == address_data.address), None)
        if existing:
            raise HTTPException(status_code=400, detail="Address already exists")
        
        new_address = {
            'id': str(len(addresses_db) + 1),
            'address': address_data.address,
            'crypto_type': address_data.crypto_type,
            'category': address_data.category or 'unknown',
            'source_url': address_data.source_url,
            'tags': address_data.tags,
            'notes': address_data.notes,
            'risk_score': 0.0,
            'first_seen': datetime.now(timezone.utc).isoformat(),
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'is_watched': False
        }
        
        # Use ML categorizer if available
        if ADVANCED_FEATURES and not address_data.category:
            categorization = categorizer.categorize_address({
                'context': address_data.notes or '',
                'source_url': address_data.source_url or ''
            })
            new_address['category'] = categorization['category']
            new_address['risk_score'] = categorizer.calculate_risk_score(new_address, categorization['category'])
        
        addresses_db.append(new_address)
        
        return new_address
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/addresses/{address_id}")
async def get_address_detail(address_id: str, authorization: Optional[str] = Header(None)):
    """Get detailed information about a specific address"""
    try:
        get_current_user(authorization)
        
        address = next((a for a in addresses_db if a['id'] == address_id), None)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        
        # Add additional analysis if available
        if ADVANCED_FEATURES:
            related = clusterer.find_related_addresses(address['address'], addresses_db)
            address['related_addresses'] = related[:10]  # Limit to 10
        
        return address
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scraper/start")
async def start_scraper(job_config: ScraperJobConfig, background_tasks: BackgroundTasks, 
                       authorization: Optional[str] = Header(None)):
    """Start a new scraping job"""
    try:
        get_current_user(authorization)
        
        if not ADVANCED_FEATURES:
            raise HTTPException(status_code=501, detail="Advanced scraping features not available")
        
        # Start scraping job
        job_id = await job_manager.start_scraping_job(job_config.dict())
        
        return {
            'success': True,
            'job_id': job_id,
            'message': 'Scraping job started'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scraper/jobs")
async def get_scraper_jobs(authorization: Optional[str] = Header(None)):
    """Get all scraping jobs"""
    try:
        get_current_user(authorization)
        
        if not ADVANCED_FEATURES:
            return []
        
        jobs = job_manager.get_all_jobs()
        return jobs
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scraper/jobs/{job_id}")
async def get_scraper_job_status(job_id: str, authorization: Optional[str] = Header(None)):
    """Get status of a specific scraping job"""
    try:
        get_current_user(authorization)
        
        if not ADVANCED_FEATURES:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = job_manager.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/addresses/analyze")
async def analyze_address(request: AddressAnalysisRequest, authorization: Optional[str] = Header(None)):
    """Analyze a cryptocurrency address using Blockchair API and ML"""
    try:
        get_current_user(authorization)
        
        if not ADVANCED_FEATURES:
            raise HTTPException(status_code=501, detail="Analysis features not available")
        
        # Use Blockchair API for comprehensive data
        blockchain_data = await blockchair.get_address_info(request.address, request.crypto_type)
        transactions = await blockchair.get_transactions(request.address, request.crypto_type, limit=100)
        stats = await blockchair.get_address_stats(request.address, request.crypto_type)
        
        # Get ERC-20 tokens for Ethereum addresses
        erc20_tokens = []
        if request.crypto_type.lower() == 'ethereum':
            erc20_tokens = await blockchair.get_erc20_tokens(request.address)
        
        # Categorize using ML
        address_data = {
            'address': request.address,
            'crypto_type': request.crypto_type,
            'tx_count': blockchain_data.get('transaction_count', 0),
            'balance': blockchain_data.get('balance', 0),
            'total_received': blockchain_data.get('received', 0),
            'total_sent': blockchain_data.get('spent', 0),
            'context': f"Transaction count: {blockchain_data.get('transaction_count', 0)}"
        }
        
        categorization = categorizer.categorize_address(address_data)
        risk_score = categorizer.calculate_risk_score(address_data, categorization['category'])
        
        # Analyze transaction patterns
        pattern_analysis = categorizer.analyze_transaction_pattern(transactions) if transactions else {}
        
        return {
            'address': request.address,
            'crypto_type': request.crypto_type,
            'blockchain_data': blockchain_data,
            'statistics': stats,
            'transactions_analyzed': len(transactions),
            'erc20_tokens': erc20_tokens,
            'category': categorization['category'],
            'confidence': categorization['confidence'],
            'risk_score': risk_score,
            'pattern_analysis': pattern_analysis,
            'alternative_categories': categorization.get('alternative_categories', [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/addresses/search")
async def search_addresses_api(query: str, blockchain: Optional[str] = None, 
                               authorization: Optional[str] = Header(None)):
    """Search for addresses across blockchains using Blockchair"""
    try:
        get_current_user(authorization)
        
        if not ADVANCED_FEATURES:
            raise HTTPException(status_code=501, detail="Search features not available")
        
        results = await blockchair.search_addresses(query, blockchain)
        
        return {
            'success': True,
            'query': query,
            'blockchain': blockchain or 'all',
            'results': results,
            'count': len(results)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
