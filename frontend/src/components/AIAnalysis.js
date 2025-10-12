import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Bot, 
  BarChart3, 
  AlertTriangle, 
  Check, 
  Loader2,
  FileText,
  Shield
} from 'lucide-react';

const AIAnalysis = () => {
  const [addresses, setAddresses] = useState([]);
  const [selectedAddresses, setSelectedAddresses] = useState([]);
  const [analysisResults, setAnalysisResults] = useState([]);
  const [forensicReport, setForensicReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/addresses', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAddresses(data);
      }
    } catch (error) {
      console.error('Failed to fetch addresses:', error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeAddress = async (addressId) => {
    setAnalyzing(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/ai/analyze/address/${addressId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const result = await response.json();
        setAnalysisResults(prev => [...prev, result]);
        return result;
      }
    } catch (error) {
      console.error('AI analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const bulkAnalyze = async () => {
    if (selectedAddresses.length === 0) {
      alert('Please select addresses to analyze');
      return;
    }

    setAnalyzing(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/ai/analyze/bulk', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedAddresses)
      });
      
      if (response.ok) {
        const result = await response.json();
        setAnalysisResults(result.analysis_results);
        setForensicReport(result.forensic_report);
      }
    } catch (error) {
      console.error('Bulk analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const generateForensicReport = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/ai/report/forensic', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setForensicReport(data.forensic_report);
      }
    } catch (error) {
      console.error('Failed to generate report:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskScore) => {
    if (riskScore >= 70) return 'text-red-500';
    if (riskScore >= 40) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getRiskLabel = (riskScore) => {
    if (riskScore >= 70) return 'High Risk';
    if (riskScore >= 40) return 'Medium Risk';
    return 'Low Risk';
  };

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Brain className="text-3xl text-blue-400" />
              <div>
                <h1 className="text-3xl font-bold">AI Forensic Analysis</h1>
                <p className="text-gray-400">Advanced cryptocurrency forensics with Google AI</p>
              </div>
            </div>
            
            <div className="flex space-x-3">
              <button
                onClick={bulkAnalyze}
                disabled={analyzing || selectedAddresses.length === 0}
                className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg disabled:opacity-50"
              >
                {analyzing ? <Loader2 className="animate-spin" /> : <Bot />}
                <span>Bulk Analyze ({selectedAddresses.length})</span>
              </button>
              
              <button
                onClick={generateForensicReport}
                disabled={loading}
                className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg disabled:opacity-50"
              >
                {loading ? <Loader2 className="animate-spin" /> : <FileText />}
                <span>Generate Report</span>
              </button>
            </div>
          </div>
        </div>

        {/* Address Selection */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Shield className="mr-2 text-green-400" />
              Select Addresses for Analysis
            </h2>
            
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {addresses.map(address => (
                <div key={address.id} className="flex items-center space-x-3 p-2 bg-gray-700 rounded">
                  <input
                    type="checkbox"
                    checked={selectedAddresses.includes(address.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedAddresses(prev => [...prev, address.id]);
                      } else {
                        setSelectedAddresses(prev => prev.filter(id => id !== address.id));
                      }
                    }}
                    className="w-4 h-4"
                  />
                  <div className="flex-1">
                    <div className="font-mono text-sm">{address.address.substring(0, 20)}...</div>
                    <div className="text-xs text-gray-400">
                      {address.crypto_type} • {address.source}
                    </div>
                  </div>
                  <div className={`text-sm ${getRiskColor(address.risk_score)}`}>
                    {address.risk_score}/100
                  </div>
                  <button
                    onClick={() => analyzeAddress(address.id)}
                    disabled={analyzing}
                    className="p-1 bg-blue-600 hover:bg-blue-700 rounded"
                  >
                    <Brain className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <BarChart3 className="mr-2 text-blue-400" />
              Analysis Statistics
            </h2>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span>Total Addresses:</span>
                <span className="font-semibold">{addresses.length}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span>Selected for Analysis:</span>
                <span className="font-semibold text-blue-400">{selectedAddresses.length}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span>Completed Analyses:</span>
                <span className="font-semibold text-green-400">{analysisResults.length}</span>
              </div>
              
              {forensicReport && (
                <div className="pt-2 border-t border-gray-600">
                  <div className="text-sm text-gray-400 mb-2">Latest Report:</div>
                  <div className="text-xs">
                    Avg Risk: {forensicReport.summary?.average_risk_score || 0}/100
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Analysis Results */}
        {analysisResults.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Bot className="mr-2 text-purple-400" />
              AI Analysis Results
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
              {analysisResults.map((result, index) => (
                <div key={index} className="bg-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="font-mono text-sm">
                      {result.address.substring(0, 15)}...
                    </div>
                    <div className={`px-2 py-1 rounded text-xs ${getRiskColor(result.risk_score)} bg-gray-600`}>
                      {getRiskLabel(result.risk_score)}
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Risk Score:</span>
                      <span className={getRiskColor(result.risk_score)}>
                        {result.risk_score}/100
                      </span>
                    </div>
                    
                    <div className="flex justify-between text-sm">
                      <span>Confidence:</span>
                      <span>{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                    
                    <div className="mt-3">
                      <div className="text-xs text-gray-400 mb-1">Key Findings:</div>
                      <div className="space-y-1">
                        {result.findings.slice(0, 2).map((finding, i) => (
                          <div key={i} className="text-xs bg-gray-600 p-1 rounded">
                            {finding}
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="mt-3">
                      <div className="text-xs text-gray-400 mb-1">Recommendations:</div>
                      <div className="space-y-1">
                        {result.recommendations.slice(0, 2).map((rec, i) => (
                          <div key={i} className="text-xs bg-blue-900 p-1 rounded">
                            {rec}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Forensic Report */}
        {forensicReport && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <FileText className="mr-2 text-purple-400" />
              Forensic Investigation Report
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-400">
                  {forensicReport.summary?.total_addresses_analyzed || 0}
                </div>
                <div className="text-sm text-gray-400">Addresses Analyzed</div>
              </div>
              
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-yellow-400">
                  {forensicReport.summary?.average_risk_score || 0}/100
                </div>
                <div className="text-sm text-gray-400">Average Risk Score</div>
              </div>
              
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-green-400">
                  {forensicReport.summary?.average_confidence || 0}%
                </div>
                <div className="text-sm text-gray-400">Average Confidence</div>
              </div>
              
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-red-400">
                  {forensicReport.risk_distribution?.high_risk?.count || 0}
                </div>
                <div className="text-sm text-gray-400">High Risk Addresses</div>
              </div>
            </div>

            {/* Risk Distribution */}
            {forensicReport.risk_distribution && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3">Risk Distribution</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-red-900 bg-opacity-50 rounded-lg p-3">
                    <div className="flex items-center justify-between">
                      <AlertTriangle className="text-red-400" />
                      <span className="text-sm">High Risk</span>
                    </div>
                    <div className="text-xl font-bold text-red-400">
                      {forensicReport.risk_distribution.high_risk.count}
                    </div>
                    <div className="text-xs text-gray-400">
                      {forensicReport.risk_distribution.high_risk.percentage.toFixed(1)}%
                    </div>
                  </div>
                  
                  <div className="bg-yellow-900 bg-opacity-50 rounded-lg p-3">
                    <div className="flex items-center justify-between">
                      <FaExclamationTriangle className="text-yellow-400" />
                      <span className="text-sm">Medium Risk</span>
                    </div>
                    <div className="text-xl font-bold text-yellow-400">
                      {forensicReport.risk_distribution.medium_risk.count}
                    </div>
                    <div className="text-xs text-gray-400">
                      {forensicReport.risk_distribution.medium_risk.percentage.toFixed(1)}%
                    </div>
                  </div>
                  
                  <div className="bg-green-900 bg-opacity-50 rounded-lg p-3">
                    <div className="flex items-center justify-between">
                      <FaCheck className="text-green-400" />
                      <span className="text-sm">Low Risk</span>
                    </div>
                    <div className="text-xl font-bold text-green-400">
                      {forensicReport.risk_distribution.low_risk.count}
                    </div>
                    <div className="text-xs text-gray-400">
                      {forensicReport.risk_distribution.low_risk.percentage.toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Top Findings */}
            {forensicReport.top_findings && (
              <div>
                <h3 className="text-lg font-semibold mb-3">Most Common Security Findings</h3>
                <div className="space-y-2">
                  {forensicReport.top_findings.slice(0, 5).map(([finding, count], index) => (
                    <div key={index} className="flex justify-between items-center bg-gray-700 p-3 rounded">
                      <span className="text-sm">{finding}</span>
                      <span className="bg-blue-600 px-2 py-1 rounded text-xs">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AIAnalysis;