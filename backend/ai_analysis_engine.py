#!/usr/bin/env python3
"""
AI Analysis Engine for Cryptocurrency Forensics
Provides comprehensive AI-powered analysis of cryptocurrency addresses and transactions
"""

import asyncio
import aiohttp
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import logging
from dataclasses import dataclass
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Structure for AI analysis results"""
    address: str
    risk_score: int
    confidence: float
    analysis_type: str
    findings: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]
    timestamp: str

class CryptoForensicsAI:
    """AI Analysis Engine for Cryptocurrency Forensics"""
    
    def __init__(self, google_api_key: str = None):
        self.google_api_key = google_api_key or os.getenv('GOOGLE_API_KEY')
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable must be set")
        self.gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
        # Built-in forensic patterns
        self.risk_patterns = {
            'mixer_services': [
                'tornado', 'mixer', 'tumbler', 'blender', 'coinjoin',
                'wasabi', 'samourai', 'whirlpool'
            ],
            'darkweb_markets': [
                'silk road', 'alphabay', 'dream market', 'wall street',
                'hydra', 'monopoly', 'versus'
            ],
            'ransomware': [
                'wannacry', 'ryuk', 'maze', 'revil', 'conti', 'lockbit',
                'darkside', 'babuk', 'avaddon'
            ],
            'exchanges': [
                'binance', 'coinbase', 'kraken', 'huobi', 'okex',
                'bitfinex', 'bitmex', 'ftx'
            ]
        }
        
        # Behavioral analysis patterns
        self.behavioral_patterns = {
            'structuring': 'Multiple transactions just under reporting thresholds',
            'rapid_movement': 'Quick successive transfers between addresses',
            'dormant_activation': 'Long-dormant address suddenly becomes active',
            'round_numbers': 'Transactions in suspiciously round amounts',
            'time_clustering': 'Multiple transactions within short time windows'
        }

    async def analyze_address(self, address: str, address_data: Dict[str, Any]) -> AnalysisResult:
        """Comprehensive AI analysis of a cryptocurrency address"""
        
        logger.info(f"🤖 Starting AI analysis for address: {address[:15]}...")
        
        # Combine multiple analysis methods
        risk_analysis = await self._analyze_risk_factors(address, address_data)
        behavioral_analysis = await self._analyze_behavior_patterns(address, address_data)
        google_ai_analysis = await self._query_google_ai(address, address_data)
        
        # Combine results
        combined_risk = max(risk_analysis['risk_score'], behavioral_analysis['risk_score'])
        if google_ai_analysis and google_ai_analysis.get('risk_score', 0) > 0:
            combined_risk = max(combined_risk, google_ai_analysis['risk_score'])
        
        all_findings = []
        all_findings.extend(risk_analysis['findings'])
        all_findings.extend(behavioral_analysis['findings'])
        if google_ai_analysis:
            all_findings.extend(google_ai_analysis.get('findings', []))
        
        all_recommendations = []
        all_recommendations.extend(risk_analysis['recommendations'])
        all_recommendations.extend(behavioral_analysis['recommendations'])
        if google_ai_analysis:
            all_recommendations.extend(google_ai_analysis.get('recommendations', []))
        
        # Calculate confidence based on multiple sources
        confidence = min(0.95, (len(all_findings) * 0.2) + 0.3)
        
        result = AnalysisResult(
            address=address,
            risk_score=min(100, combined_risk),
            confidence=confidence,
            analysis_type="comprehensive_ai",
            findings=all_findings[:10],  # Limit to top 10
            recommendations=all_recommendations[:8],  # Limit to top 8
            metadata={
                'risk_analysis': risk_analysis,
                'behavioral_analysis': behavioral_analysis,
                'google_ai_analysis': google_ai_analysis,
                'analysis_sources': ['pattern_matching', 'behavioral_analysis', 'google_ai'],
                'crypto_type': address_data.get('crypto_type', 'unknown'),
                'source': address_data.get('source', 'unknown')
            },
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        logger.info(f"✅ AI analysis completed: Risk {result.risk_score}/100, Confidence {result.confidence:.2%}")
        return result

    async def _analyze_risk_factors(self, address: str, address_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk factors based on known patterns"""
        
        risk_score = 0
        findings = []
        recommendations = []
        
        # Check source and labels
        source = address_data.get('source', '').lower()
        labels = [label.lower() for label in address_data.get('labels', [])]
        notes = address_data.get('notes', '').lower()
        
        # High-risk sources
        if any(keyword in source for keyword in ['darkweb', 'ransomware', 'criminal']):
            risk_score += 50
            findings.append(f"🚨 High-risk source detected: {source}")
            recommendations.append("🔍 Immediate investigation required - criminal source")
        
        # Check against known risk patterns
        for category, keywords in self.risk_patterns.items():
            matches = []
            for keyword in keywords:
                if keyword in source or keyword in notes or any(keyword in label for label in labels):
                    matches.append(keyword)
            
            if matches:
                if category == 'ransomware':
                    risk_score += 40
                    findings.append(f"💰 Ransomware indicators: {', '.join(matches)}")
                    recommendations.append("🚫 Block address - known ransomware")
                elif category == 'mixer_services':
                    risk_score += 30
                    findings.append(f"🌀 Mixing service detected: {', '.join(matches)}")
                    recommendations.append("⚠️ Enhanced monitoring - privacy tool")
                elif category == 'darkweb_markets':
                    risk_score += 45
                    findings.append(f"🕸️ Darkweb marketplace: {', '.join(matches)}")
                    recommendations.append("🚨 High priority investigation")
                elif category == 'exchanges':
                    risk_score = max(0, risk_score - 10)  # Legitimate exchanges reduce risk
                    findings.append(f"🏦 Legitimate exchange: {', '.join(matches)}")
                    recommendations.append("✅ Verified exchange - lower risk")
        
        # Transaction amount analysis
        balance = address_data.get('balance', 0)
        total_received = address_data.get('total_received', 0)
        total_sent = address_data.get('total_sent', 0)
        tx_count = address_data.get('transaction_count', 0)
        
        if total_received > 1000000:  # > $1M equivalent
            risk_score += 15
            findings.append(f"💸 High volume address: ${total_received:,.2f} received")
            recommendations.append("📊 Monitor for large transaction patterns")
        
        if tx_count > 1000:
            risk_score += 10
            findings.append(f"🔄 High activity: {tx_count} transactions")
            recommendations.append("📈 Analyze transaction patterns")
        
        # Web layer risk
        web_layer = address_data.get('web_layer', '').lower()
        if 'dark' in web_layer:
            risk_score += 25
            findings.append("🕸️ Dark web source")
            recommendations.append("🔍 Enhanced due diligence required")
        elif 'deep' in web_layer:
            risk_score += 15
            findings.append("🔒 Deep web source")
            recommendations.append("⚠️ Additional verification needed")
        
        return {
            'risk_score': min(100, risk_score),
            'findings': findings,
            'recommendations': recommendations,
            'method': 'pattern_analysis'
        }

    async def _analyze_behavior_patterns(self, address: str, address_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns for suspicious activity"""
        
        risk_score = 0
        findings = []
        recommendations = []
        
        balance = address_data.get('balance', 0)
        total_received = address_data.get('total_received', 0)
        total_sent = address_data.get('total_sent', 0)
        tx_count = address_data.get('transaction_count', 0)
        
        # Behavioral analysis
        if tx_count > 0:
            avg_transaction = total_received / tx_count
            
            # Structuring detection
            if 9000 <= avg_transaction <= 10000:  # Just under common reporting thresholds
                risk_score += 20
                findings.append("📊 Potential structuring detected")
                recommendations.append("🔍 Investigate for AML compliance")
            
            # Round number analysis
            if avg_transaction % 1000 == 0 or avg_transaction % 10000 == 0:
                risk_score += 10
                findings.append("🔢 Round number transactions (possible structuring)")
                recommendations.append("📈 Monitor transaction patterns")
        
        # Balance vs activity analysis
        if balance == 0 and total_received > 0:
            risk_score += 15
            findings.append("💸 Address completely drained")
            recommendations.append("🚨 Investigate rapid fund movement")
        
        if total_sent > total_received * 0.9 and balance < total_received * 0.1:
            risk_score += 10
            findings.append("🔄 High turnover address")
            recommendations.append("📊 Analyze fund flow patterns")
        
        # Address format analysis (Bitcoin specific)
        if address_data.get('crypto_type') == 'BTC':
            if address.startswith('bc1'):
                findings.append("🔧 Uses modern Bech32 format")
            elif address.startswith('3'):
                findings.append("🔐 Multi-signature or script address")
                risk_score += 5  # Slight risk increase for complexity
            elif address.startswith('1'):
                findings.append("📊 Legacy P2PKH address")
        
        return {
            'risk_score': min(100, risk_score),
            'findings': findings,
            'recommendations': recommendations,
            'method': 'behavioral_analysis'
        }

    async def _query_google_ai(self, address: str, address_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Query Google Gemini AI for advanced analysis"""
        
        if not self.google_api_key:
            logger.warning("No Google API key provided, skipping AI analysis")
            return None
        
        try:
            # Prepare context for AI
            context = {
                'address': address[:15] + "...",  # Anonymize for privacy
                'crypto_type': address_data.get('crypto_type', 'unknown'),
                'source': address_data.get('source', 'unknown'),
                'labels': address_data.get('labels', []),
                'risk_score': address_data.get('risk_score', 0),
                'balance': address_data.get('balance', 0),
                'total_received': address_data.get('total_received', 0),
                'transaction_count': address_data.get('transaction_count', 0),
                'web_layer': address_data.get('web_layer', 'unknown')
            }
            
            prompt = f"""
            As a cryptocurrency forensics expert, analyze this wallet address data:
            
            Address: {context['address']} ({context['crypto_type']})
            Source: {context['source']}
            Labels: {', '.join(context['labels'])}
            Current Risk Score: {context['risk_score']}/100
            Balance: ${context['balance']:,.2f}
            Total Received: ${context['total_received']:,.2f}
            Transactions: {context['transaction_count']}
            Web Layer: {context['web_layer']}
            
            Provide a forensic analysis focusing on:
            1. Risk assessment (0-100 scale)
            2. Key findings (max 3)
            3. Recommended actions (max 3)
            
            Format as JSON with keys: risk_score, findings, recommendations
            """
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 500
                }
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            url = f"{self.gemini_endpoint}?key={self.google_api_key}"
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Extract text from Gemini response
                        if 'candidates' in result and result['candidates']:
                            ai_text = result['candidates'][0]['content']['parts'][0]['text']
                            
                            # Try to parse JSON from AI response
                            try:
                                # Extract JSON from the response
                                json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
                                if json_match:
                                    ai_analysis = json.loads(json_match.group())
                                    
                                    logger.info(f"✅ Google AI analysis completed for {address[:15]}...")
                                    return {
                                        'risk_score': ai_analysis.get('risk_score', 0),
                                        'findings': ai_analysis.get('findings', []),
                                        'recommendations': ai_analysis.get('recommendations', []),
                                        'method': 'google_gemini_ai',
                                        'raw_response': ai_text
                                    }
                                else:
                                    logger.warning("Could not extract JSON from AI response")
                                    return None
                            except json.JSONDecodeError:
                                logger.warning("Could not parse JSON from AI response")
                                return None
                    else:
                        logger.warning(f"Google AI API error: {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"Google AI analysis failed: {e}")
            return None

    async def bulk_analyze(self, addresses: List[Dict[str, Any]]) -> List[AnalysisResult]:
        """Analyze multiple addresses in parallel"""
        
        logger.info(f"🚀 Starting bulk AI analysis for {len(addresses)} addresses")
        
        tasks = []
        for addr_data in addresses:
            address = addr_data.get('address', '')
            if address:
                tasks.append(self.analyze_address(address, addr_data))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, AnalysisResult)]
        
        logger.info(f"✅ Bulk analysis completed: {len(valid_results)}/{len(addresses)} successful")
        return valid_results

    def generate_forensic_report(self, analysis_results: List[AnalysisResult]) -> Dict[str, Any]:
        """Generate comprehensive forensic report"""
        
        if not analysis_results:
            return {'error': 'No analysis results provided'}
        
        # Aggregate statistics
        total_addresses = len(analysis_results)
        high_risk = len([r for r in analysis_results if r.risk_score >= 70])
        medium_risk = len([r for r in analysis_results if 40 <= r.risk_score < 70])
        low_risk = len([r for r in analysis_results if r.risk_score < 40])
        
        avg_risk = sum(r.risk_score for r in analysis_results) / total_addresses
        avg_confidence = sum(r.confidence for r in analysis_results) / total_addresses
        
        # Top findings
        all_findings = []
        for result in analysis_results:
            all_findings.extend(result.findings)
        
        finding_counts = {}
        for finding in all_findings:
            finding_counts[finding] = finding_counts.get(finding, 0) + 1
        
        top_findings = sorted(finding_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Risk distribution
        risk_distribution = {
            'high_risk': {'count': high_risk, 'percentage': (high_risk / total_addresses) * 100},
            'medium_risk': {'count': medium_risk, 'percentage': (medium_risk / total_addresses) * 100},
            'low_risk': {'count': low_risk, 'percentage': (low_risk / total_addresses) * 100}
        }
        
        report = {
            'summary': {
                'total_addresses_analyzed': total_addresses,
                'average_risk_score': round(avg_risk, 2),
                'average_confidence': round(avg_confidence * 100, 2),
                'analysis_timestamp': datetime.now(timezone.utc).isoformat()
            },
            'risk_distribution': risk_distribution,
            'top_findings': top_findings,
            'high_risk_addresses': [
                {
                    'address': r.address[:15] + "...",
                    'risk_score': r.risk_score,
                    'key_findings': r.findings[:3]
                }
                for r in analysis_results if r.risk_score >= 70
            ][:10],
            'recommendations': {
                'immediate_action': [
                    f"Investigate {high_risk} high-risk addresses immediately",
                    f"Enhanced monitoring for {medium_risk} medium-risk addresses",
                    f"Routine checks for {low_risk} low-risk addresses"
                ],
                'system_improvements': [
                    "Implement real-time monitoring for high-risk patterns",
                    "Enhance data collection for better analysis",
                    "Regular updates to risk detection algorithms"
                ]
            }
        }
        
        return report

# Initialize the AI engine with API key from environment
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    crypto_ai = CryptoForensicsAI(google_api_key=google_api_key)
    logger.info(f"✅ AI Analysis Engine initialized")
else:
    logger.warning("⚠️ GOOGLE_API_KEY not set - AI analysis will not work")
    crypto_ai = None

async def analyze_single_address(address: str, address_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for single address analysis"""
    result = await crypto_ai.analyze_address(address, address_data)
    return {
        'address': result.address,
        'risk_score': result.risk_score,
        'confidence': result.confidence,
        'findings': result.findings,
        'recommendations': result.recommendations,
        'metadata': result.metadata,
        'timestamp': result.timestamp
    }

if __name__ == "__main__":
    # Test the AI analysis system
    async def test_ai_analysis():
        test_address_data = {
            'address': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
            'crypto_type': 'BTC',
            'source': 'darkweb_marketplace',
            'labels': ['silk road', 'criminal', 'seized'],
            'risk_score': 95,
            'balance': 0.0,
            'total_received': 50000.0,
            'total_sent': 50000.0,
            'transaction_count': 150,
            'web_layer': 'Dark Web',
            'notes': 'Known Silk Road marketplace address'
        }
        
        print("🤖 Testing AI Analysis System")
        print("=" * 50)
        
        result = await crypto_ai.analyze_address(
            test_address_data['address'], 
            test_address_data
        )
        
        print(f"Address: {result.address}")
        print(f"Risk Score: {result.risk_score}/100")
        print(f"Confidence: {result.confidence:.2%}")
        print(f"Findings: {result.findings}")
        print(f"Recommendations: {result.recommendations}")
    
    asyncio.run(test_ai_analysis())