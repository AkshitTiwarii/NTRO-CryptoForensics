// API Service - Supports both Demo Mode and Real Backend

import axios from 'axios';
import {
  DEMO_MODE,
  mockLogin,
  mockAddresses,
  mockSeeds,
  mockDashboardStats,
  mockBulkAIAnalysis,
  mockAddressDetails,
  mockScrapeSource
} from './mockData';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API_BASE = `${BACKEND_URL}/api`;

// Helper to create axios config with auth
const getConfig = (token) => ({
  headers: {
    Authorization: token ? `Bearer ${token}` : undefined
  }
});

// Authentication
export const login = async (username, password) => {
  if (DEMO_MODE) {
    return mockLogin(username, password);
  }
  
  const response = await axios.post(`${API_BASE}/auth/login`, {
    username,
    password
  });
  return response.data;
};

export const signup = async (username, email, password) => {
  if (DEMO_MODE) {
    // In demo mode, just redirect to login
    return { message: 'Demo mode - please use demo/demo123 to login' };
  }
  
  const response = await axios.post(`${API_BASE}/auth/signup`, {
    username,
    email,
    password
  });
  return response.data;
};

export const getUser = async (token) => {
  if (DEMO_MODE) {
    return {
      id: 1,
      username: 'demo',
      email: 'demo@ntro.gov.in',
      role: 'admin'
    };
  }
  
  const response = await axios.get(`${API_BASE}/auth/user`, getConfig(token));
  return response.data;
};

// Dashboard Stats
export const getDashboardStats = async (token) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 300));
    return mockDashboardStats;
  }
  
  const response = await axios.get(`${API_BASE}/stats`, getConfig(token));
  return response.data;
};

// Addresses
export const getAddresses = async (token, filters = {}) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 400));
    
    let filtered = [...mockAddresses];
    
    if (filters.search) {
      const search = filters.search.toLowerCase();
      filtered = filtered.filter(addr => 
        addr.address.toLowerCase().includes(search) ||
        addr.blockchain.toLowerCase().includes(search) ||
        addr.labels.some(label => label.toLowerCase().includes(search))
      );
    }
    
    if (filters.risk_level) {
      filtered = filtered.filter(addr => {
        const level = addr.ai_analysis?.risk_level || 'LOW';
        return level === filters.risk_level;
      });
    }
    
    return {
      addresses: filtered,
      total: filtered.length
    };
  }
  
  const params = new URLSearchParams();
  Object.keys(filters).forEach(key => {
    if (filters[key]) params.append(key, filters[key]);
  });
  
  const response = await axios.get(
    `${API_BASE}/addresses?${params.toString()}`,
    getConfig(token)
  );
  return response.data;
};

export const getAddressDetails = async (token, addressId) => {
  if (DEMO_MODE) {
    return mockAddressDetails(addressId);
  }
  
  const response = await axios.get(
    `${API_BASE}/addresses/${addressId}`,
    getConfig(token)
  );
  return response.data;
};

export const addAddress = async (token, addressData) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const newAddress = {
      id: String(mockAddresses.length + 1),
      ...addressData,
      risk_score: Math.floor(Math.random() * 100),
      total_received: 0,
      total_sent: 0,
      balance: 0,
      transaction_count: 0,
      first_seen: new Date().toISOString(),
      last_seen: new Date().toISOString(),
      status: 'new',
      web_layer: 'surface',
      forensic_flags: []
    };
    
    mockAddresses.push(newAddress);
    return { success: true, address: newAddress };
  }
  
  const response = await axios.post(
    `${API_BASE}/addresses`,
    addressData,
    getConfig(token)
  );
  return response.data;
};

// Seeds (Forensic Sources)
export const getSeeds = async (token) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 300));
    return { seeds: mockSeeds };
  }
  
  const response = await axios.get(`${API_BASE}/seeds`, getConfig(token));
  return response.data;
};

export const scrapeSource = async (token, seedId) => {
  if (DEMO_MODE) {
    return mockScrapeSource(seedId);
  }
  
  const response = await axios.post(
    `${API_BASE}/seeds/${seedId}/scrape`,
    {},
    getConfig(token)
  );
  return response.data;
};

// AI Analysis
export const runBulkAIAnalysis = async (token, addressIds) => {
  if (DEMO_MODE) {
    return mockBulkAIAnalysis(addressIds);
  }
  
  const response = await axios.post(
    `${API_BASE}/ai/analyze/bulk`,
    { address_ids: addressIds },
    getConfig(token)
  );
  return response.data;
};

export const analyzeAddress = async (token, addressId) => {
  if (DEMO_MODE) {
    const address = mockAddresses.find(a => a.id === addressId);
    if (!address) {
      throw new Error('Address not found');
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      success: true,
      analysis: address.ai_analysis
    };
  }
  
  const response = await axios.post(
    `${API_BASE}/ai/analyze/address/${addressId}`,
    {},
    getConfig(token)
  );
  return response.data;
};

// Export
export const exportData = async (token, format = 'csv', filters = {}) => {
  if (DEMO_MODE) {
    // Generate demo export
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const addresses = mockAddresses;
    let content = '';
    
    if (format === 'csv') {
      content = 'Address,Blockchain,Risk Score,Balance,Status,Web Layer\n';
      addresses.forEach(addr => {
        content += `${addr.address},${addr.blockchain},${addr.risk_score},${addr.balance},${addr.status},${addr.web_layer}\n`;
      });
    } else if (format === 'json') {
      content = JSON.stringify(addresses, null, 2);
    }
    
    // Create and download file
    const blob = new Blob([content], { type: format === 'csv' ? 'text/csv' : 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ntro-crypto-forensics-${Date.now()}.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    return { success: true, message: 'Export completed' };
  }
  
  const params = new URLSearchParams({ format });
  Object.keys(filters).forEach(key => {
    if (filters[key]) params.append(key, filters[key]);
  });
  
  const response = await axios.get(
    `${API_BASE}/export?${params.toString()}`,
    { ...getConfig(token), responseType: 'blob' }
  );
  
  // Download the file
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `export.${format}`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  
  return { success: true };
};

// Graph Data
export const getGraphData = async (token, addressId = null) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 600));
    
    // Generate demo graph data
    const nodes = mockAddresses.slice(0, 6).map(addr => ({
      id: addr.id,
      label: addr.address.substring(0, 10) + '...',
      risk_score: addr.risk_score,
      blockchain: addr.blockchain
    }));
    
    const edges = [
      { from: '1', to: '2', value: 125.5, label: '125.5 BTC' },
      { from: '2', to: '3', value: 45.2, label: '45.2 ETH' },
      { from: '1', to: '4', value: 12.8, label: '12.8 BTC' },
      { from: '3', to: '5', value: 234.1, label: '234.1 ADA' },
      { from: '4', to: '6', value: 567.3, label: '567.3 BTC' },
      { from: '6', to: '2', value: 89.4, label: '89.4 BTC' }
    ];
    
    return { nodes, edges };
  }
  
  const url = addressId 
    ? `${API_BASE}/graph/${addressId}`
    : `${API_BASE}/graph`;
    
  const response = await axios.get(url, getConfig(token));
  return response.data;
};

export default {
  DEMO_MODE,
  login,
  signup,
  getUser,
  getDashboardStats,
  getAddresses,
  getAddressDetails,
  addAddress,
  getSeeds,
  scrapeSource,
  runBulkAIAnalysis,
  analyzeAddress,
  exportData,
  getGraphData
};
