import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { useTheme } from '../contexts/ThemeContext';
import { 
  Shield, 
  Search, 
  TrendingUp, 
  Globe, 
  Eye, 
  Lock,
  AlertTriangle,
  CheckCircle,
  ArrowRight,
  Database,
  Network,
  FileSearch,
  Zap,
  ChevronRight,
  Sun,
  Moon
} from 'lucide-react';

const LandingPage = ({ onLogin }) => {
  const [showLogin, setShowLogin] = useState(false);
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-background text-foreground transition-theme">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Navigation */}
        <nav className="relative z-10 flex flex-wrap justify-between items-center p-4 sm:p-6 max-w-7xl mx-auto gap-3">
          <div className="flex items-center space-x-2">
            <Shield className="w-6 h-6 sm:w-8 sm:h-8 text-primary" />
            <span className="text-lg sm:text-2xl font-bold">NTRO CryptoForensics</span>
            <Badge className="hidden sm:inline-flex bg-primary text-primary-foreground ml-2 text-xs">Intelligence Suite</Badge>
          </div>
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 sm:p-3 rounded-lg bg-card border border-border hover:bg-accent transition-colors touch-manipulation"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="h-4 w-4 sm:h-5 sm:w-5" /> : <Moon className="h-4 w-4 sm:h-5 sm:w-5" />}
            </button>
            <Button 
              onClick={() => setShowLogin(!showLogin)}
              className="bg-primary hover:bg-primary/90 text-xs sm:text-sm"
              size="sm"
            >
              <Lock className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">Admin </span>Login
            </Button>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 py-12 sm:py-20 text-center">
          <div className="mb-4 sm:mb-6">
            <Badge className="bg-destructive text-destructive-foreground px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm">
              🚨 NTRO
            </Badge>
          </div>
          
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 sm:mb-6 leading-tight px-2">
            Blockchain Intelligence
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
              For Law Enforcement
            </span>
          </h1>
          
          <p className="text-sm sm:text-base md:text-xl text-muted-foreground mb-6 sm:mb-8 max-w-3xl mx-auto px-4">
            Advanced cryptocurrency forensics platform for tracking illicit transactions across 
            surface web, dark web, and deep web sources.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-3 sm:gap-4 mb-8 sm:mb-12 px-4">
            <Button 
              size="lg" 
              className="bg-primary hover:bg-primary/90 px-6 sm:px-8 w-full sm:w-auto touch-manipulation"
              onClick={() => setShowLogin(true)}
            >
              Access Dashboard
              <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 ml-2" />
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-border hover:bg-accent w-full sm:w-auto touch-manipulation"
              onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
            >
              Learn More
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-6 max-w-4xl mx-auto px-4">
            <Card className="bg-card border-border backdrop-blur">
              <CardContent className="pt-4 sm:pt-6 text-center px-2 sm:px-4">
                <div className="text-2xl sm:text-3xl font-bold text-blue-400">24/7</div>
                <div className="text-xs sm:text-sm text-muted-foreground mt-1">Autonomous</div>
              </CardContent>
            </Card>
            <Card className="bg-card border-border backdrop-blur">
              <CardContent className="pt-4 sm:pt-6 text-center px-2 sm:px-4">
                <div className="text-2xl sm:text-3xl font-bold text-purple-400">3 Layers</div>
                <div className="text-xs sm:text-sm text-muted-foreground mt-1">Surface • Dark</div>
              </CardContent>
            </Card>
            <Card className="bg-card border-border backdrop-blur">
              <CardContent className="pt-4 sm:pt-6 text-center px-2 sm:px-4">
                <div className="text-2xl sm:text-3xl font-bold text-green-400">Real-time</div>
                <div className="text-xs sm:text-sm text-muted-foreground mt-1">Tracking</div>
              </CardContent>
            </Card>
            <Card className="bg-card border-border backdrop-blur">
              <CardContent className="pt-4 sm:pt-6 text-center px-2 sm:px-4">
                <div className="text-3xl font-bold text-pink-400">AI-Powered</div>
                <div className="text-sm text-muted-foreground mt-1">Pattern Detection</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Problem Statement */}
      <div className="bg-background py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <Badge className="bg-destructive text-destructive-foreground mb-4">THE CHALLENGE</Badge>
            <h2 className="text-4xl font-bold mb-4">Critical Issues We Solve</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Cryptocurrency-based criminal activities are growing exponentially, requiring advanced tools
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-8">
            <Card className="bg-destructive/10 border-destructive/50">
              <CardHeader className="p-4 sm:p-6">
                <div className="flex items-start gap-3 sm:gap-4">
                  <AlertTriangle className="w-6 h-6 sm:w-8 sm:h-8 text-destructive flex-shrink-0 mt-1" />
                  <div>
                    <CardTitle className="text-base sm:text-xl mb-1 sm:mb-2">Dark Web Crime</CardTitle>
                    <CardDescription className="text-xs sm:text-sm">
                      Illegal marketplaces on Tor (.onion) facilitate drug trafficking, weapons sales, 
                      and ransomware payments using cryptocurrency. Traditional tools cannot access these sites.
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>

            <Card className="bg-destructive/10 border-destructive/50">
              <CardHeader>
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-8 h-8 text-destructive flex-shrink-0 mt-1" />
                  <div>
                    <CardTitle className="text-xl mb-2">Money Laundering</CardTitle>
                    <CardDescription>
                      Criminals use mixing services and complex transaction chains to obscure fund origins. 
                      Manual tracking is impossible at scale.
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>

            <Card className="bg-destructive/10 border-destructive/50">
              <CardHeader>
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-8 h-8 text-destructive flex-shrink-0 mt-1" />
                  <div>
                    <CardTitle className="text-xl mb-2">Terrorism Financing</CardTitle>
                    <CardDescription>
                      Terror groups receive donations via Bitcoin/Ethereum, making transactions hard to trace 
                      across international borders and anonymous networks.
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>

            <Card className="bg-destructive/10 border-destructive/50">
              <CardHeader>
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-8 h-8 text-destructive flex-shrink-0 mt-1" />
                  <div>
                    <CardTitle className="text-xl mb-2">Data Fragmentation</CardTitle>
                    <CardDescription>
                      Crypto addresses scattered across forums, social media, pastebin dumps, and darknet markets. 
                      No centralized intelligence database exists.
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="bg-card/50 py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <Badge className="bg-green-600 text-white mb-4">OUR SOLUTION</Badge>
            <h2 className="text-4xl font-bold mb-4">Comprehensive Intelligence Platform</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Military-grade blockchain forensics combining automation, deep web access, and AI analysis
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="bg-card border-border hover:border-primary transition-all">
              <CardHeader>
                <Globe className="w-12 h-12 text-blue-400 mb-4" />
                <CardTitle>Multi-Layer Web Scraping</CardTitle>
                <CardDescription>
                  Automatically scrape cryptocurrency addresses from:
                  <ul className="mt-2 space-y-1 list-disc list-inside">
                    <li>🌐 Surface Web (Forums, GitHub, Reddit)</li>
                    <li>🧅 Dark Web (Tor .onion markets)</li>
                    <li>🕸️ Deep Web (I2P networks)</li>
                  </ul>
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-card border-border hover:border-purple-500 transition-all">
              <CardHeader>
                <Database className="w-12 h-12 text-purple-400 mb-4" />
                <CardTitle>Centralized Intelligence</CardTitle>
                <CardDescription>
                  MongoDB-powered database stores:
                  <ul className="mt-2 space-y-1 list-disc list-inside">
                    <li>Bitcoin & Ethereum addresses</li>
                    <li>Transaction metadata</li>
                    <li>Source attribution</li>
                    <li>Temporal tracking</li>
                  </ul>
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-card border-border hover:border-green-500 transition-all">
              <CardHeader>
                <Zap className="w-12 h-12 text-green-400 mb-4" />
                <CardTitle>Autonomous Operation</CardTitle>
                <CardDescription>
                  Celery-powered automation:
                  <ul className="mt-2 space-y-1 list-disc list-inside">
                    <li>⏰ Hourly scraping schedule</li>
                    <li>🔄 Self-synchronizing data</li>
                    <li>🤖 No manual intervention</li>
                    <li>📊 Real-time updates</li>
                  </ul>
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-card border-border hover:border-yellow-500 transition-all">
              <CardHeader>
                <Network className="w-12 h-12 text-yellow-400 mb-4" />
                <CardTitle>Network Graph Analysis</CardTitle>
                <CardDescription>
                  Visualize transaction flows and connections between addresses to identify criminal networks
                  and money laundering patterns.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-card border-border hover:border-pink-500 transition-all">
              <CardHeader>
                <Eye className="w-12 h-12 text-pink-400 mb-4" />
                <CardTitle>Watchlist Monitoring</CardTitle>
                <CardDescription>
                  Real-time alerts when monitored addresses appear in new transactions or are mentioned
                  on dark web forums.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-card border-border hover:border-red-500 transition-all">
              <CardHeader>
                <FileSearch className="w-12 h-12 text-red-400 mb-4" />
                <CardTitle>Advanced Search</CardTitle>
                <CardDescription>
                  Filter by currency, source, date range, and web layer. Export reports for legal proceedings
                  and evidence documentation.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </div>

      {/* Technology Stack */}
      <div className="bg-background py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <Badge className="bg-purple-600 text-white mb-4">TECHNOLOGY</Badge>
            <h2 className="text-4xl font-bold mb-4">Built for Scale & Security</h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="bg-card border-border">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-400 mb-2">Frontend</div>
                  <div className="text-sm text-muted-foreground space-y-1">
                    <div>React 19</div>
                    <div>TailwindCSS</div>
                    <div>shadcn/ui</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-lg font-bold text-green-400 mb-2">Backend</div>
                  <div className="text-sm text-muted-foreground space-y-1">
                    <div>Python FastAPI</div>
                    <div>MongoDB</div>
                    <div>Redis + Celery</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-400 mb-2">Scraping</div>
                  <div className="text-sm text-muted-foreground space-y-1">
                    <div>BeautifulSoup4</div>
                    <div>Tor SOCKS5</div>
                    <div>I2P Proxy</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-lg font-bold text-pink-400 mb-2">Security</div>
                  <div className="text-sm text-muted-foreground space-y-1">
                    <div>JWT Auth</div>
                    <div>bcrypt</div>
                    <div>HTTPS/TLS</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Login Modal */}
      {showLogin && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md bg-card border-border">
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle className="text-2xl flex items-center gap-2">
                    <Shield className="w-6 h-6 text-primary" />
                    Admin Login
                  </CardTitle>
                  <CardDescription>
                    Authorized NTRO personnel only
                  </CardDescription>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowLogin(false)}
                  className="hover:bg-accent"
                >
                  ✕
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <LoginForm onSuccess={onLogin} />
            </CardContent>
          </Card>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-card border-t border-border py-8 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-primary" />
            <span className="text-muted-foreground">NTRO CryptoForensics Intelligence Suite</span>
          </div>
          <p className="text-muted-foreground text-sm">
            ⚠️ Restricted access system for authorized law enforcement use only
          </p>
          <p className="text-muted-foreground/60 text-xs mt-2">
            National Technical Research Organisation • Government of India
          </p>
        </div>
      </footer>
    </div>
  );
};

const LoginForm = ({ onSuccess }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        onSuccess();
      } else {
        setError(data.detail || 'Invalid credentials');
      }
    } catch (err) {
      setError('Connection failed. Please check if backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-900/30 border border-red-700 text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2">
          Username
        </label>
        <input
          type="text"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
          className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
          placeholder="Enter NTRO username"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2">
          Password
        </label>
        <input
          type="password"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
          placeholder="Enter password"
          required
        />
      </div>

      <Button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white"
        disabled={loading}
      >
        {loading ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
            Authenticating...
          </>
        ) : (
          <>
            <Lock className="w-4 h-4 mr-2" />
            Access Dashboard
          </>
        )}
      </Button>

      <div className="text-center text-xs text-gray-600 mt-4">
        Demo credentials: admin / admin123
      </div>
    </form>
  );
};

export default LandingPage;
