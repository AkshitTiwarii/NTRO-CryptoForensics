import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Badge } from './ui/badge';
import { Switch } from './ui/switch';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Alert, AlertDescription } from './ui/alert';
import { Plus, Trash2, Play, Globe, Clock, TrendingUp, Database, Loader2, CheckCircle, Eye, Shield } from 'lucide-react';

const SeedManager = () => {
  const [seeds, setSeeds] = useState([]);
  const [stats, setStats] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [scrapingSeeds, setScrapingSeeds] = useState(new Set()); // Track which seeds are scraping
  const [newSeed, setNewSeed] = useState({
    url: '',
    category: 'forum',
    priority: 3,
    frequency: 'daily',
    name: '',
    description: '',
    deep_web: false
  });
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    loadSeeds();
    loadStats();
    const interval = setInterval(() => {
      loadSeeds();
      loadStats();
    }, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const loadSeeds = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/seeds');
      const data = await response.json();
      setSeeds(data.seeds);
    } catch (error) {
      console.error('Error loading seeds:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/seeds/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleAddSeed = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/seeds', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newSeed)
      });
      
      if (response.ok) {
        setMessage({ type: 'success', text: 'Seed added successfully!' });
        // Auto-hide message after 3 seconds
        setTimeout(() => {
          setMessage({ type: '', text: '' });
        }, 3000);
        setShowAddForm(false);
        setNewSeed({
          url: '',
          category: 'forum',
          priority: 3,
          frequency: 'daily',
          name: '',
          description: '',
          deep_web: false
        });
        loadSeeds();
        loadStats();
      } else {
        setMessage({ type: 'error', text: 'Failed to add seed' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error adding seed' });
    }
  };

  const toggleSeed = async (seedId) => {
    try {
      await fetch(`http://localhost:8000/api/seeds/${seedId}/toggle`, {
        method: 'PUT'
      });
      loadSeeds();
    } catch (error) {
      console.error('Error toggling seed:', error);
    }
  };

  const deleteSeed = async (seedId) => {
    if (!window.confirm('Are you sure you want to delete this seed?')) return;
    
    try {
      await fetch(`http://localhost:8000/api/seeds/${seedId}`, {
        method: 'DELETE'
      });
      setMessage({ type: 'success', text: 'Seed deleted successfully' });
      // Auto-hide message after 3 seconds
      setTimeout(() => {
        setMessage({ type: '', text: '' });
      }, 3000);
      loadSeeds();
      loadStats();
    } catch (error) {
      setMessage({ type: 'error', text: 'Error deleting seed' });
    }
  };

  const triggerScrape = async (seedId, seedName) => {
    setScrapingSeeds(prev => new Set(prev).add(seedId));
    
    try {
      const response = await fetch(`http://localhost:8000/api/seeds/${seedId}/scrape`, {
        method: 'POST'
      });
      const data = await response.json();
      
      // Show success message with details
      setMessage({ 
        type: 'success', 
        text: `✅ Scraping "${seedName}" completed! Found ${data.addresses_found || 0} addresses. → Go to "Addresses" menu to view them.`
      });
      
      // Auto-hide message after 5 seconds
      setTimeout(() => {
        setMessage({ type: '', text: '' });
      }, 5000);
      
      // Reload to show updated stats
      setTimeout(() => {
        loadSeeds();
        loadStats();
      }, 1000);
      
    } catch (error) {
      setMessage({ type: 'error', text: 'Error starting scrape job' });
      // Auto-hide error after 5 seconds
      setTimeout(() => {
        setMessage({ type: '', text: '' });
      }, 5000);
    } finally {
      // Remove from scraping state after 2 seconds
      setTimeout(() => {
        setScrapingSeeds(prev => {
          const newSet = new Set(prev);
          newSet.delete(seedId);
          return newSet;
        });
      }, 2000);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      forum: 'bg-blue-500',
      social: 'bg-purple-500',
      news: 'bg-green-500',
      pastebin: 'bg-orange-500',
      market: 'bg-red-500',
      code: 'bg-gray-500'
    };
    return colors[category] || 'bg-gray-500';
  };

  const getPriorityLabel = (priority) => {
    const labels = {
      1: { text: 'Critical', color: 'bg-red-600' },
      2: { text: 'High', color: 'bg-orange-600' },
      3: { text: 'Medium', color: 'bg-yellow-600' },
      4: { text: 'Low', color: 'bg-blue-600' }
    };
    return labels[priority] || labels[3];
  };

  const getWebTypeInfo = (seed) => {
    // Determine web type based on URL and deep_web flag
    // For NTRO law enforcement use - all web layers supported
    if (seed.deep_web || seed.url.includes('.onion')) {
      return { type: 'Dark Web (Tor)', icon: '🧅', color: 'bg-purple-600', description: 'Requires Tor SOCKS5 proxy - NTRO authorized' };
    } else if (seed.url.includes('i2p') || seed.url.includes('.i2p')) {
      return { type: 'Deep Web (I2P)', icon: '🕸️', color: 'bg-indigo-600', description: 'Requires I2P router - NTRO authorized' };
    } else if (seed.url.startsWith('https://')) {
      return { type: 'Surface Web (HTTPS)', icon: '🌐', color: 'bg-green-600', description: 'Secure encrypted connection' };
    } else if (seed.url.startsWith('http://')) {
      return { type: 'Surface Web (HTTP)', icon: '🌐', color: 'bg-blue-600', description: 'Standard web connection' };
    } else {
      return { type: 'Unknown', icon: '❓', color: 'bg-gray-600', description: 'Unknown protocol' };
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">Autonomous Seed Manager</h2>
          <p className="text-gray-600">Manage sources for continuous autonomous scraping</p>
        </div>
        <Button onClick={() => setShowAddForm(!showAddForm)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Seed Source
        </Button>
      </div>

      {/* Message Alert */}
      {message.text && (
        <Alert className={`relative ${message.type === 'success' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
          <AlertDescription className={`pr-8 ${message.type === 'success' ? 'text-green-800' : 'text-red-800'}`}>
            {message.text}
          </AlertDescription>
          <button 
            onClick={() => setMessage({ type: '', text: '' })}
            className="absolute right-2 top-2 text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </Alert>
      )}

      {/* Statistics Dashboard */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Seeds</p>
                  <p className="text-2xl font-bold">{stats.total_seeds}</p>
                </div>
                <Database className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Active Seeds</p>
                  <p className="text-2xl font-bold">{stats.enabled_seeds}</p>
                </div>
                <Globe className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Addresses Found</p>
                  <p className="text-2xl font-bold">{stats.total_addresses_found.toLocaleString()}</p>
                </div>
                <TrendingUp className="w-8 h-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Success Rate</p>
                  <p className="text-2xl font-bold">{(stats.average_success_rate * 100).toFixed(0)}%</p>
                </div>
                <Clock className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Add Seed Form */}
      {showAddForm && (
        <Card>
          <CardHeader>
            <CardTitle>Add New Seed Source</CardTitle>
            <CardDescription>Configure a new source for autonomous scraping</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddSeed} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="url">URL *</Label>
                  <Input
                    id="url"
                    value={newSeed.url}
                    onChange={(e) => setNewSeed({...newSeed, url: e.target.value})}
                    placeholder="https://example.com"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    value={newSeed.name}
                    onChange={(e) => setNewSeed({...newSeed, name: e.target.value})}
                    placeholder="Friendly name"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Select value={newSeed.category} onValueChange={(value) => setNewSeed({...newSeed, category: value})}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="forum">Forum</SelectItem>
                      <SelectItem value="social">Social Media</SelectItem>
                      <SelectItem value="news">News</SelectItem>
                      <SelectItem value="pastebin">Pastebin</SelectItem>
                      <SelectItem value="market">Marketplace</SelectItem>
                      <SelectItem value="code">Code Repository</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="priority">Priority</Label>
                  <Select value={String(newSeed.priority)} onValueChange={(value) => setNewSeed({...newSeed, priority: parseInt(value)})}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1">Critical</SelectItem>
                      <SelectItem value="2">High</SelectItem>
                      <SelectItem value="3">Medium</SelectItem>
                      <SelectItem value="4">Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="frequency">Frequency</Label>
                  <Select value={newSeed.frequency} onValueChange={(value) => setNewSeed({...newSeed, frequency: value})}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="hourly">Hourly</SelectItem>
                      <SelectItem value="daily">Daily</SelectItem>
                      <SelectItem value="weekly">Weekly</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="description">Description</Label>
                <Input
                  id="description"
                  value={newSeed.description}
                  onChange={(e) => setNewSeed({...newSeed, description: e.target.value})}
                  placeholder="What this source provides"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="deep_web"
                  checked={newSeed.deep_web}
                  onCheckedChange={(checked) => setNewSeed({...newSeed, deep_web: checked})}
                />
                <Label htmlFor="deep_web">Deep Web Source (.onion)</Label>
              </div>

              <div className="flex space-x-2">
                <Button type="submit">Add Seed</Button>
                <Button type="button" variant="outline" onClick={() => setShowAddForm(false)}>Cancel</Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Seeds List */}
      <div className="grid grid-cols-1 gap-4">
        {seeds.map((seed) => {
          const webType = getWebTypeInfo(seed);
          const isScrapingSeed = scrapingSeeds.has(seed.id);
          
          return (
            <Card key={seed.id} className={!seed.enabled ? 'opacity-50' : ''}>
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2 flex-wrap gap-2">
                      <h3 className="text-lg font-semibold">{seed.name}</h3>
                      <Badge className={getCategoryColor(seed.category)}>{seed.category}</Badge>
                      <Badge className={getPriorityLabel(seed.priority).color}>
                        {getPriorityLabel(seed.priority).text}
                      </Badge>
                      <Badge variant="outline">{seed.frequency}</Badge>
                      <Badge className={webType.color} title={webType.description}>
                        {webType.icon} {webType.type}
                      </Badge>
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-2">{seed.url}</p>
                    {seed.description && <p className="text-sm text-gray-500 mb-3">{seed.description}</p>}
                    
                    <div className="grid grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Addresses Found</p>
                        <p className="font-semibold text-green-600">{seed.addresses_found.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Success Rate</p>
                        <p className="font-semibold">{(seed.success_rate * 100).toFixed(0)}%</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Total Crawls</p>
                        <p className="font-semibold">{seed.total_crawls}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Last Crawled</p>
                        <p className="font-semibold">
                          {seed.last_crawled ? new Date(seed.last_crawled).toLocaleString() : 'Never'}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 ml-4">
                    <Switch
                      checked={seed.enabled}
                      onCheckedChange={() => toggleSeed(seed.id)}
                    />
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => triggerScrape(seed.id, seed.name)}
                      disabled={!seed.enabled || isScrapingSeed}
                      className={isScrapingSeed ? 'bg-green-100' : ''}
                    >
                      {isScrapingSeed ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Play className="w-4 h-4" />
                      )}
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => deleteSeed(seed.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {seeds.length === 0 && (
        <Card>
          <CardContent className="pt-6 text-center text-gray-500">
            <p>No seed sources configured. Click "Add Seed Source" to get started.</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SeedManager;
