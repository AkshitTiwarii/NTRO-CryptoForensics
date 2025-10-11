import React, { useEffect, useMemo, useState } from "react";
import "./App.css";
import axios from "axios";
import SeedManager from "./components/SeedManager";
import LandingPage from "./components/LandingPage";
import { useTheme } from "./contexts/ThemeContext";
import {
  AlertTriangle,
  BarChart3,
  Clock,
  Database,
  Download,
  Eye,
  Filter,
  Globe,
  LayoutDashboard,
  LogOut,
  MapPin,
  Menu,
  Moon,
  Network,
  Plus,
  Search,
  Shield,
  Sun,
  TrendingUp,
  X
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard, description: "Overview & statistics" },
  { id: "addresses", label: "Addresses", icon: Database, description: "View & manage crypto addresses" },
  { id: "scraping", label: "Scraping", icon: Globe, description: "Manual & automated web scraping" },
  { id: "analytics", label: "Analytics", icon: BarChart3, description: "Charts & trend analysis" },
  { id: "graph", label: "Network Graph", icon: Network, description: "Visual connections" },
  { id: "alerts", label: "Watchlist", icon: AlertTriangle, description: "Monitor addresses" },
  { id: "export", label: "Export", icon: Download, description: "Download reports" }
];

const AUTH_VIEWS = new Set(["login", "signup", "landing"]);

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [view, setView] = useState(token ? "dashboard" : "landing");
  // Mobile responsive: start collapsed on mobile, open on desktop
  const [sidebarOpen, setSidebarOpen] = useState(window.innerWidth >= 1024);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  // Tabs for merged views
  const [addressesTab, setAddressesTab] = useState("search"); // "search" or "add"
  const [scrapingTab, setScrapingTab] = useState("auto"); // "manual" or "auto"

  const [loginForm, setLoginForm] = useState({ username: "", password: "" });
  const [signupForm, setSignupForm] = useState({ username: "", email: "", password: "" });

  const [stats, setStats] = useState(null);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [filters, setFilters] = useState({ crypto_type: "", category: "", search: "" });
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [scraperJobs, setScraperJobs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const [addAddressForm, setAddAddressForm] = useState({
    address: "",
    crypto_type: "BTC",
    category: "",
    source_url: "",
    notes: "",
    tags: []
  });
  const [scraperUrl, setScraperUrl] = useState("");
  const [exportFormat, setExportFormat] = useState("csv");
  
  // New state for Blockchair analysis
  const [analysisForm, setAnalysisForm] = useState({ address: "", crypto_type: "bitcoin" });
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const axiosConfig = useMemo(
    () => ({ headers: { Authorization: token ? `Bearer ${token}` : undefined } }),
    [token]
  );

  useEffect(() => {
    if (!token) {
      setUser(null);
      setView("login");
      return;
    }
    loadUser();
  }, [token]);

  useEffect(() => {
    if (!user) {
      return;
    }
    if (["dashboard", "addresses", "analytics"].includes(view)) {
      loadDashboard();
    }
    if (view === "scraper") {
      loadScraperJobs();
    }
    if (view === "graph") {
      loadGraph();
    }
  }, [user, view]);

  useEffect(() => {
    if (token && user) {
      loadAlerts();
    }
  }, [token, user]);

  const loadUser = async () => {
    try {
      const response = await axios.get(`${API}/auth/me`, axiosConfig);
      setUser(response.data);
      if (AUTH_VIEWS.has(view)) {
        setView("dashboard");
      }
    } catch (error) {
      console.error("Failed to load user:", error);
      logout();
    }
  };

  const loadDashboard = async () => {
    try {
      const [statsRes, addressesRes, categoriesRes] = await Promise.all([
        axios.get(`${API}/analytics/dashboard`, axiosConfig),
        axios.get(`${API}/addresses?limit=100`, axiosConfig),
        axios.get(`${API}/analytics/categories`, axiosConfig)
      ]);
      setStats(statsRes.data);
      setAddresses(addressesRes.data);
      setCategories(categoriesRes.data.categories || []);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    }
  };

  const loadAlerts = () => {
    setAlerts([
      {
        id: "alert-1",
        severity: "critical",
        title: "High-Risk Cluster",
        message: "Cluster C-217 flagged for terror financing patterns.",
        timestamp: new Date()
      },
      {
        id: "alert-2",
        severity: "warning",
        title: "Watchlist Activity",
        message: "Watched address 3FZ...9KQ received 2.3 BTC from Hydra marketplace.",
        timestamp: new Date(Date.now() - 3600 * 1000)
      }
    ]);
  };

  const exportData = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.crypto_type) params.append("crypto_type", filters.crypto_type);
      if (filters.category) params.append("category", filters.category);
      if (filters.search) params.append("search", filters.search);
      params.append("limit", "500");

      const response = await axios.get(`${API}/addresses?${params.toString()}`, axiosConfig);
      const data = response.data;

      if (exportFormat === "csv") {
        const headers = ["Address", "Type", "Category", "Risk Score", "Balance", "Transactions", "First Seen", "Source"];
        const rows = data.map((addr) => [
          addr.address,
          addr.crypto_type,
          addr.category || "",
          addr.risk_score,
          addr.balance ?? 0,
          addr.transaction_count ?? 0,
          addr.first_seen ? new Date(addr.first_seen).toISOString() : "",
          addr.source_url || ""
        ]);
        let csv = headers.join(",") + "\n";
        rows.forEach((row) => {
          csv += row.map((field) => `"${String(field ?? "").replace(/"/g, '""')}"`).join(",") + "\n";
        });
        const blob = new Blob([csv], { type: "text/csv" });
        triggerDownload(blob, `ntro_crypto_registry_${Date.now()}.csv`);
      } else {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
        triggerDownload(blob, `ntro_crypto_registry_${Date.now()}.json`);
      }

      alert(`Export generated (${exportFormat.toUpperCase()})`);
    } catch (error) {
      alert("Failed to export data: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const triggerDownload = (blob, filename) => {
    const url = window.URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    window.URL.revokeObjectURL(url);
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/auth/login`, loginForm);
      setToken(response.data.token);
      setUser(response.data.user);
      localStorage.setItem("token", response.data.token);
      setView("dashboard");
    } catch (error) {
      alert("Login failed: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const signup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/auth/signup`, signupForm);
      setToken(response.data.token);
      setUser(response.data.user);
      localStorage.setItem("token", response.data.token);
      setView("dashboard");
    } catch (error) {
      alert("Signup failed: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user");
    setView("landing");
  };

  const addAddress = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        `${API}/addresses`,
        {
          ...addAddressForm,
          tags: addAddressForm.tags.filter(Boolean)
        },
        axiosConfig
      );
      setAddAddressForm({ address: "", crypto_type: "BTC", category: "", source_url: "", notes: "", tags: [] });
      loadDashboard();
      alert("Address added successfully");
    } catch (error) {
      alert("Failed to add address: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const startScraper = async () => {
    if (!scraperUrl) {
      alert("Please enter a URL to scrape");
      return;
    }
    try {
      await axios.post(`${API}/scraper/start?target_url=${encodeURIComponent(scraperUrl)}`, {}, axiosConfig);
      setScraperUrl("");
      alert("Scraper started. Monitor progress in Recent Jobs.");
      loadScraperJobs();
    } catch (error) {
      alert("Failed to start scraper: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const loadScraperJobs = async () => {
    try {
      const response = await axios.get(`${API}/scraper/jobs`, axiosConfig);
      setScraperJobs(response.data);
    } catch (error) {
      console.error("Failed to load scraper jobs:", error);
    }
  };

  const loadGraph = async (address = null) => {
    try {
      const url = address ? `${API}/analytics/graph?address=${address}` : `${API}/analytics/graph?limit=40`;
      const response = await axios.get(url, axiosConfig);
      setGraphData(response.data);
    } catch (error) {
      console.error("Failed to load graph:", error);
    }
  };

  const applyFilters = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.crypto_type) params.append("crypto_type", filters.crypto_type);
      if (filters.category) params.append("category", filters.category);
      if (filters.search) params.append("search", filters.search);
      params.append("limit", "100");

      const response = await axios.get(`${API}/addresses?${params.toString()}`, axiosConfig);
      setAddresses(response.data);
    } catch (error) {
      console.error("Failed to apply filters:", error);
    }
  };

  const analyzeAddress = async (e) => {
    if (e) e.preventDefault();
    if (!analysisForm.address) {
      alert("Please enter an address to analyze");
      return;
    }
    setAnalysisLoading(true);
    try {
      const response = await axios.post(
        `${API}/addresses/analyze`,
        {
          address: analysisForm.address,
          crypto_type: analysisForm.crypto_type
        },
        axiosConfig
      );
      setAnalysisResult(response.data);
    } catch (error) {
      alert("Analysis failed: " + (error.response?.data?.detail || "Unknown error"));
      setAnalysisResult(null);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const resetFilters = async () => {
    setFilters({ crypto_type: "", category: "", search: "" });
    await loadDashboard();
  };

  const toggleWatch = async (addressId, currentStatus) => {
    try {
      await axios.patch(`${API}/addresses/${addressId}`, { is_watched: !currentStatus }, axiosConfig);
      loadDashboard();
    } catch (error) {
      console.error("Failed to toggle watch:", error);
    }
  };

  const handleNavigation = (viewId) => {
    setView(viewId);
  };

  if (!token || AUTH_VIEWS.has(view)) {
    // Show landing page if no token and view is 'landing'
    if (view === 'landing') {
      return <LandingPage onLogin={() => {
        // After successful login from landing page
        const savedToken = localStorage.getItem('auth_token');
        if (savedToken) {
          setToken(savedToken);
          setView('dashboard');
        }
      }} />;
    }
    
    // Show auth shell for login/signup
    return (
      <AuthShell
        view={view}
        setView={setView}
        loginForm={loginForm}
        setLoginForm={setLoginForm}
        signupForm={signupForm}
        setSignupForm={setSignupForm}
        onLogin={login}
        onSignup={signup}
      />
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex transition-theme">
      {/* Desktop Sidebar */}
      <div className="hidden lg:block">
        <Sidebar
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          view={view}
          handleNavigation={handleNavigation}
          user={user}
          onLogout={logout}
          isMobile={false}
        />
      </div>

      {/* Mobile Sidebar Overlay */}
      {mobileMenuOpen && (
        <>
          <div 
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          />
          <div className="fixed inset-y-0 left-0 w-72 z-50 lg:hidden">
            <Sidebar
              sidebarOpen={true}
              setSidebarOpen={setMobileMenuOpen}
              view={view}
              handleNavigation={(id) => {
                handleNavigation(id);
                setMobileMenuOpen(false);
              }}
              user={user}
              onLogout={logout}
              isMobile={true}
            />
          </div>
        </>
      )}

      <main className="flex-1 overflow-y-auto">
        <Header view={view} onMenuClick={() => setMobileMenuOpen(true)} />
        <div className="p-4 sm:p-6 lg:p-8 space-y-4 sm:space-y-6">
          {view === "dashboard" && <Dashboard stats={stats} />}
          
          {/* Addresses View with Tabs */}
          {view === "addresses" && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-foreground">Cryptocurrency Addresses</h1>
                <div className="flex gap-2 bg-card border border-border rounded-lg p-1">
                  <button
                    onClick={() => setAddressesTab("search")}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      addressesTab === "search"
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    Search Registry
                  </button>
                  <button
                    onClick={() => setAddressesTab("add")}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      addressesTab === "add"
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    Add New
                  </button>
                </div>
              </div>
              
              {addressesTab === "search" && (
                <AddressRegistry
                  addresses={addresses}
                  categories={categories}
                  filters={filters}
                  setFilters={setFilters}
                  applyFilters={applyFilters}
                  resetFilters={resetFilters}
                  setView={setView}
                  setSelectedAddress={setSelectedAddress}
                  toggleWatch={toggleWatch}
                />
              )}
              
              {addressesTab === "add" && (
                <AddAddress
                  categories={categories}
                  addAddressForm={addAddressForm}
                  setAddAddressForm={setAddAddressForm}
                  onSubmit={addAddress}
                />
              )}
            </div>
          )}
          
          {/* Scraping View with Tabs */}
          {view === "scraping" && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-foreground">Web Scraping</h1>
                <div className="flex gap-2 bg-card border border-border rounded-lg p-1">
                  <button
                    onClick={() => setScrapingTab("auto")}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      scrapingTab === "auto"
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    Seed Manager
                  </button>
                  <button
                    onClick={() => setScrapingTab("manual")}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      scrapingTab === "manual"
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    Manual Scraper
                  </button>
                </div>
              </div>
              
              {scrapingTab === "auto" && <SeedManager />}
              
              {scrapingTab === "manual" && (
                <ScraperCenter jobs={scraperJobs} scraperUrl={scraperUrl} setScraperUrl={setScraperUrl} onStart={startScraper} />
              )}
            </div>
          )}
          
          {view === "graph" && <NetworkGraph graphData={graphData} />}
          {view === "analytics" && (
            <div className="space-y-6">
              <BlockchairAnalysis 
                analysisForm={analysisForm}
                setAnalysisForm={setAnalysisForm}
                analysisResult={analysisResult}
                analysisLoading={analysisLoading}
                onAnalyze={analyzeAddress}
              />
              <AnalyticsBoard stats={stats} />
            </div>
          )}
          {view === "alerts" && <AlertsPanel alerts={alerts} />}
          {view === "export" && (
            <ExportPanel exportFormat={exportFormat} setExportFormat={setExportFormat} onExport={exportData} />
          )}
        </div>
      </main>

      {selectedAddress && <AddressModal address={selectedAddress} onClose={() => setSelectedAddress(null)} />}
    </div>
  );
}

function AuthShell({ view, setView, loginForm, setLoginForm, signupForm, setSignupForm, onLogin, onSignup }) {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 transition-theme">
      {/* Theme Toggle in Top Right */}
      <button
        onClick={toggleTheme}
        className="fixed top-4 right-4 p-3 rounded-lg bg-card border border-border hover:bg-accent transition-colors shadow-lg"
        aria-label="Toggle theme"
      >
        {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      </button>
      
      <div className="bg-card border border-border rounded-xl w-full max-w-md shadow-2xl">
        <div className="p-8">
          <div className="mb-8 text-center">
            <div className="mb-4">
              <Shield className="h-12 w-12 mx-auto text-primary" />
            </div>
            <h1 className="text-2xl font-bold text-foreground mb-2">NTRO CryptoForensics</h1>
            <p className="text-muted-foreground text-sm">National Technical Research Organisation</p>
            <p className="text-muted-foreground text-xs">Blockchain Intelligence Suite</p>
            
            {/* Back to Landing Page Link */}
            <button
              onClick={() => setView("landing")}
              className="mt-4 text-xs text-primary hover:underline"
            >
              ← Back to Home
            </button>
          </div>
          
          <div className="flex border-b border-border mb-6">
            <button
              onClick={() => setView("login")}
              className={`flex-1 pb-3 text-sm font-medium transition ${
                view === "login" 
                  ? "text-foreground border-b-2 border-primary" 
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setView("signup")}
              className={`flex-1 pb-3 text-sm font-medium transition ${
                view === "signup" 
                  ? "text-foreground border-b-2 border-primary" 
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Register
            </button>
          </div>
          
          {view === "login" ? (
            <form onSubmit={onLogin} className="space-y-4">
              <div className="bg-accent/50 border border-border rounded-lg p-3 mb-4">
                <p className="text-xs text-foreground font-medium">Demo Credentials:</p>
                <p className="text-xs text-muted-foreground">Username: <code className="text-foreground">admin</code></p>
                <p className="text-xs text-muted-foreground">Password: <code className="text-foreground">admin123</code></p>
              </div>
              <InputField
                label="Username"
                value={loginForm.username}
                onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                placeholder="admin"
                required
              />
              <InputField
                label="Password"
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                placeholder="admin123"
                required
              />
              <button 
                type="submit" 
                className="w-full py-2.5 bg-primary text-primary-foreground rounded-md font-medium transition hover:opacity-90 text-sm"
              >
                Sign In
              </button>
            </form>
          ) : (
            <form onSubmit={onSignup} className="space-y-4">
              <div className="bg-accent/50 border border-border rounded-lg p-3 mb-4">
                <p className="text-xs text-foreground font-medium">Demo Mode:</p>
                <p className="text-xs text-muted-foreground">Use admin/admin123 to login</p>
              </div>
              <InputField
                label="Username"
                value={signupForm.username}
                onChange={(e) => setSignupForm({ ...signupForm, username: e.target.value })}
                placeholder="admin"
                required
              />
              <InputField
                label="Email"
                type="email"
                value={signupForm.email}
                onChange={(e) => setSignupForm({ ...signupForm, email: e.target.value })}
                placeholder="admin@ntro.gov.in"
                required
              />
              <InputField
                label="Password"
                type="password"
                value={signupForm.password}
                onChange={(e) => setSignupForm({ ...signupForm, password: e.target.value })}
                placeholder="admin123"
                required
              />
              <button 
                type="submit" 
                className="w-full py-2.5 bg-primary text-primary-foreground rounded-md font-medium transition hover:opacity-90 text-sm"
              >
                Register
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

function InputField({ label, value, onChange, type = "text", placeholder = "", required = false }) {
  return (
    <div>
      <label className="block text-xs font-medium text-foreground mb-2">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full px-3 py-2 bg-background text-foreground rounded-md border border-input focus:outline-none focus:ring-2 focus:ring-ring text-sm transition-colors"
        required={required}
      />
    </div>
  );
}

function Sidebar({ sidebarOpen, setSidebarOpen, view, handleNavigation, user, onLogout, isMobile }) {
  return (
    <aside className={`${sidebarOpen ? "w-72" : "w-20"} ${isMobile ? 'h-full' : ''} transition-all duration-300 bg-card border-r border-border flex flex-col h-screen`}>
      <div className="flex items-center justify-between px-5 py-4 border-b border-border">
        <div className={`${sidebarOpen ? "block" : "hidden"} transition-all`}>
          <h1 className="text-base sm:text-lg font-semibold text-foreground">NTRO CryptoForensics</h1>
          <p className="text-xs text-muted-foreground">Blockchain Intelligence Suite</p>
        </div>
        <button 
          onClick={() => setSidebarOpen(!sidebarOpen)} 
          className="p-2 rounded-md bg-secondary hover:bg-accent transition-colors"
          aria-label={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
        >
          {sidebarOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </button>
      </div>
      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-3">
          {NAV_ITEMS.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => handleNavigation(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition text-sm ${
                  view === item.id 
                    ? "bg-primary text-primary-foreground" 
                    : "text-muted-foreground hover:text-foreground hover:bg-accent"
                }`}
                aria-label={item.label}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                {sidebarOpen && (
                  <div className="text-left min-w-0">
                    <div className="font-medium truncate">{item.label}</div>
                    <div className="text-xs opacity-70 truncate">{item.description}</div>
                  </div>
                )}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <div className="px-4 py-3 border-t border-border">
        {user && sidebarOpen && (
          <div className="mb-3 text-sm">
            <p className="text-muted-foreground text-xs">Logged in as</p>
            <p className="text-foreground font-medium truncate">{user.username}</p>
          </div>
        )}
        <button 
          onClick={onLogout} 
          className="w-full flex items-center justify-center gap-2 px-3 py-2.5 bg-destructive text-destructive-foreground hover:opacity-90 rounded-md text-sm transition-opacity touch-manipulation"
          aria-label="Sign out"
        >
          <LogOut className="h-4 w-4" />
          {sidebarOpen && "Sign Out"}
        </button>
      </div>
    </aside>
  );
}

function Header({ view, onMenuClick }) {
  const { theme, toggleTheme } = useTheme();
  const activeNav = NAV_ITEMS.find((item) => item.id === view);
  
  return (
    <header className="border-b border-border bg-card transition-theme sticky top-0 z-30">
      <div className="px-4 sm:px-6 lg:px-8 py-3 sm:py-5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4">
          <div className="flex items-center justify-between sm:justify-start gap-3">
            {/* Mobile Menu Button */}
            <button
              onClick={onMenuClick}
              className="lg:hidden p-2 rounded-md bg-secondary hover:bg-accent transition-colors"
              aria-label="Open menu"
            >
              <Menu className="h-5 w-5" />
            </button>
            
            <div>
              <h2 className="text-lg sm:text-xl font-semibold text-foreground">{activeNav?.label}</h2>
              <p className="text-xs text-muted-foreground hidden sm:block">{activeNav?.description}</p>
            </div>

            {/* Mobile Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="sm:hidden p-2 rounded-md bg-secondary hover:bg-accent transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>
          </div>
          
          <div className="flex items-center gap-3 sm:gap-4">
            {/* Desktop Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-lg bg-secondary hover:bg-accent transition-colors text-sm font-medium"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? (
                <>
                  <Sun className="h-4 w-4" />
                  <span className="hidden md:inline">Light Mode</span>
                </>
              ) : (
                <>
                  <Moon className="h-4 w-4" />
                  <span className="hidden md:inline">Dark Mode</span>
                </>
              )}
            </button>
            {/* Backend URL - Hidden on mobile */}
            <div className="hidden lg:flex items-center gap-2 text-xs text-muted-foreground">
              <span>Backend:</span>
              <code className="px-2 py-1 bg-secondary border border-border rounded text-xs">{BACKEND_URL}</code>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function Dashboard({ stats }) {
  if (!stats) {
    return <p className="text-sm text-slate-500">Loading dashboard metrics...</p>;
  }

  const distributionTotals = {
    crypto: Object.values(stats.addresses_by_crypto || {}).reduce((sum, val) => sum + val, 0),
    category: Object.values(stats.addresses_by_category || {}).reduce((sum, val) => sum + val, 0)
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <DashboardCard icon={Database} label="Total Addresses" value={stats.total_addresses} helper="Addresses in repository" />
        <DashboardCard icon={Shield} label="High Risk" value={stats.high_risk_addresses} helper="Risk score above 70" />
        <DashboardCard icon={Eye} label="Watchlist" value={stats.watched_addresses} helper="Active monitored wallets" />
        <DashboardCard icon={Clock} label="24h Updates" value={stats.recent_activity} helper="New or updated records" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DistributionCard
          title="Cryptocurrency Distribution"
          icon={TrendingUp}
          helper="Most active chains in investigations"
          data={stats.addresses_by_crypto}
          total={distributionTotals.crypto}
        />
        <DistributionCard
          title="Category Breakdown"
          icon={MapPin}
          helper="Threat vectors linked to wallets"
          data={stats.addresses_by_category}
          total={distributionTotals.category}
        />
      </div>
    </div>
  );
}

function DashboardCard({ icon: Icon, label, value, helper }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
      <div className="flex items-center justify-between mb-3">
        <div className="text-xs uppercase tracking-wide text-slate-500">{label}</div>
        <Icon className="h-4 w-4 text-slate-500" />
      </div>
      <div className="text-3xl font-bold text-slate-100">{value}</div>
      <p className="text-xs text-slate-500 mt-2">{helper}</p>
    </div>
  );
}

function DistributionCard({ title, icon: Icon, helper, data, total }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      <SectionHeader title={title} icon={Icon} helper={helper} />
      <div className="space-y-4 mt-4">
        {data && Object.entries(data).length > 0 ? (
          Object.entries(data).map(([key, value]) => (
            <StatBar key={key} label={key.replace("_", " ").toUpperCase()} value={value} total={total} />
          ))
        ) : (
          <p className="text-sm text-slate-500">No data available.</p>
        )}
      </div>
    </div>
  );
}

function SectionHeader({ title, icon: Icon, helper }) {
  return (
    <div className="flex items-center gap-3">
      <div className="p-2 rounded-md bg-slate-800/60">
        <Icon className="h-4 w-4 text-slate-300" />
      </div>
      <div>
        <h3 className="text-sm font-semibold text-slate-100">{title}</h3>
        <p className="text-xs text-slate-500">{helper}</p>
      </div>
    </div>
  );
}

function StatBar({ label, value, total }) {
  const width = total ? Math.min(100, Math.round((value / total) * 100)) : 0;
  return (
    <div>
      <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span>
        <span>{value}</span>
      </div>
      <div className="h-2 bg-slate-800 rounded-full">
        <div className="h-2 bg-slate-500 rounded-full" style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

function AddressRegistry({ addresses, categories, filters, setFilters, applyFilters, resetFilters, setView, setSelectedAddress, toggleWatch }) {
  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <div className="flex items-center justify-between mb-4">
          <SectionHeader title="Search & Filter" icon={Filter} helper="Filter registry by crypto, category or pattern" />
          <div className="flex gap-2">
            <button onClick={applyFilters} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-xs font-medium transition">
              Apply
            </button>
            <button onClick={resetFilters} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-xs font-medium transition">
              Reset
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              placeholder="Search address / hash"
              className="w-full pl-9 pr-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm font-mono"
            />
          </div>
          <select
            value={filters.crypto_type}
            onChange={(e) => setFilters({ ...filters, crypto_type: e.target.value })}
            className="px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
          >
            <option value="">All Cryptocurrencies</option>
            <option value="BTC">Bitcoin</option>
            <option value="ETH">Ethereum</option>
            <option value="XRP">Ripple</option>
            <option value="LTC">Litecoin</option>
          </select>
          <select
            value={filters.category}
            onChange={(e) => setFilters({ ...filters, category: e.target.value })}
            className="px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.replace("_", " ").toUpperCase()}
              </option>
            ))}
          </select>
          <button onClick={() => setView("add")} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-xs font-medium transition">
            Quick Add
          </button>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-950 border-b border-slate-800 text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-4 py-3 text-left">Address</th>
                <th className="px-4 py-3 text-left">Type</th>
                <th className="px-4 py-3 text-left">Category</th>
                <th className="px-4 py-3 text-left">Risk</th>
                <th className="px-4 py-3 text-left">Balance</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {addresses.map((addr) => (
                <tr key={addr.id} className="hover:bg-slate-800/60 transition">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      {addr.is_watched && <span className="h-2 w-2 rounded-full bg-slate-300" />}
                      <span className="font-mono text-xs text-slate-200 break-all">{addr.address}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-1 bg-slate-800 rounded-md text-xs text-slate-200 font-medium">{addr.crypto_type}</span>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-400">{addr.category ? addr.category.replace("_", " ") : "Unassigned"}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-slate-800 h-1.5 rounded-full">
                        <div
                          className={`h-1.5 rounded-full ${addr.risk_score > 70 ? "bg-red-400" : addr.risk_score > 40 ? "bg-orange-400" : "bg-slate-400"}`}
                          style={{ width: `${addr.risk_score}%` }}
                        />
                      </div>
                      <span className="text-xs text-slate-300 w-8">{addr.risk_score}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-300">
                    {addr.balance !== null ? `${Number(addr.balance).toFixed(4)} ${addr.crypto_type}` : "�"}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <button onClick={() => setSelectedAddress(addr)} className="px-3 py-1 bg-slate-800 hover:bg-slate-700 rounded text-xs">
                        View
                      </button>
                      <button
                        onClick={() => toggleWatch(addr.id, addr.is_watched)}
                        className={`px-3 py-1 rounded text-xs transition ${addr.is_watched ? "bg-slate-700 hover:bg-slate-600" : "bg-slate-800 hover:bg-slate-700"}`}
                      >
                        {addr.is_watched ? "Unwatch" : "Watch"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {addresses.length === 0 && <div className="text-center py-10 text-sm text-slate-500">No addresses found.</div>}
        </div>
      </div>
    </div>
  );
}

function AddAddress({ categories, addAddressForm, setAddAddressForm, onSubmit }) {
  return (
    <div className="max-w-3xl mx-auto bg-slate-900 border border-slate-800 rounded-lg p-6">
      <SectionHeader title="Register Cryptocurrency Address" icon={Plus} helper="Manually ingest newly discovered wallet evidence" />
      <form onSubmit={onSubmit} className="mt-4 space-y-4">
        <InputField
          label="Cryptocurrency Address"
          value={addAddressForm.address}
          onChange={(e) => setAddAddressForm({ ...addAddressForm, address: e.target.value })}
          required
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1 block">Cryptocurrency Type</label>
            <select
              value={addAddressForm.crypto_type}
              onChange={(e) => setAddAddressForm({ ...addAddressForm, crypto_type: e.target.value })}
              className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
              required
            >
              <option value="BTC">Bitcoin (BTC)</option>
              <option value="ETH">Ethereum (ETH)</option>
              <option value="XRP">Ripple (XRP)</option>
              <option value="LTC">Litecoin (LTC)</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1 block">Category</label>
            <select
              value={addAddressForm.category}
              onChange={(e) => setAddAddressForm({ ...addAddressForm, category: e.target.value })}
              className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
            >
              <option value="">Select category...</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat.replace("_", " ").toUpperCase()}
                </option>
              ))}
            </select>
          </div>
        </div>
        <InputField
          label="Source URL"
          type="url"
          value={addAddressForm.source_url}
          onChange={(e) => setAddAddressForm({ ...addAddressForm, source_url: e.target.value })}
        />
        <div>
          <label className="text-xs font-medium text-slate-400 mb-1 block">Notes</label>
          <textarea
            value={addAddressForm.notes}
            onChange={(e) => setAddAddressForm({ ...addAddressForm, notes: e.target.value })}
            className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
            rows="3"
          />
        </div>
        <button type="submit" className="w-full py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-sm font-medium transition">
          Register Address
        </button>
      </form>
    </div>
  );
}

function ScraperCenter({ jobs, scraperUrl, setScraperUrl, onStart }) {
  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <SectionHeader title="Autonomous OSINT Scraper" icon={Globe} helper="Deploy crawlers against surface / deep sources" />
        <div className="mt-4 flex flex-col md:flex-row gap-3">
          <input
            type="url"
            value={scraperUrl}
            onChange={(e) => setScraperUrl(e.target.value)}
            className="flex-1 px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
            placeholder="https://forum.example/onion/post"
          />
          <button onClick={onStart} className="px-6 py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-sm font-medium transition">
            Launch Scraper
          </button>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <SectionHeader title="Recent Jobs" icon={Clock} helper="Monitor scraper executions and harvested artifacts" />
        <div className="mt-4 space-y-3">
          {jobs.map((job) => (
            <div key={job.id} className="bg-slate-950 border border-slate-800 rounded-md p-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
              <div>
                <p className="font-mono text-xs text-slate-200 break-all">{job.target_url}</p>
                <p className="text-xs text-slate-500 mt-1">
                  Status: <span className="font-medium text-slate-300">{job.status.toUpperCase()}</span>
                  {job.started_at && `  Started ${new Date(job.started_at).toLocaleString()}`}
                </p>
                {job.error && <p className="text-xs text-red-300 mt-1">Error: {job.error}</p>}
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-slate-200">{job.addresses_found}</p>
                <p className="text-xs text-slate-500">addresses found</p>
              </div>
            </div>
          ))}
          {jobs.length === 0 && <p className="text-sm text-slate-500">No scraper jobs yet.</p>}
        </div>
      </div>
    </div>
  );
}

function NetworkGraph({ graphData }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      <SectionHeader title="Network Graph" icon={Network} helper="Visualize clusters and transactional flows" />
      <p className="text-sm text-slate-500 mb-6">Addresses are positioned in a grid for quick overview. Integrate with a dedicated graph library for production-grade analysis.</p>
      {graphData.nodes.length > 0 ? (
        <div className="bg-slate-950 border border-slate-800 rounded-md">
          <svg width="100%" height="520" className="bg-slate-950">
            {graphData.edges.map((edge, idx) => {
              const sourceIdx = graphData.nodes.findIndex((n) => n.id === edge.source);
              const targetIdx = graphData.nodes.findIndex((n) => n.id === edge.target);
              if (sourceIdx === -1 || targetIdx === -1) return null;
              const x1 = 120 + (sourceIdx % 8) * 120;
              const y1 = 120 + Math.floor(sourceIdx / 8) * 120;
              const x2 = 120 + (targetIdx % 8) * 120;
              const y2 = 120 + Math.floor(targetIdx / 8) * 120;
              return <line key={idx} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#475569" strokeWidth="1" />;
            })}
            {graphData.nodes.map((node, idx) => {
              const x = 120 + (idx % 8) * 120;
              const y = 120 + Math.floor(idx / 8) * 120;
              const color = node.risk_score > 70 ? "#f87171" : node.risk_score > 40 ? "#fbbf24" : "#94a3b8";
              return (
                <g key={node.id}>
                  <circle cx={x} cy={y} r="24" fill={color} stroke="#0f172a" strokeWidth="3" />
                  <text x={x} y={y + 40} fill="#cbd5f5" fontSize="10" textAnchor="middle">
                    {node.label}
                  </text>
                </g>
              );
            })}
          </svg>
          <div className="p-4 bg-slate-900 border-t border-slate-800 flex gap-6 justify-center text-xs text-slate-400">
            <LegendDot color="#94a3b8" label="Low Risk" />
            <LegendDot color="#fbbf24" label="Medium Risk" />
            <LegendDot color="#f87171" label="High Risk" />
          </div>
        </div>
      ) : (
        <p className="text-sm text-slate-500">No graph data available. Select an address or expand OSINT ingestion.</p>
      )}
    </div>
  );
}

function AnalyticsBoard({ stats }) {
  if (!stats) {
    return <p className="text-sm text-slate-500">Loading analytics...</p>;
  }
  const total = stats.total_addresses || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      <SectionHeader title="Strategic Analytics" icon={BarChart3} helper="Address volumes by context, severity and chain" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <AnalyticsCard label="Total Addresses" value={stats.total_addresses} helper="Aggregate OSINT hits" />
        <AnalyticsCard label="High-Risk %" value={`${Math.round((stats.high_risk_addresses / total) * 100)}%`} helper="Risk score > 70" />
        <AnalyticsCard label="Watchlist %" value={`${Math.round((stats.watched_addresses / total) * 100)}%`} helper="Manual or automated watch" />
      </div>
    </div>
  );
}

function BlockchairAnalysis({ analysisForm, setAnalysisForm, analysisResult, analysisLoading, onAnalyze }) {
  const SUPPORTED_BLOCKCHAINS = [
    { value: "bitcoin", label: "Bitcoin (BTC)" },
    { value: "ethereum", label: "Ethereum (ETH)" },
    { value: "litecoin", label: "Litecoin (LTC)" },
    { value: "dogecoin", label: "Dogecoin (DOGE)" },
    { value: "bitcoin-cash", label: "Bitcoin Cash (BCH)" },
    { value: "ripple", label: "Ripple (XRP)" },
    { value: "cardano", label: "Cardano (ADA)" },
    { value: "monero", label: "Monero (XMR)" },
    { value: "zcash", label: "Zcash (ZEC)" },
    { value: "dash", label: "Dash (DASH)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      <SectionHeader 
        title="Blockchain Address Analysis" 
        icon={Search} 
        helper="Deep dive into any cryptocurrency address using Blockchair API (41 blockchains supported)" 
      />
      
      <form onSubmit={onAnalyze} className="mt-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <label className="text-xs font-medium text-slate-400 mb-2 block">Cryptocurrency Address</label>
            <input
              type="text"
              value={analysisForm.address}
              onChange={(e) => setAnalysisForm({ ...analysisForm, address: e.target.value })}
              placeholder="Enter address (e.g., 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa)"
              className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm font-mono"
              required
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-400 mb-2 block">Blockchain</label>
            <select
              value={analysisForm.crypto_type}
              onChange={(e) => setAnalysisForm({ ...analysisForm, crypto_type: e.target.value })}
              className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
            >
              {SUPPORTED_BLOCKCHAINS.map(chain => (
                <option key={chain.value} value={chain.value}>{chain.label}</option>
              ))}
            </select>
          </div>
        </div>
        
        <button 
          type="submit" 
          disabled={analysisLoading}
          className="w-full md:w-auto px-6 py-2 bg-slate-800 hover:bg-slate-700 disabled:bg-slate-800 disabled:opacity-50 rounded-md text-sm font-medium transition flex items-center justify-center gap-2"
        >
          {analysisLoading ? (
            <>
              <span className="animate-spin h-4 w-4 border-2 border-slate-400 border-t-transparent rounded-full" />
              Analyzing...
            </>
          ) : (
            <>
              <Search className="h-4 w-4" />
              Analyze Address
            </>
          )}
        </button>
      </form>

      {analysisResult && (
        <div className="mt-6 space-y-6">
          {/* Blockchain Data Section */}
          {analysisResult.blockchain_data && (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-5">
              <h4 className="text-sm font-semibold text-slate-100 mb-4 flex items-center gap-2">
                <Database className="h-4 w-4" />
                Blockchain Data
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <AnalysisDataPoint 
                  label="Balance" 
                  value={`${analysisResult.blockchain_data.balance || 0} ${analysisForm.crypto_type.toUpperCase()}`}
                  subValue={analysisResult.blockchain_data.balance_usd ? `$${Number(analysisResult.blockchain_data.balance_usd).toLocaleString()}` : null}
                />
                <AnalysisDataPoint 
                  label="Total Received" 
                  value={`${analysisResult.blockchain_data.received || 0} ${analysisForm.crypto_type.toUpperCase()}`}
                  subValue={analysisResult.blockchain_data.received_usd ? `$${Number(analysisResult.blockchain_data.received_usd).toLocaleString()}` : null}
                />
                <AnalysisDataPoint 
                  label="Total Spent" 
                  value={`${analysisResult.blockchain_data.spent || 0} ${analysisForm.crypto_type.toUpperCase()}`}
                  subValue={analysisResult.blockchain_data.spent_usd ? `$${Number(analysisResult.blockchain_data.spent_usd).toLocaleString()}` : null}
                />
                <AnalysisDataPoint 
                  label="Transactions" 
                  value={analysisResult.blockchain_data.transaction_count || 0}
                />
                <AnalysisDataPoint 
                  label="First Seen" 
                  value={analysisResult.blockchain_data.first_seen ? new Date(analysisResult.blockchain_data.first_seen).toLocaleDateString() : "Unknown"}
                />
                <AnalysisDataPoint 
                  label="Last Seen" 
                  value={analysisResult.blockchain_data.last_seen ? new Date(analysisResult.blockchain_data.last_seen).toLocaleDateString() : "Unknown"}
                />
              </div>
            </div>
          )}

          {/* ML Categorization Section */}
          {analysisResult.category && (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-5">
              <h4 className="text-sm font-semibold text-slate-100 mb-4 flex items-center gap-2">
                <Shield className="h-4 w-4" />
                ML Categorization & Risk Assessment
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Category</p>
                  <p className="text-lg font-semibold text-slate-100 capitalize">
                    {analysisResult.category.replace(/_/g, ' ')}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    Confidence: {Math.round((analysisResult.confidence || 0) * 100)}%
                  </p>
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Risk Score</p>
                  <div className="flex items-center gap-3">
                    <p className="text-2xl font-bold" style={{ 
                      color: analysisResult.risk_score > 70 ? '#f87171' : analysisResult.risk_score > 40 ? '#fbbf24' : '#94a3b8' 
                    }}>
                      {Math.round(analysisResult.risk_score || 0)}
                    </p>
                    <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div 
                        className="h-full rounded-full transition-all" 
                        style={{ 
                          width: `${analysisResult.risk_score || 0}%`,
                          backgroundColor: analysisResult.risk_score > 70 ? '#f87171' : analysisResult.risk_score > 40 ? '#fbbf24' : '#94a3b8'
                        }}
                      />
                    </div>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    {analysisResult.risk_score > 70 ? 'High Risk' : analysisResult.risk_score > 40 ? 'Medium Risk' : 'Low Risk'}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Related Addresses</p>
                  <p className="text-lg font-semibold text-slate-100">
                    {analysisResult.related_addresses?.length || 0}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">Via clustering</p>
                </div>
              </div>
            </div>
          )}

          {/* Statistics Section */}
          {analysisResult.statistics && (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-5">
              <h4 className="text-sm font-semibold text-slate-100 mb-4 flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                Advanced Statistics
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <AnalysisDataPoint 
                  label="Avg Transaction" 
                  value={analysisResult.statistics.average_transaction_value ? 
                    `${Number(analysisResult.statistics.average_transaction_value).toFixed(4)} ${analysisForm.crypto_type.toUpperCase()}` : 
                    'N/A'}
                />
                <AnalysisDataPoint 
                  label="Largest Transaction" 
                  value={analysisResult.statistics.largest_transaction ? 
                    `${Number(analysisResult.statistics.largest_transaction).toFixed(4)} ${analysisForm.crypto_type.toUpperCase()}` : 
                    'N/A'}
                />
                <AnalysisDataPoint 
                  label="Active Days" 
                  value={analysisResult.statistics.active_days || 0}
                />
                <AnalysisDataPoint 
                  label="Suspicious Score" 
                  value={analysisResult.statistics.suspicious_score ? 
                    `${Math.round(analysisResult.statistics.suspicious_score * 100)}%` : 
                    '0%'}
                />
              </div>
            </div>
          )}

          {/* Pattern Analysis Section */}
          {analysisResult.pattern_analysis && (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-5">
              <h4 className="text-sm font-semibold text-slate-100 mb-4 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4" />
                Pattern Analysis
              </h4>
              <div className="space-y-2">
                <PatternIndicator 
                  label="Round Number Transactions" 
                  detected={analysisResult.pattern_analysis.round_number_transactions}
                  description="Transactions with suspiciously round amounts"
                />
                <PatternIndicator 
                  label="Rapid Transactions" 
                  detected={analysisResult.pattern_analysis.rapid_transactions}
                  description="Multiple transactions in short time periods"
                />
                <PatternIndicator 
                  label="Large Transactions" 
                  detected={analysisResult.pattern_analysis.large_transactions}
                  description="Unusually large transaction amounts"
                />
              </div>
            </div>
          )}

          {/* ERC-20 Tokens (for Ethereum) */}
          {analysisResult.erc20_tokens && analysisResult.erc20_tokens.length > 0 && (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-5">
              <h4 className="text-sm font-semibold text-slate-100 mb-4 flex items-center gap-2">
                <Database className="h-4 w-4" />
                ERC-20 Token Holdings
              </h4>
              <div className="space-y-2">
                {analysisResult.erc20_tokens.map((token, idx) => (
                  <div key={idx} className="flex items-center justify-between py-2 px-3 bg-slate-900 rounded">
                    <span className="text-sm text-slate-200">{token.symbol || 'Unknown'}</span>
                    <span className="text-sm text-slate-400 font-mono">{token.balance || 0}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function AnalysisDataPoint({ label, value, subValue }) {
  return (
    <div>
      <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-sm font-semibold text-slate-100">{value}</p>
      {subValue && <p className="text-xs text-slate-400 mt-0.5">{subValue}</p>}
    </div>
  );
}

function PatternIndicator({ label, detected, description }) {
  return (
    <div className="flex items-center justify-between py-2 px-3 bg-slate-900 rounded">
      <div className="flex items-center gap-3">
        <div className={`h-2 w-2 rounded-full ${detected ? 'bg-red-400' : 'bg-green-400'}`} />
        <div>
          <p className="text-sm text-slate-200">{label}</p>
          <p className="text-xs text-slate-500">{description}</p>
        </div>
      </div>
      <span className={`text-xs font-semibold ${detected ? 'text-red-400' : 'text-green-400'}`}>
        {detected ? 'DETECTED' : 'NONE'}
      </span>
    </div>
  );
}

function AnalyticsCard({ label, value, helper }) {
  return (
    <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
      <div className="text-xs text-slate-500 uppercase tracking-wide mb-1">{label}</div>
      <div className="text-2xl font-semibold text-slate-100">{value}</div>
      <div className="text-xs text-slate-500 mt-2">{helper}</div>
    </div>
  );
}

function AlertsPanel({ alerts }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
      <SectionHeader title="Alerts & Watchlists" icon={AlertTriangle} helper="Investigative queues and notifications" />
      {alerts.length > 0 ? (
        alerts.map((alert) => (
          <div key={alert.id} className="bg-slate-950 border border-slate-800 rounded-md p-4">
            <div className="flex items-center justify-between mb-2">
              <span className={`text-xs font-semibold ${alert.severity === "critical" ? "text-red-300" : "text-yellow-300"}`}>
                {alert.severity.toUpperCase()}
              </span>
              <span className="text-xs text-slate-500">{alert.timestamp.toLocaleString()}</span>
            </div>
            <h4 className="text-sm font-semibold text-slate-100">{alert.title}</h4>
            <p className="text-sm text-slate-400 mt-1">{alert.message}</p>
          </div>
        ))
      ) : (
        <p className="text-sm text-slate-500">No alerts yet. Configure watchlists or wait for new OSINT hits.</p>
      )}
    </div>
  );
}

function ExportPanel({ exportFormat, setExportFormat, onExport }) {
  return (
    <div className="max-w-2xl mx-auto bg-slate-900 border border-slate-800 rounded-lg p-6">
      <SectionHeader title="Export Data" icon={Download} helper="Generate CSV / JSON for downstream tooling" />
      <div className="mt-4 space-y-4">
        <div>
          <label className="text-xs font-medium text-slate-400 mb-1 block">Format</label>
          <select
            value={exportFormat}
            onChange={(e) => setExportFormat(e.target.value)}
            className="w-full px-3 py-2 bg-slate-950 text-slate-100 rounded-md border border-slate-800 focus:outline-none focus:border-slate-600 text-sm"
          >
            <option value="csv">CSV</option>
            <option value="json">JSON</option>
          </select>
        </div>
        <button onClick={onExport} className="w-full py-2 bg-slate-800 hover:bg-slate-700 rounded-md text-sm font-medium transition">
          Export Current View
        </button>
        <p className="text-xs text-slate-500">Filters from the Address Registry are respected. Switch there to refine subset prior to export.</p>
      </div>
    </div>
  );
}

function LegendDot({ color, label }) {
  return (
    <span className="flex items-center gap-2">
      <span className="h-3 w-3 rounded-full" style={{ backgroundColor: color }} />
      <span>{label}</span>
    </span>
  );
}

function AddressModal({ address, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-800 rounded-lg max-w-2xl w-full p-6" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-100">Address Details</h2>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl">&times;</button>
        </div>
        <div className="space-y-4 text-sm">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Address</p>
            <p className="font-mono bg-slate-950 p-2 rounded text-slate-200 break-all">{address.address}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <DetailItem label="Type" value={address.crypto_type} />
            <DetailItem label="Category" value={address.category || "Unassigned"} />
            <DetailItem label="Risk Score" value={`${address.risk_score}/100`} />
            <DetailItem label="Balance" value={address.balance !== null ? `${Number(address.balance).toFixed(4)} ${address.crypto_type}` : "�"} />
            <DetailItem label="Transactions" value={address.transaction_count || 0} />
            <DetailItem label="First Seen" value={address.first_seen ? new Date(address.first_seen).toLocaleDateString() : "Unknown"} />
          </div>
          {address.source_url && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Source</p>
              <a href={address.source_url} target="_blank" rel="noopener noreferrer" className="text-slate-300 hover:text-slate-100 text-xs break-all">
                {address.source_url}
              </a>
            </div>
          )}
          {address.notes && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Notes</p>
              <p className="bg-slate-950 p-2 rounded text-slate-200 text-xs">{address.notes}</p>
            </div>
          )}
          {address.tags && address.tags.length > 0 && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">Tags</p>
              <div className="flex gap-2 flex-wrap">
                {address.tags.map((tag, idx) => (
                  <span key={idx} className="px-2 py-1 bg-slate-800 text-slate-300 rounded text-xs">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function DetailItem({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-slate-200">{value}</p>
    </div>
  );
}

export default App;
