"""
Blockchair API Integration Module
Enhanced blockchain data retrieval for cryptocurrency forensics
"""

import aiohttp
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Blockchair API Configuration
BLOCKCHAIR_API_KEY = "G___dgu3oEftCaBFOjjW5AFHTzGncdVX"
BLOCKCHAIR_BASE_URL = "https://api.blockchair.com"


class BlockchairAPI:
    """Integration with Blockchair API for multi-blockchain data"""
    
    def __init__(self, api_key: str = BLOCKCHAIR_API_KEY):
        self.api_key = api_key
        self.base_url = BLOCKCHAIR_BASE_URL
        
        # Supported blockchains
        self.supported_chains = {
            'bitcoin': 'bitcoin',
            'ethereum': 'ethereum',
            'litecoin': 'litecoin',
            'bitcoin_cash': 'bitcoin-cash',
            'dogecoin': 'dogecoin',
            'dash': 'dash',
            'ripple': 'ripple',
            'cardano': 'cardano',
            'monero': 'monero',
            'zcash': 'zcash'
        }
    
    async def get_address_info(self, address: str, blockchain: str) -> Dict:
        """
        Get comprehensive address information from Blockchair
        
        Args:
            address: Cryptocurrency address
            blockchain: Blockchain name (bitcoin, ethereum, etc.)
            
        Returns:
            Dict with balance, transaction count, received, sent, etc.
        """
        try:
            chain = self.supported_chains.get(blockchain.lower())
            if not chain:
                logger.warning(f"Unsupported blockchain: {blockchain}")
                return {}
            
            url = f"{self.base_url}/{chain}/dashboards/address/{address}"
            params = {'key': self.api_key}
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_address_data(data, blockchain)
                    elif response.status == 402:
                        logger.error("Blockchair API quota exceeded")
                        return {'error': 'API quota exceeded'}
                    else:
                        logger.error(f"Blockchair API error: {response.status}")
                        return {'error': f'API error: {response.status}'}
                        
        except Exception as e:
            logger.error(f"Error fetching Blockchair data: {e}")
            return {'error': str(e)}
    
    def _parse_address_data(self, data: Dict, blockchain: str) -> Dict:
        """Parse Blockchair API response"""
        try:
            if 'data' not in data:
                return {}
            
            address_data = list(data['data'].values())[0]['address']
            
            # Universal format for all blockchains
            parsed = {
                'blockchain': blockchain,
                'balance': 0,
                'balance_usd': 0,
                'received': 0,
                'received_usd': 0,
                'spent': 0,
                'spent_usd': 0,
                'transaction_count': address_data.get('transaction_count', 0),
                'unspent_output_count': address_data.get('unspent_output_count', 0),
                'first_seen': address_data.get('first_seen_receiving'),
                'last_seen': address_data.get('last_seen_receiving'),
                'type': address_data.get('type', 'unknown')
            }
            
            # Parse balance based on blockchain
            if blockchain == 'bitcoin':
                parsed['balance'] = address_data.get('balance', 0) / 100000000  # Satoshi to BTC
                parsed['received'] = address_data.get('received', 0) / 100000000
                parsed['spent'] = address_data.get('spent', 0) / 100000000
                parsed['balance_usd'] = address_data.get('balance_usd', 0)
                parsed['received_usd'] = address_data.get('received_usd', 0)
                parsed['spent_usd'] = address_data.get('spent_usd', 0)
                
            elif blockchain == 'ethereum':
                parsed['balance'] = address_data.get('balance', 0) / 1e18  # Wei to ETH
                parsed['received'] = address_data.get('received', 0) / 1e18
                parsed['spent'] = address_data.get('spent', 0) / 1e18
                parsed['balance_usd'] = address_data.get('balance_usd', 0)
                
            else:
                # Generic parsing for other chains
                parsed['balance'] = address_data.get('balance', 0)
                parsed['received'] = address_data.get('received', 0)
                parsed['spent'] = address_data.get('spent', 0)
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing Blockchair response: {e}")
            return {}
    
    async def get_transactions(self, address: str, blockchain: str, limit: int = 100) -> List[Dict]:
        """
        Get transaction history for an address
        
        Args:
            address: Cryptocurrency address
            blockchain: Blockchain name
            limit: Maximum number of transactions (default 100, max 10000)
            
        Returns:
            List of transaction dictionaries
        """
        try:
            chain = self.supported_chains.get(blockchain.lower())
            if not chain:
                return []
            
            url = f"{self.base_url}/{chain}/dashboards/address/{address}"
            params = {
                'key': self.api_key,
                'limit': min(limit, 10000),
                'transaction_details': 'true'
            }
            
            timeout = aiohttp.ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_transactions(data, blockchain)
                    else:
                        logger.error(f"Failed to fetch transactions: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []
    
    def _parse_transactions(self, data: Dict, blockchain: str) -> List[Dict]:
        """Parse transaction data from API response"""
        try:
            if 'data' not in data:
                return []
            
            address_key = list(data['data'].keys())[0]
            transactions = data['data'][address_key].get('transactions', [])
            
            parsed_txs = []
            for tx in transactions:
                parsed_tx = {
                    'hash': tx.get('hash'),
                    'time': tx.get('time'),
                    'block_id': tx.get('block_id'),
                    'balance_change': tx.get('balance_change', 0),
                    'is_spent': tx.get('is_spent', False)
                }
                
                # Add blockchain-specific fields
                if blockchain == 'bitcoin':
                    parsed_tx['balance_change'] = tx.get('balance_change', 0) / 100000000
                    parsed_tx['fee'] = tx.get('fee', 0) / 100000000
                elif blockchain == 'ethereum':
                    parsed_tx['balance_change'] = tx.get('balance_change', 0) / 1e18
                    parsed_tx['fee'] = tx.get('fee', 0) / 1e18
                    parsed_tx['gas_used'] = tx.get('gas_used', 0)
                
                parsed_txs.append(parsed_tx)
            
            return parsed_txs
            
        except Exception as e:
            logger.error(f"Error parsing transactions: {e}")
            return []
    
    async def search_addresses(self, query: str, blockchain: str = None) -> List[Dict]:
        """
        Full-text search for addresses across blockchains
        
        Args:
            query: Search query (address fragment, transaction hash, etc.)
            blockchain: Optional blockchain to limit search
            
        Returns:
            List of matching addresses
        """
        try:
            # If blockchain specified, search only that chain
            chains = [blockchain] if blockchain else list(self.supported_chains.keys())
            
            results = []
            for chain in chains[:5]:  # Limit to 5 chains to avoid quota issues
                chain_name = self.supported_chains.get(chain)
                if not chain_name:
                    continue
                
                url = f"{self.base_url}/{chain_name}/dashboards/address/{query}"
                params = {'key': self.api_key}
                
                try:
                    timeout = aiohttp.ClientTimeout(total=10)
                    async with aiohttp.ClientSession(timeout=timeout) as session:
                        async with session.get(url, params=params) as response:
                            if response.status == 200:
                                data = await response.json()
                                parsed = self._parse_address_data(data, chain)
                                if parsed:
                                    parsed['address'] = query
                                    results.append(parsed)
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error in address search: {e}")
            return []
    
    async def get_address_stats(self, address: str, blockchain: str) -> Dict:
        """
        Get advanced statistics for an address
        
        Returns:
            Dict with transaction patterns, time analysis, etc.
        """
        try:
            # Get basic info and transactions
            info = await self.get_address_info(address, blockchain)
            txs = await self.get_transactions(address, blockchain, limit=1000)
            
            if not txs:
                return info
            
            # Calculate statistics
            stats = {
                **info,
                'total_transactions': len(txs),
                'average_transaction_value': sum(abs(tx['balance_change']) for tx in txs) / len(txs) if txs else 0,
                'largest_transaction': max((abs(tx['balance_change']) for tx in txs), default=0),
                'first_transaction': min((tx['time'] for tx in txs if tx.get('time')), default=None),
                'last_transaction': max((tx['time'] for tx in txs if tx.get('time')), default=None),
                'active_days': len(set(tx['time'].split('T')[0] for tx in txs if tx.get('time'))),
            }
            
            # Detect patterns
            stats['pattern_analysis'] = self._analyze_patterns(txs)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating stats: {e}")
            return {}
    
    def _analyze_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze transaction patterns for suspicious activity"""
        patterns = {
            'round_number_txs': 0,
            'rapid_txs': 0,
            'large_txs': 0,
            'suspicious_score': 0.0
        }
        
        if not transactions:
            return patterns
        
        # Check for round numbers (possible money laundering)
        for tx in transactions:
            value = abs(tx.get('balance_change', 0))
            if value > 0 and value == int(value):
                patterns['round_number_txs'] += 1
            if value > 10:  # Large transaction threshold
                patterns['large_txs'] += 1
        
        # Calculate round number ratio
        if transactions:
            round_ratio = patterns['round_number_txs'] / len(transactions)
            if round_ratio > 0.7:
                patterns['suspicious_score'] += 0.3
        
        # Check for rapid transactions (within 5 minutes)
        sorted_txs = sorted(transactions, key=lambda x: x.get('time', ''))
        rapid_count = 0
        
        for i in range(1, len(sorted_txs)):
            try:
                t1 = datetime.fromisoformat(sorted_txs[i-1].get('time', '').replace('Z', '+00:00'))
                t2 = datetime.fromisoformat(sorted_txs[i].get('time', '').replace('Z', '+00:00'))
                if (t2 - t1).total_seconds() < 300:  # 5 minutes
                    rapid_count += 1
            except:
                continue
        
        patterns['rapid_txs'] = rapid_count
        if rapid_count > 5:
            patterns['suspicious_score'] += 0.2
        
        # High number of large transactions
        if patterns['large_txs'] > len(transactions) * 0.3:
            patterns['suspicious_score'] += 0.15
        
        patterns['suspicious_score'] = min(patterns['suspicious_score'], 1.0)
        
        return patterns
    
    async def get_erc20_tokens(self, eth_address: str) -> List[Dict]:
        """Get ERC-20 token balances for an Ethereum address"""
        try:
            url = f"{self.base_url}/ethereum/dashboards/address/{eth_address}"
            params = {
                'key': self.api_key,
                'erc_20': 'true'
            }
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'data' in data:
                            address_data = list(data['data'].values())[0]
                            tokens = address_data.get('layer_2', {}).get('erc_20', [])
                            
                            return [{
                                'token_address': token.get('token_address'),
                                'token_name': token.get('token_name'),
                                'token_symbol': token.get('token_symbol'),
                                'token_decimals': token.get('token_decimals'),
                                'balance': token.get('balance', 0),
                                'balance_approximate': token.get('balance_approximate', 0)
                            } for token in tokens]
                    
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching ERC-20 tokens: {e}")
            return []
