// Mock Data Service for Vercel Demo (No Backend Required)

export const DEMO_MODE = process.env.REACT_APP_DEMO_MODE === 'true' || !process.env.REACT_APP_BACKEND_URL;

// Mock Authentication
export const mockLogin = async (username, password) => {
  await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API delay
  
  return {
    token: 'demo_token_' + Date.now(),
    user: {
      id: 1,
      username: username,
      role: 'admin',
      email: 'demo@ntro.gov.in'
    }
  };
};

// Mock Addresses with Real-Looking Data
export const mockAddresses = [
  {
    id: '1',
    address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
    blockchain: 'Bitcoin',
    risk_score: 95,
    total_received: 68.14523145,
    total_sent: 68.14523145,
    balance: 0,
    transaction_count: 2847,
    first_seen: '2009-01-03T18:15:05Z',
    last_seen: '2024-10-12T14:23:11Z',
    labels: ['Genesis Block', 'Satoshi Nakamoto', 'Historical'],
    status: 'monitored',
    web_layer: 'surface',
    forensic_flags: ['high_profile', 'historical_significance'],
    ai_analysis: {
      vulnerability_score: 95,
      risk_level: 'CRITICAL',
      findings: [
        'Genesis block address - Historical significance',
        'Associated with Bitcoin creator',
        'High-profile target for attacks'
      ],
      recommendations: [
        'Monitor for any suspicious activity',
        'Track derivative addresses',
        'Alert on any transactions'
      ]
    }
  },
  {
    id: '2',
    address: '12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX',
    blockchain: 'Bitcoin',
    risk_score: 88,
    total_received: 127453.45,
    total_sent: 127450.12,
    balance: 3.33,
    transaction_count: 15234,
    first_seen: '2011-06-19T10:30:00Z',
    last_seen: '2024-10-11T08:15:42Z',
    labels: ['Mt. Gox Exchange', 'Defunct Exchange', 'Hack Victim'],
    status: 'flagged',
    web_layer: 'deep',
    forensic_flags: ['exchange_hack', 'large_volume', 'suspicious_patterns'],
    ai_analysis: {
      vulnerability_score: 88,
      risk_level: 'HIGH',
      findings: [
        'Associated with defunct Mt. Gox exchange',
        'Large volume of suspicious transactions detected',
        'Potential mixing service usage',
        'Deep web marketplace connections found'
      ],
      recommendations: [
        'Block transactions from this address',
        'Investigate connected wallets',
        'Report to financial authorities',
        'Enhanced monitoring required'
      ]
    }
  },
  {
    id: '3',
    address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    blockchain: 'Ethereum',
    risk_score: 72,
    total_received: 8234.56,
    total_sent: 8100.23,
    balance: 134.33,
    transaction_count: 4521,
    first_seen: '2017-03-15T12:00:00Z',
    last_seen: '2024-10-13T02:45:18Z',
    labels: ['DeFi Protocol', 'Smart Contract', 'High Activity'],
    status: 'monitored',
    web_layer: 'surface',
    forensic_flags: ['defi_interaction', 'smart_contract'],
    ai_analysis: {
      vulnerability_score: 72,
      risk_level: 'MEDIUM',
      findings: [
        'Active DeFi protocol interactions',
        'Smart contract vulnerabilities detected',
        'Moderate risk transaction patterns'
      ],
      recommendations: [
        'Review smart contract code',
        'Monitor for flash loan attacks',
        'Standard KYC verification'
      ]
    }
  },
  {
    id: '4',
    address: '3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy',
    blockchain: 'Bitcoin',
    risk_score: 45,
    total_received: 12.456,
    total_sent: 10.234,
    balance: 2.222,
    transaction_count: 234,
    first_seen: '2020-05-12T09:30:00Z',
    last_seen: '2024-10-12T18:22:33Z',
    labels: ['Individual Wallet', 'Regular Activity'],
    status: 'clean',
    web_layer: 'surface',
    forensic_flags: [],
    ai_analysis: {
      vulnerability_score: 45,
      risk_level: 'LOW',
      findings: [
        'Normal transaction patterns',
        'Regular individual wallet activity',
        'No suspicious connections detected'
      ],
      recommendations: [
        'Standard monitoring sufficient',
        'Low priority for investigation'
      ]
    }
  },
  {
    id: '5',
    address: 'DdzFFzCqrhssjmxkChyAHE9MdHJkEc4zsZe7jgum6RtGzKLkUanN1kPZ1ipVPBLwVq2TWrhmPsAvArcr47Pp1VNKmZTh6jv8ctAFVCkj',
    blockchain: 'Cardano',
    risk_score: 62,
    total_received: 4523.12,
    total_sent: 4200.00,
    balance: 323.12,
    transaction_count: 892,
    first_seen: '2021-09-01T14:20:00Z',
    last_seen: '2024-10-13T01:11:55Z',
    labels: ['Stake Pool', 'Cardano Network'],
    status: 'monitored',
    web_layer: 'surface',
    forensic_flags: ['stake_pool_operator'],
    ai_analysis: {
      vulnerability_score: 62,
      risk_level: 'MEDIUM',
      findings: [
        'Cardano stake pool operations',
        'Large delegation amounts',
        'Network validator activity'
      ],
      recommendations: [
        'Monitor stake pool performance',
        'Verify operator credentials',
        'Regular compliance checks'
      ]
    }
  },
  {
    id: '6',
    address: 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq',
    blockchain: 'Bitcoin',
    risk_score: 91,
    total_received: 234567.89,
    total_sent: 234500.00,
    balance: 67.89,
    transaction_count: 8923,
    first_seen: '2019-11-20T16:45:00Z',
    last_seen: '2024-10-12T23:59:12Z',
    labels: ['Darknet Market', 'Illegal Activity', 'Mixer Service'],
    status: 'blocked',
    web_layer: 'dark',
    forensic_flags: ['darknet_marketplace', 'mixing_service', 'illegal_activity'],
    ai_analysis: {
      vulnerability_score: 91,
      risk_level: 'CRITICAL',
      findings: [
        'Confirmed darknet marketplace address',
        'Extensive mixing service usage detected',
        'Links to illegal cryptocurrency operations',
        'Multiple law enforcement red flags'
      ],
      recommendations: [
        'IMMEDIATE BLOCK - Do not process',
        'Report to cyber crime division',
        'Freeze related accounts',
        'Coordinate with international agencies'
      ]
    }
  }
];

// Mock Seeds (Forensic Sources)
export const mockSeeds = [
  {
    id: 1,
    name: 'FBI Cryptocurrency Investigation Database',
    url: 'https://fbi.gov/crypto-investigations',
    category: 'Law Enforcement',
    web_layer: 'surface',
    status: 'active',
    last_scraped: '2024-10-13T00:00:00Z',
    addresses_found: 1247,
    priority: 'high'
  },
  {
    id: 2,
    name: 'Europol Cybercrime Centre',
    url: 'https://europol.europa.eu/crime-areas-and-statistics/crime-areas/cybercrime',
    category: 'Law Enforcement',
    web_layer: 'surface',
    status: 'active',
    last_scraped: '2024-10-12T22:30:00Z',
    addresses_found: 892,
    priority: 'high'
  },
  {
    id: 3,
    name: 'Chainalysis Reactor - Darknet Markets',
    url: 'https://chainalysis.com/darknet',
    category: 'Blockchain Analytics',
    web_layer: 'deep',
    status: 'active',
    last_scraped: '2024-10-12T20:15:00Z',
    addresses_found: 3421,
    priority: 'critical'
  },
  {
    id: 4,
    name: 'CipherTrace Threat Intelligence',
    url: 'https://ciphertrace.com/threat-intel',
    category: 'Threat Intelligence',
    web_layer: 'surface',
    status: 'active',
    last_scraped: '2024-10-12T18:45:00Z',
    addresses_found: 2156,
    priority: 'high'
  }
];

// Mock Dashboard Stats
export const mockDashboardStats = {
  total_addresses: 8234,
  high_risk_addresses: 1247,
  active_investigations: 34,
  blocked_addresses: 892,
  total_scraped_sources: 47,
  last_update: '2024-10-13T02:30:00Z',
  alerts: [
    {
      id: 1,
      type: 'critical',
      message: 'New darknet marketplace detected with 234 addresses',
      timestamp: '2024-10-13T01:15:00Z'
    },
    {
      id: 2,
      type: 'warning',
      message: 'Unusual transaction pattern detected on 12 addresses',
      timestamp: '2024-10-13T00:45:00Z'
    },
    {
      id: 3,
      type: 'info',
      message: 'Forensic scraping completed successfully - 892 new addresses',
      timestamp: '2024-10-12T23:30:00Z'
    }
  ]
};

// Mock AI Analysis for bulk addresses
export const mockBulkAIAnalysis = async (addressIds) => {
  await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate AI processing
  
  return {
    success: true,
    analyzed_count: addressIds.length,
    results: addressIds.map(id => {
      const address = mockAddresses.find(a => a.id === id);
      return address ? address.ai_analysis : null;
    }).filter(Boolean)
  };
};

// Mock single address details
export const mockAddressDetails = async (addressId) => {
  await new Promise(resolve => setTimeout(resolve, 300));
  
  const address = mockAddresses.find(a => a.id === addressId);
  if (!address) {
    throw new Error('Address not found');
  }
  
  return {
    ...address,
    transaction_history: [
      {
        hash: 'tx_' + Math.random().toString(36).substr(2, 9),
        type: 'received',
        amount: (Math.random() * 10).toFixed(8),
        timestamp: '2024-10-12T14:23:11Z',
        from: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
      },
      {
        hash: 'tx_' + Math.random().toString(36).substr(2, 9),
        type: 'sent',
        amount: (Math.random() * 5).toFixed(8),
        timestamp: '2024-10-11T08:15:42Z',
        to: '3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy'
      }
    ]
  };
};

// Mock scraping trigger
export const mockScrapeSource = async (seedId) => {
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  return {
    success: true,
    message: `Scraped ${Math.floor(Math.random() * 500)} addresses from source`,
    addresses_added: Math.floor(Math.random() * 500),
    timestamp: new Date().toISOString()
  };
};

export default {
  DEMO_MODE,
  mockLogin,
  mockAddresses,
  mockSeeds,
  mockDashboardStats,
  mockBulkAIAnalysis,
  mockAddressDetails,
  mockScrapeSource
};
