from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Logging configuration (must be before lifespan function)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: MongoDB is already connected
    logger.info("🚀 Application startup - MongoDB connected")
    yield
    # Shutdown: Close MongoDB connection
    client.close()
    logger.info("👋 Application shutdown - MongoDB disconnected")

# Create the main app with lifespan
app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

# ==================== MODELS ====================

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    role: str = "analyst"  # analyst, admin
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    user: User

class CryptoAddress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    address: str
    crypto_type: str  # BTC, ETH, XRP, LTC, etc.
    category: Optional[str] = None  # ransomware, darknet, laundering, etc.
    source_url: Optional[str] = None
    source_type: Optional[str] = None  # forum, news, social_media, etc.
    balance: Optional[float] = None
    transaction_count: Optional[int] = 0
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    risk_score: Optional[int] = 0  # 0-100
    tags: List[str] = []
    notes: Optional[str] = None
    cluster_id: Optional[str] = None
    is_watched: bool = False

class AddressCreate(BaseModel):
    address: str
    crypto_type: str
    category: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    tags: List[str] = []
    notes: Optional[str] = None

class AddressUpdate(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    is_watched: Optional[bool] = None

class Entity(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    usernames: List[str] = []
    addresses: List[str] = []  # crypto addresses
    source_urls: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Transaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    crypto_type: str
    timestamp: datetime
    block_number: Optional[int] = None
    fee: Optional[float] = None

class ScraperJob(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    target_url: str
    status: str = "pending"  # pending, running, completed, failed
    addresses_found: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

class DashboardStats(BaseModel):
    total_addresses: int
    addresses_by_crypto: Dict[str, int]
    addresses_by_category: Dict[str, int]
    high_risk_addresses: int
    watched_addresses: int
    recent_activity: int

# ==================== AUTH UTILITIES ====================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, username: str) -> str:
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = decode_token(token)
    
    # For demo mode: if it's the admin user, return it directly without DB check
    if payload['user_id'] == "admin-001":
        return {
            'id': 'admin-001',
            'username': payload.get('username', 'admin'),
            'email': 'admin@ntro.gov.in',
            'role': 'admin',
            'created_at': datetime.now(timezone.utc).isoformat()
        }
    
    # For other users, check the database
    user = await db.users.find_one({'id': payload['user_id']}, {'_id': 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ==================== BLOCKCHAIN API HELPERS ====================

async def fetch_btc_address_info(address: str) -> dict:
    """Fetch Bitcoin address info from blockchain.info API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://blockchain.info/rawaddr/{address}?limit=10"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    balance = data.get('final_balance', 0) / 100000000  # Convert satoshi to BTC
                    tx_count = data.get('n_tx', 0)
                    return {'balance': balance, 'tx_count': tx_count, 'transactions': data.get('txs', [])}
    except Exception as e:
        logging.error(f"Error fetching BTC info: {e}")
    return {'balance': 0, 'tx_count': 0, 'transactions': []}

async def fetch_eth_address_info(address: str) -> dict:
    """Fetch Ethereum address info from Etherscan API (limited without key)"""
    try:
        # Using public API endpoint (limited rate)
        async with aiohttp.ClientSession() as session:
            url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == '1':
                        balance = int(data.get('result', 0)) / 1000000000000000000  # Wei to ETH
                        return {'balance': balance, 'tx_count': 0}
    except Exception as e:
        logging.error(f"Error fetching ETH info: {e}")
    return {'balance': 0, 'tx_count': 0}

# ==================== WEB SCRAPER ====================

CRYPTO_PATTERNS = {
    'BTC': r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|\bbc1[a-z0-9]{39,59}\b',
    'ETH': r'\b0x[a-fA-F0-9]{40}\b',
    'XRP': r'\br[a-zA-Z0-9]{24,34}\b',
    'LTC': r'\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b',
}

async def scrape_addresses_from_url(url: str, job_id: str):
    """Scrape cryptocurrency addresses from a URL"""
    try:
        await db.scraper_jobs.update_one(
            {'id': job_id},
            {'$set': {'status': 'running', 'started_at': datetime.now(timezone.utc).isoformat()}}
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch URL: {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                text_content = soup.get_text()

                addresses_found = 0
                for crypto_type, pattern in CRYPTO_PATTERNS.items():
                    matches = re.findall(pattern, text_content)
                    for address in set(matches):  # Remove duplicates
                        # Check if address already exists
                        existing = await db.addresses.find_one({'address': address}, {'_id': 0})
                        if not existing:
                            addr_obj = CryptoAddress(
                                address=address,
                                crypto_type=crypto_type,
                                source_url=url,
                                source_type='web_scraper',
                                tags=['scraped'],
                                risk_score=random.randint(30, 70)
                            )
                            doc = addr_obj.model_dump()
                            doc['first_seen'] = doc['first_seen'].isoformat()
                            doc['last_updated'] = doc['last_updated'].isoformat()
                            await db.addresses.insert_one(doc)
                            addresses_found += 1

        await db.scraper_jobs.update_one(
            {'id': job_id},
            {'$set': {
                'status': 'completed',
                'completed_at': datetime.now(timezone.utc).isoformat(),
                'addresses_found': addresses_found
            }}
        )

    except Exception as e:
        logging.error(f"Scraper error: {e}")
        await db.scraper_jobs.update_one(
            {'id': job_id},
            {'$set': {
                'status': 'failed',
                'completed_at': datetime.now(timezone.utc).isoformat(),
                'error': str(e)
            }}
        )

# ==================== AUTH ROUTES ====================

@api_router.post("/auth/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate):
    """
    Simplified signup - accepts any username but only validates admin/admin123
    For demo purposes, auto-creates admin user
    """
    # Simple validation: accept admin credentials
    if user_data.username == "admin" and user_data.password == "admin123":
        # Create admin user object
        user = User(
            id="admin-001",
            username="admin",
            email=user_data.email or "admin@ntro.gov.in",
            role="admin",
            created_at=datetime.now(timezone.utc)
        )
        
        token = create_token(user.id, user.username)
        return TokenResponse(token=token, user=user)
    
    # For any other credentials, return error
    raise HTTPException(
        status_code=400, 
        detail="Demo mode: Please use username 'admin' and password 'admin123'"
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Simplified login - only accepts admin/admin123
    No database check, immediate token generation
    """
    # Hardcoded admin credentials
    if credentials.username == "admin" and credentials.password == "admin123":
        # Create admin user object
        user = User(
            id="admin-001",
            username="admin",
            email="admin@ntro.gov.in",
            role="admin",
            created_at=datetime.now(timezone.utc)
        )
        
        token = create_token(user.id, user.username)
        return TokenResponse(token=token, user=user)
    
    # Invalid credentials
    raise HTTPException(
        status_code=401, 
        detail="Invalid credentials. Use username 'admin' and password 'admin123'"
    )

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return current user from token"""
    if isinstance(current_user.get('created_at'), str):
        current_user['created_at'] = datetime.fromisoformat(current_user['created_at'])
    return User(**current_user)

# ==================== ADDRESS ROUTES ====================

@api_router.post("/addresses", response_model=CryptoAddress)
async def create_address(address_data: AddressCreate, current_user: dict = Depends(get_current_user)):
    # Check if address already exists
    existing = await db.addresses.find_one({'address': address_data.address}, {'_id': 0})
    if existing:
        raise HTTPException(status_code=400, detail="Address already exists")
    
    # Create address
    addr = CryptoAddress(**address_data.model_dump())
    
    # Fetch blockchain data
    if address_data.crypto_type == 'BTC':
        info = await fetch_btc_address_info(address_data.address)
        addr.balance = info['balance']
        addr.transaction_count = info['tx_count']
    elif address_data.crypto_type == 'ETH':
        info = await fetch_eth_address_info(address_data.address)
        addr.balance = info['balance']
    
    # Calculate risk score based on various factors
    addr.risk_score = random.randint(20, 90)  # Simplified for MVP
    
    doc = addr.model_dump()
    doc['first_seen'] = doc['first_seen'].isoformat()
    doc['last_updated'] = doc['last_updated'].isoformat()
    
    await db.addresses.insert_one(doc)
    return addr

@api_router.get("/addresses", response_model=List[CryptoAddress])
async def get_addresses(
    crypto_type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_watched: Optional[bool] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    query = {}
    if crypto_type:
        query['crypto_type'] = crypto_type
    if category:
        query['category'] = category
    if search:
        query['address'] = {'$regex': search, '$options': 'i'}
    if is_watched is not None:
        query['is_watched'] = is_watched
    
    addresses = await db.addresses.find(query, {'_id': 0}).sort('last_updated', -1).limit(limit).to_list(limit)
    
    # Convert ISO strings back to datetime
    for addr in addresses:
        if isinstance(addr.get('first_seen'), str):
            addr['first_seen'] = datetime.fromisoformat(addr['first_seen'])
        if isinstance(addr.get('last_updated'), str):
            addr['last_updated'] = datetime.fromisoformat(addr['last_updated'])
    
    return addresses

@api_router.get("/addresses/{address_id}", response_model=CryptoAddress)
async def get_address(address_id: str, current_user: dict = Depends(get_current_user)):
    addr = await db.addresses.find_one({'id': address_id}, {'_id': 0})
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Convert ISO strings
    if isinstance(addr.get('first_seen'), str):
        addr['first_seen'] = datetime.fromisoformat(addr['first_seen'])
    if isinstance(addr.get('last_updated'), str):
        addr['last_updated'] = datetime.fromisoformat(addr['last_updated'])
    
    return CryptoAddress(**addr)

@api_router.patch("/addresses/{address_id}", response_model=CryptoAddress)
async def update_address(
    address_id: str,
    updates: AddressUpdate,
    current_user: dict = Depends(get_current_user)
):
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    update_data['last_updated'] = datetime.now(timezone.utc).isoformat()
    
    result = await db.addresses.update_one(
        {'id': address_id},
        {'$set': update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return await get_address(address_id, current_user)

@api_router.delete("/addresses/{address_id}")
async def delete_address(address_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.addresses.delete_one({'id': address_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    return {'message': 'Address deleted successfully'}

# ==================== SCRAPER ROUTES ====================

@api_router.post("/scraper/start")
async def start_scraper(target_url: str, current_user: dict = Depends(get_current_user)):
    job = ScraperJob(target_url=target_url)
    doc = job.model_dump()
    await db.scraper_jobs.insert_one(doc)
    
    # Start scraping in background
    asyncio.create_task(scrape_addresses_from_url(target_url, job.id))
    
    return {'job_id': job.id, 'message': 'Scraper job started'}

@api_router.get("/scraper/jobs", response_model=List[ScraperJob])
async def get_scraper_jobs(current_user: dict = Depends(get_current_user)):
    jobs = await db.scraper_jobs.find({}, {'_id': 0}).sort('started_at', -1).limit(50).to_list(50)
    
    for job in jobs:
        if isinstance(job.get('started_at'), str):
            job['started_at'] = datetime.fromisoformat(job['started_at'])
        if isinstance(job.get('completed_at'), str):
            job['completed_at'] = datetime.fromisoformat(job['completed_at'])
    
    return jobs

# ==================== ANALYTICS ROUTES ====================

@api_router.get("/analytics/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    total = await db.addresses.count_documents({})
    
    # Addresses by crypto type
    crypto_pipeline = [
        {'$group': {'_id': '$crypto_type', 'count': {'$sum': 1}}}
    ]
    crypto_stats = await db.addresses.aggregate(crypto_pipeline).to_list(None)
    addresses_by_crypto = {item['_id']: item['count'] for item in crypto_stats}
    
    # Addresses by category
    category_pipeline = [
        {'$match': {'category': {'$ne': None}}},
        {'$group': {'_id': '$category', 'count': {'$sum': 1}}}
    ]
    category_stats = await db.addresses.aggregate(category_pipeline).to_list(None)
    addresses_by_category = {item['_id']: item['count'] for item in category_stats}
    
    # High risk addresses (risk_score > 70)
    high_risk = await db.addresses.count_documents({'risk_score': {'$gt': 70}})
    
    # Watched addresses
    watched = await db.addresses.count_documents({'is_watched': True})
    
    # Recent activity (last 24 hours)
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    recent = await db.addresses.count_documents({'last_updated': {'$gte': yesterday}})
    
    return DashboardStats(
        total_addresses=total,
        addresses_by_crypto=addresses_by_crypto,
        addresses_by_category=addresses_by_category,
        high_risk_addresses=high_risk,
        watched_addresses=watched,
        recent_activity=recent
    )

@api_router.get("/analytics/graph")
async def get_transaction_graph(
    address: Optional[str] = None,
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get transaction graph data for visualization"""
    nodes = []
    edges = []
    
    if address:
        # Get specific address and its connections
        addr = await db.addresses.find_one({'address': address}, {'_id': 0})
        if addr:
            nodes.append({
                'id': addr['address'],
                'label': addr['address'][:10] + '...',
                'type': addr['crypto_type'],
                'risk_score': addr.get('risk_score', 0),
                'category': addr.get('category', 'unknown')
            })
            
            # Get related transactions (mock data for MVP)
            related = await db.addresses.find(
                {'crypto_type': addr['crypto_type']},
                {'_id': 0}
            ).limit(10).to_list(10)
            
            for rel in related:
                if rel['address'] != address:
                    nodes.append({
                        'id': rel['address'],
                        'label': rel['address'][:10] + '...',
                        'type': rel['crypto_type'],
                        'risk_score': rel.get('risk_score', 0),
                        'category': rel.get('category', 'unknown')
                    })
                    edges.append({
                        'source': addr['address'],
                        'target': rel['address'],
                        'amount': random.uniform(0.1, 10.0)
                    })
    else:
        # Get general graph
        addresses = await db.addresses.find({}, {'_id': 0}).limit(limit).to_list(limit)
        for addr in addresses:
            nodes.append({
                'id': addr['address'],
                'label': addr['address'][:10] + '...',
                'type': addr['crypto_type'],
                'risk_score': addr.get('risk_score', 0),
                'category': addr.get('category', 'unknown')
            })
    
    return {'nodes': nodes, 'edges': edges}

@api_router.get("/analytics/categories")
async def get_categories(current_user: dict = Depends(get_current_user)):
    """Get list of all categories"""
    return {
        'categories': [
            'ransomware',
            'darknet_market',
            'money_laundering',
            'terror_financing',
            'drug_trafficking',
            'fraud',
            'scam',
            'mixer',
            'exchange',
            'gambling',
            'other'
        ]
    }

# ==================== SEED MANAGER ROUTES ====================

from seed_manager import seed_manager

# Try to import Celery tasks (optional - fallback to sync if not available)
try:
    from tasks import scrape_seed
    CELERY_AVAILABLE = True
    logger.info("✅ Celery tasks loaded - Autonomous scraping enabled")
except ImportError as e:
    CELERY_AVAILABLE = False
    logger.warning(f"⚠️ Celery not available - Running in sync mode only: {e}")

class SeedCreate(BaseModel):
    url: str
    category: str
    priority: int = 3
    frequency: str = "daily"
    name: Optional[str] = None
    description: Optional[str] = None
    deep_web: bool = False

@api_router.get("/seeds")
async def get_seeds():
    """Get all seed sources"""
    return {"seeds": seed_manager.get_all_seeds()}

@api_router.post("/seeds")
async def create_seed(seed: SeedCreate):
    """Add a new seed source"""
    new_seed = seed_manager.add_seed(
        url=seed.url,
        category=seed.category,
        priority=seed.priority,
        frequency=seed.frequency,
        name=seed.name,
        description=seed.description,
        deep_web=seed.deep_web
    )
    return {"seed": new_seed}

@api_router.put("/seeds/{seed_id}/toggle")
async def toggle_seed(seed_id: int):
    """Enable/disable a seed"""
    enabled = seed_manager.toggle_seed(seed_id)
    return {"enabled": enabled}

@api_router.delete("/seeds/{seed_id}")
async def delete_seed(seed_id: int):
    """Delete a seed"""
    success = seed_manager.delete_seed(seed_id)
    if not success:
        raise HTTPException(status_code=404, detail="Seed not found")
    return {"success": True}

@api_router.post("/seeds/{seed_id}/scrape")
async def trigger_scrape(seed_id: int):
    """Manually trigger scraping for a seed - REAL IMPLEMENTATION"""
    seed = seed_manager.get_seed_by_id(seed_id)
    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")
    
    job_id = f"manual_{seed_id}_{int(datetime.now(timezone.utc).timestamp())}"
    
    # Try to use Celery if available, otherwise run synchronously
    if CELERY_AVAILABLE:
        try:
            task = scrape_seed.delay(job_id, seed)
            logger.info(f"🚀 Scraping job queued via Celery: {seed['name']}")
            return {
                "job_id": job_id,
                "task_id": task.id,
                "seed": seed,
                "mode": "async",
                "message": "Scraping job queued successfully - will process in background"
            }
        except Exception as e:
            logger.warning(f"⚠️ Celery failed, falling back to sync: {e}")
    
    # Fallback: Run REAL scraping synchronously
    logger.info(f"🌐 Running REAL scraping synchronously for seed: {seed['name']}")
    
    from scraper import RealScraper
    
    # Check if seed requires proxy (Tor/I2P)
    use_proxy = seed.get('deep_web', False) or '.onion' in seed['url'] or '.i2p' in seed['url']
    
    scraper = RealScraper(timeout=30 if use_proxy else 15)  # Longer timeout for Tor/I2P
    result = scraper.scrape_seed(seed, use_proxy=use_proxy)
    
    # Save addresses to MongoDB
    addresses_saved = 0
    if result['success'] and result['addresses_found']:
        for addr_data in result['addresses_found']:
            try:
                # Check if address already exists
                existing = await db.addresses.find_one({"address": addr_data['address']})
                
                if existing:
                    # Update last_seen
                    await db.addresses.update_one(
                        {"address": addr_data['address']},
                        {"$set": {"last_seen": addr_data['last_seen']}}
                    )
                else:
                    # Insert new address
                    await db.addresses.insert_one(addr_data)
                    addresses_saved += 1
                    logger.info(f"💾 Saved address: {addr_data['address'][:10]}... ({addr_data['currency']})")
            
            except Exception as db_error:
                logger.error(f"❌ Failed to save address: {db_error}")
    
    # Update seed stats
    seed_manager.update_seed_stats(
        seed_id=seed_id,
        addresses_found=addresses_saved,
        success=result['success']
    )
    
    return {
        "job_id": job_id,
        "task_id": "sync_" + job_id,
        "seed": seed,
        "mode": "real_scraping",
        "message": f"✅ Real scraping completed! Found {result['count']} addresses ({addresses_saved} new).",
        "addresses_found": addresses_saved,
        "total_extracted": result['count'],
        "success": result['success'],
        "error": result.get('error'),
        "url": seed['url']
    }

@api_router.get("/seeds/stats")
async def get_seed_stats():
    """Get overall seed statistics"""
    seeds = seed_manager.get_all_seeds()
    return {
        "total_seeds": len(seeds),
        "enabled_seeds": len([s for s in seeds if s['enabled']]),
        "total_addresses_found": sum(s['addresses_found'] for s in seeds),
        "average_success_rate": sum(s['success_rate'] for s in seeds) / len(seeds) if seeds else 0,
        "by_category": {
            category: len([s for s in seeds if s['category'] == category])
            for category in set(s['category'] for s in seeds)
        }
    }

# ==================== ROOT ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "NTRO Cryptocurrency Forensics System API", "version": "1.0.0"}

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run server
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting NTRO Cryptocurrency Forensics System...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
