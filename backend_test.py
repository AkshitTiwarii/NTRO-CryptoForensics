#!/usr/bin/env python3
"""
NTRO Cryptocurrency Forensics System - Backend API Tests
Tests all backend endpoints with realistic data
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "https://blockchain-sleuth-1.preview.emergentagent.com/api"
TEST_USER = {
    "username": "forensic_analyst_2025",
    "email": "analyst@ntro.gov.in", 
    "password": "SecureForensics@2025"
}

# Test Bitcoin address (Satoshi's first address)
TEST_BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
TEST_ETH_ADDRESS = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.test_results = {}
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"   Details: {details}")
        
        self.test_results[test_name] = {
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_auth_signup(self):
        """Test user signup"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/signup", json=TEST_USER)
            
            if response.status_code == 201 or response.status_code == 200:
                data = response.json()
                if "token" in data and "user" in data:
                    self.token = data["token"]
                    self.user_id = data["user"]["id"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.log_result("Auth Signup", True, "User created successfully", 
                                  f"User ID: {self.user_id}")
                    return True
                else:
                    self.log_result("Auth Signup", False, "Invalid response format", 
                                  f"Response: {data}")
                    return False
            elif response.status_code == 400:
                # User might already exist, try login instead
                self.log_result("Auth Signup", True, "User already exists (expected)", 
                              f"Status: {response.status_code}")
                return self.test_auth_login()
            else:
                self.log_result("Auth Signup", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Auth Signup", False, f"Request failed: {str(e)}")
            return False
    
    def test_auth_login(self):
        """Test user login"""
        try:
            login_data = {
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data and "user" in data:
                    self.token = data["token"]
                    self.user_id = data["user"]["id"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.log_result("Auth Login", True, "Login successful", 
                                  f"Token received, User: {data['user']['username']}")
                    return True
                else:
                    self.log_result("Auth Login", False, "Invalid response format", 
                                  f"Response: {data}")
                    return False
            else:
                self.log_result("Auth Login", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Auth Login", False, f"Request failed: {str(e)}")
            return False
    
    def test_auth_me(self):
        """Test get current user"""
        try:
            if not self.token:
                self.log_result("Auth Me", False, "No token available")
                return False
                
            response = self.session.get(f"{BASE_URL}/auth/me")
            
            if response.status_code == 200:
                data = response.json()
                if "username" in data and "email" in data:
                    self.log_result("Auth Me", True, "User profile retrieved", 
                                  f"Username: {data['username']}")
                    return True
                else:
                    self.log_result("Auth Me", False, "Invalid user data", 
                                  f"Response: {data}")
                    return False
            else:
                self.log_result("Auth Me", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Auth Me", False, f"Request failed: {str(e)}")
            return False
    
    def test_create_btc_address(self):
        """Test creating a Bitcoin address"""
        try:
            if not self.token:
                self.log_result("Create BTC Address", False, "No authentication token")
                return False
            
            address_data = {
                "address": TEST_BTC_ADDRESS,
                "crypto_type": "BTC",
                "category": "genesis_block",
                "source_url": "https://bitcoin.org/bitcoin.pdf",
                "source_type": "whitepaper",
                "tags": ["satoshi", "genesis", "historical"],
                "notes": "Satoshi Nakamoto's first Bitcoin address from genesis block"
            }
            
            response = self.session.post(f"{BASE_URL}/addresses", json=address_data)
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                if "id" in data and "address" in data:
                    self.address_id = data["id"]
                    balance = data.get("balance", 0)
                    tx_count = data.get("transaction_count", 0)
                    self.log_result("Create BTC Address", True, 
                                  f"Address created with blockchain data", 
                                  f"Balance: {balance} BTC, Transactions: {tx_count}")
                    return True
                else:
                    self.log_result("Create BTC Address", False, "Invalid response format", 
                                  f"Response: {data}")
                    return False
            elif response.status_code == 400:
                # Address might already exist
                self.log_result("Create BTC Address", True, "Address already exists (expected)", 
                              response.text)
                return True
            else:
                self.log_result("Create BTC Address", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Create BTC Address", False, f"Request failed: {str(e)}")
            return False
    
    def test_create_eth_address(self):
        """Test creating an Ethereum address"""
        try:
            if not self.token:
                self.log_result("Create ETH Address", False, "No authentication token")
                return False
            
            address_data = {
                "address": TEST_ETH_ADDRESS,
                "crypto_type": "ETH",
                "category": "exchange",
                "source_url": "https://etherscan.io",
                "source_type": "blockchain_explorer",
                "tags": ["ethereum", "exchange"],
                "notes": "Ethereum Foundation address"
            }
            
            response = self.session.post(f"{BASE_URL}/addresses", json=address_data)
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                if "id" in data and "address" in data:
                    balance = data.get("balance", 0)
                    self.log_result("Create ETH Address", True, 
                                  f"ETH address created with blockchain data", 
                                  f"Balance: {balance} ETH")
                    return True
                else:
                    self.log_result("Create ETH Address", False, "Invalid response format", 
                                  f"Response: {data}")
                    return False
            elif response.status_code == 400:
                # Address might already exist
                self.log_result("Create ETH Address", True, "Address already exists (expected)", 
                              response.text)
                return True
            else:
                self.log_result("Create ETH Address", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Create ETH Address", False, f"Request failed: {str(e)}")
            return False
    
    def test_get_addresses(self):
        """Test retrieving addresses with filters"""
        try:
            if not self.token:
                self.log_result("Get Addresses", False, "No authentication token")
                return False
            
            # Test basic retrieval
            response = self.session.get(f"{BASE_URL}/addresses")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Get Addresses", True, 
                                  f"Retrieved {len(data)} addresses")
                    
                    # Test with filters
                    btc_response = self.session.get(f"{BASE_URL}/addresses?crypto_type=BTC")
                    if btc_response.status_code == 200:
                        btc_data = btc_response.json()
                        self.log_result("Get BTC Addresses", True, 
                                      f"Retrieved {len(btc_data)} BTC addresses")
                    
                    return True
                else:
                    self.log_result("Get Addresses", False, "Invalid response format", 
                                  f"Expected list, got: {type(data)}")
                    return False
            else:
                self.log_result("Get Addresses", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Get Addresses", False, f"Request failed: {str(e)}")
            return False
    
    def test_update_address(self):
        """Test updating an address"""
        try:
            if not self.token:
                self.log_result("Update Address", False, "No authentication token")
                return False
            
            # First get an address to update
            response = self.session.get(f"{BASE_URL}/addresses?limit=1")
            if response.status_code != 200:
                self.log_result("Update Address", False, "Could not get address to update")
                return False
            
            addresses = response.json()
            if not addresses:
                self.log_result("Update Address", False, "No addresses found to update")
                return False
            
            address_id = addresses[0]["id"]
            update_data = {
                "category": "updated_category",
                "tags": ["updated", "test"],
                "is_watched": True,
                "notes": "Updated during testing"
            }
            
            response = self.session.patch(f"{BASE_URL}/addresses/{address_id}", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("is_watched") == True:
                    self.log_result("Update Address", True, "Address updated successfully", 
                                  f"Address ID: {address_id}")
                    return True
                else:
                    self.log_result("Update Address", False, "Update not reflected", 
                                  f"Response: {data}")
                    return False
            else:
                self.log_result("Update Address", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Update Address", False, f"Request failed: {str(e)}")
            return False
    
    def test_web_scraper(self):
        """Test web scraper functionality"""
        try:
            if not self.token:
                self.log_result("Web Scraper", False, "No authentication token")
                return False
            
            # Start scraper job
            test_url = "https://bitcoin.org/bitcoin.pdf"
            response = self.session.post(f"{BASE_URL}/scraper/start", 
                                       params={"target_url": test_url})
            
            if response.status_code == 200:
                data = response.json()
                if "job_id" in data:
                    job_id = data["job_id"]
                    self.log_result("Web Scraper Start", True, "Scraper job started", 
                                  f"Job ID: {job_id}")
                    
                    # Wait a moment for job to process
                    time.sleep(2)
                    
                    # Check job status
                    jobs_response = self.session.get(f"{BASE_URL}/scraper/jobs")
                    if jobs_response.status_code == 200:
                        jobs = jobs_response.json()
                        if isinstance(jobs, list) and len(jobs) > 0:
                            latest_job = jobs[0]
                            status = latest_job.get("status", "unknown")
                            addresses_found = latest_job.get("addresses_found", 0)
                            self.log_result("Web Scraper Status", True, 
                                          f"Job status: {status}, Addresses found: {addresses_found}")
                            return True
                        else:
                            self.log_result("Web Scraper Status", False, "No jobs found")
                            return False
                    else:
                        self.log_result("Web Scraper Status", False, 
                                      f"HTTP {jobs_response.status_code}")
                        return False
                else:
                    self.log_result("Web Scraper Start", False, "No job_id in response", 
                                  f"Response: {data}")
                    return False
            else:
                self.log_result("Web Scraper Start", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Web Scraper", False, f"Request failed: {str(e)}")
            return False
    
    def test_analytics_dashboard(self):
        """Test analytics dashboard endpoint"""
        try:
            if not self.token:
                self.log_result("Analytics Dashboard", False, "No authentication token")
                return False
            
            response = self.session.get(f"{BASE_URL}/analytics/dashboard")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_addresses", "addresses_by_crypto", 
                                 "addresses_by_category", "high_risk_addresses", 
                                 "watched_addresses", "recent_activity"]
                
                if all(field in data for field in required_fields):
                    total = data["total_addresses"]
                    crypto_stats = data["addresses_by_crypto"]
                    self.log_result("Analytics Dashboard", True, 
                                  f"Dashboard stats retrieved", 
                                  f"Total addresses: {total}, Crypto types: {list(crypto_stats.keys())}")
                    return True
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_result("Analytics Dashboard", False, 
                                  f"Missing fields: {missing}", f"Response: {data}")
                    return False
            else:
                self.log_result("Analytics Dashboard", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Analytics Dashboard", False, f"Request failed: {str(e)}")
            return False
    
    def test_analytics_graph(self):
        """Test transaction graph endpoint"""
        try:
            if not self.token:
                self.log_result("Analytics Graph", False, "No authentication token")
                return False
            
            response = self.session.get(f"{BASE_URL}/analytics/graph")
            
            if response.status_code == 200:
                data = response.json()
                if "nodes" in data and "edges" in data:
                    nodes_count = len(data["nodes"])
                    edges_count = len(data["edges"])
                    self.log_result("Analytics Graph", True, 
                                  f"Graph data retrieved", 
                                  f"Nodes: {nodes_count}, Edges: {edges_count}")
                    return True
                else:
                    self.log_result("Analytics Graph", False, "Invalid graph format", 
                                  f"Response: {data}")
                    return False
            else:
                self.log_result("Analytics Graph", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Analytics Graph", False, f"Request failed: {str(e)}")
            return False
    
    def test_analytics_categories(self):
        """Test categories endpoint"""
        try:
            if not self.token:
                self.log_result("Analytics Categories", False, "No authentication token")
                return False
            
            response = self.session.get(f"{BASE_URL}/analytics/categories")
            
            if response.status_code == 200:
                data = response.json()
                if "categories" in data and isinstance(data["categories"], list):
                    categories = data["categories"]
                    self.log_result("Analytics Categories", True, 
                                  f"Categories retrieved", 
                                  f"Available: {', '.join(categories[:5])}...")
                    return True
                else:
                    self.log_result("Analytics Categories", False, "Invalid categories format", 
                                  f"Response: {data}")
                    return False
            else:
                self.log_result("Analytics Categories", False, f"HTTP {response.status_code}", 
                              response.text)
                return False
                
        except Exception as e:
            self.log_result("Analytics Categories", False, f"Request failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 80)
        print("NTRO CRYPTOCURRENCY FORENSICS SYSTEM - BACKEND API TESTS")
        print("=" * 80)
        print(f"Testing backend at: {BASE_URL}")
        print(f"Test started at: {datetime.now().isoformat()}")
        print()
        
        # Authentication tests (HIGH PRIORITY)
        print("🔐 AUTHENTICATION TESTS")
        print("-" * 40)
        auth_success = self.test_auth_signup()
        if not auth_success:
            auth_success = self.test_auth_login()
        
        if auth_success:
            self.test_auth_me()
        
        print()
        
        # Address management tests (HIGH PRIORITY)
        if auth_success:
            print("📍 ADDRESS MANAGEMENT TESTS")
            print("-" * 40)
            self.test_create_btc_address()
            self.test_create_eth_address()
            self.test_get_addresses()
            self.test_update_address()
            print()
            
            # Web scraper tests (HIGH PRIORITY)
            print("🕷️ WEB SCRAPER TESTS")
            print("-" * 40)
            self.test_web_scraper()
            print()
            
            # Analytics tests (MEDIUM PRIORITY)
            print("📊 ANALYTICS TESTS")
            print("-" * 40)
            self.test_analytics_dashboard()
            self.test_analytics_graph()
            self.test_analytics_categories()
            print()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results.values() if result["success"])
        total = len(self.test_results)
        
        print(f"Tests passed: {passed}/{total}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        print()
        
        # Failed tests
        failed_tests = [name for name, result in self.test_results.items() 
                       if not result["success"]]
        
        if failed_tests:
            print("❌ FAILED TESTS:")
            for test_name in failed_tests:
                result = self.test_results[test_name]
                print(f"  - {test_name}: {result['message']}")
        else:
            print("✅ ALL TESTS PASSED!")
        
        print()
        return self.test_results

if __name__ == "__main__":
    tester = BackendTester()
    results = tester.run_all_tests()