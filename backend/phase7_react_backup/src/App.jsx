import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  ShieldAlert, Activity, Database, Camera, 
  History, PlaySquare, UploadCloud,
  CheckCircle, AlertTriangle, BarChart3, Loader2, Target, Info
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer
} from 'recharts';

const API_URL = 'http://127.0.0.1:8000/api';

const NavItem = ({ active, icon: Icon, label, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${active ? 'bg-brand-primary text-slate-900 font-semibold shadow-lg shadow-brand-primary/20' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}
  >
    <Icon size={20} className={active ? 'text-slate-900' : ''} />
    <span>{label}</span>
  </button>
);

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  
  return (
    <div className="min-h-screen bg-dark-bg text-slate-100 flex overflow-hidden font-sans selection:bg-brand-primary/30">
      {/* Sidebar */}
      <aside className="w-72 glass-panel border-r border-white/5 flex flex-col relative z-20">
        <div className="p-6 flex items-center space-x-3 border-b border-white/5">
          <div className="bg-brand-primary p-2 rounded-lg">
            <ShieldAlert size={24} className="text-slate-900" />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight tracking-tight text-white">Smart Rockfall</h1>
            <p className="text-xs text-brand-primary font-medium tracking-wider uppercase">Early Alert System</p>
          </div>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
          <NavItem active={currentView === 'dashboard'} icon={Activity} label="Live Dashboard" onClick={() => setCurrentView('dashboard')} />
          <NavItem active={currentView === 'prediction'} icon={Camera} label="Image Prediction" onClick={() => setCurrentView('prediction')} />
          <NavItem active={currentView === 'simulation'} icon={PlaySquare} label="Dataset Simulation" onClick={() => setCurrentView('simulation')} />
          <NavItem active={currentView === 'history'} icon={History} label="Prediction History" onClick={() => setCurrentView('history')} />
          
          <div className="pt-6 pb-2 px-4">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">System</p>
          </div>
          
          <NavItem active={currentView === 'dataset'} icon={Database} label="Dataset Info" onClick={() => setCurrentView('dataset')} />
          <NavItem active={currentView === 'model'} icon={Target} label="Model Performance" onClick={() => setCurrentView('model')} />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 relative overflow-y-auto bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-slate-900 via-dark-bg to-dark-bg">
        <div className="p-8 max-w-7xl mx-auto min-h-full">
          {currentView === 'dashboard' && <DashboardView />}
          {currentView === 'dataset' && <DatasetView />}
          {currentView === 'model' && <ModelView />}
          {currentView === 'prediction' && <PredictionView />}
          {currentView === 'simulation' && <SimulationView />}
          {currentView === 'history' && <HistoryView />}
        </div>
      </main>
    </div>
  );
}

// ================= VIEWS =================

function DashboardView() {
  const [stats, setStats] = useState({ total_preds: 0, objects_detected: 0, latest: null });
  const [sysStatus, setSysStatus] = useState('Checking...');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [historyRes, statusRes] = await Promise.all([
        axios.get(`${API_URL}/history`),
        axios.get(`${API_URL}/status`).catch(() => ({ data: { model_status: 'Unavailable' } }))
      ]);
      
      const history = historyRes.data;
      
      // Calculate total objects detected from all real history records
      let totalObjects = 0;
      history.forEach(h => {
         try {
            const classes = JSON.parse(h.detected_classes || '[]');
            totalObjects += classes.length;
         } catch(e) {}
      });
      
      setStats({
        total_preds: history.length,
        objects_detected: totalObjects,
        latest: history[0] || null
      });
      
      setSysStatus(statusRes.data.model_status);
    } catch (e) {
      console.error(e);
      setSysStatus('Unavailable');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white tracking-tight">Open-Pit Mine Dashboard</h2>
        <p className="text-slate-400 mt-1">AI-powered mine image analysis and safety analytics</p>
      </header>

      {stats.total_preds === 0 ? (
        <div className="flex flex-col items-center justify-center h-64 text-center glass-panel rounded-2xl">
          <Activity size={48} className="text-slate-500 mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">Insufficient data for this analysis.</h3>
          <p className="text-slate-400 max-w-md">Run a prediction or dataset simulation to populate the dashboard.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard title="Total Predictions" value={stats.total_preds} icon={Activity} />
            <StatCard title="Objects Detected" value={stats.objects_detected} icon={Target} color="text-brand-primary" />
            <StatCard title="Database Status" value={sysStatus?.database?.connected ? 'PostgreSQL Connected' : 'Disconnected'} icon={Database} color={sysStatus?.database?.connected ? 'text-emerald-400' : 'text-red-400'} />
            <StatCard title="Model Status" value={sysStatus?.model_available ? 'Ready' : 'Unavailable'} icon={sysStatus?.model_available ? CheckCircle : AlertTriangle} color={sysStatus?.model_available ? 'text-brand-success' : 'text-brand-danger'} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <div className="glass-panel rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">Weather / Location Context</h3>
              <div className="space-y-4">
                <div className="bg-slate-800/50 p-4 rounded-xl border border-white/5">
                  <span className="text-sm font-semibold tracking-wider uppercase text-slate-400">Weather API</span>
                  <p className="font-medium text-white mt-1">Not Available (API key missing)</p>
                </div>
                <div className="bg-slate-800/50 p-4 rounded-xl border border-white/5">
                  <span className="text-sm font-semibold tracking-wider uppercase text-slate-400">Location API</span>
                  <p className="font-medium text-white mt-1">Not Available (No real geolocation source)</p>
                </div>
              </div>
            </div>

            <div className="glass-panel rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center"><History className="mr-2" size={20}/> Latest Activity</h3>
              {stats.latest ? (
                <div className="flex items-center justify-between bg-slate-800/50 p-4 rounded-xl border border-white/5">
                  <div>
                    <p className="font-medium">{stats.latest.image_name}</p>
                    <p className="text-sm text-slate-400 text-xs mt-1">{new Date(stats.latest.timestamp).toLocaleString()}</p>
                  </div>
                  <div className="px-4 py-2 rounded-lg text-sm font-semibold bg-blue-500/20 text-blue-400">
                    Prediction Logged
                  </div>
                </div>
              ) : (
                <p className="text-slate-400 italic">No predictions made yet.</p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function DatasetView() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    axios.get(`${API_URL}/dataset-info`).then(res => setData(res.data)).catch(console.error);
  }, []);

  if (!data) return <LoadingSpinner />;

  const chartData = Object.entries(data.class_distribution).map(([name, count]) => ({ name, count }));

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white tracking-tight">Dataset Information</h2>
        <p className="text-slate-400 mt-1">Source data characteristics and distribution</p>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <StatCard title="Total Images" value={data.total_images} />
        <StatCard title="Valid Images" value={data.valid_images} />
        <StatCard title="Train Split" value={data.train_split} />
        <StatCard title="Val/Test Split" value={`${data.val_split} / ${data.test_split}`} />
        <StatCard title="Class 1 Objects" value={data.class_1_objects} />
        <StatCard title="Class n Objects" value={data.class_n_objects} />
        <StatCard title="Image Size" value={data.image_size} />
        <StatCard title="Corrected OOB Boxes" value={data.corrected_oob} />
      </div>

      <div className="glass-panel rounded-2xl p-6 mt-8">
        <h3 className="text-lg font-semibold mb-2">Exclusions</h3>
        <p className="text-slate-400">Excluded empty/garbled labels: {data.excluded_empty}</p>
        <p className="text-slate-400">Excluded apostrophe label: {data.excluded_apostrophe}</p>
      </div>
    </div>
  );
}

function ModelView() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    axios.get(`${API_URL}/model-performance`).then(res => setData(res.data)).catch(console.error);
  }, []);

  if (!data) return <LoadingSpinner />;

  if (data.message) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] text-center animate-in zoom-in-95 duration-500">
        <AlertTriangle size={48} className="text-brand-primary mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Insufficient Data</h2>
        <p className="text-slate-400 max-w-md">{data.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white tracking-tight">Model Performance</h2>
        <p className="text-slate-400 mt-1">Evaluation metrics on the unseen test set</p>
      </header>

      <div className="glass-panel rounded-2xl p-6 mb-8 border-l-4 border-l-brand-primary">
         <h3 className="font-semibold text-lg text-white mb-2">Important Limitation</h3>
         <p className="text-slate-300">
           These are purely object-detection evaluation metrics (mAP, Precision, Recall) tested on the unseen test set (462 images).<br/>
           <span className="font-mono bg-slate-800 px-2 py-1 rounded text-sm mt-2 inline-block font-bold text-red-400">Do NOT interpret these metrics as "79.1% rockfall accuracy". The semantic meaning of Class "1" and Class "n" is NOT scientifically confirmed as rockfall.</span>
         </p>
      </div>

      <h3 className="text-xl font-bold text-white mb-4">Overall Performance</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
        <StatCard title="Precision" value={(data.overall.precision * 100).toFixed(1) + '%'} />
        <StatCard title="Recall" value={(data.overall.recall * 100).toFixed(1) + '%'} />
        <StatCard title="mAP@50" value={(data.overall.map50 * 100).toFixed(1) + '%'} />
        <StatCard title="mAP@50-95" value={(data.overall.map50_95 * 100).toFixed(1) + '%'} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-bold text-white mb-4">Class '1' Metrics</h3>
          <div className="grid grid-cols-2 gap-4">
            <StatCard title="Precision" value={(data.class_1.precision * 100).toFixed(1) + '%'} />
            <StatCard title="Recall" value={(data.class_1.recall * 100).toFixed(1) + '%'} />
            <StatCard title="mAP@50" value={(data.class_1.map50 * 100).toFixed(1) + '%'} />
            <StatCard title="mAP@50-95" value={(data.class_1.map50_95 * 100).toFixed(1) + '%'} />
          </div>
        </div>
        <div>
          <h3 className="text-lg font-bold text-white mb-4">Class 'n' Metrics</h3>
          <div className="grid grid-cols-2 gap-4">
            <StatCard title="Precision" value={(data.class_n.precision * 100).toFixed(1) + '%'} />
            <StatCard title="Recall" value={(data.class_n.recall * 100).toFixed(1) + '%'} />
            <StatCard title="mAP@50" value={(data.class_n.map50 * 100).toFixed(1) + '%'} />
            <StatCard title="mAP@50-95" value={(data.class_n.map50_95 * 100).toFixed(1) + '%'} />
          </div>
        </div>
      </div>
    </div>
  );
}

function PredictionView() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setPreview(URL.createObjectURL(e.target.files[0]));
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source', 'User Uploaded Sample');

    try {
      const res = await axios.post(`${API_URL}/predict`, formData);
      if (res.data.error) setError(res.data.error);
      else setResult(res.data);
    } catch (err) {
      setError("Failed to connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-white tracking-tight">Manual Image Prediction</h2>
        <p className="text-slate-400 mt-1">Upload a sample to detect potential rockfall risks</p>
      </header>

      <div className="glass-panel rounded-3xl p-8 border border-white/10 shadow-2xl">
        {!preview ? (
          <div className="border-2 border-dashed border-slate-600 rounded-2xl p-12 text-center hover:bg-white/5 transition cursor-pointer relative">
            <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" accept="image/*" onChange={handleFileChange} />
            <UploadCloud size={48} className="mx-auto text-slate-400 mb-4" />
            <h3 className="text-lg font-medium text-white">Drag & drop an image or click to browse</h3>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="relative rounded-xl overflow-hidden bg-black/50 aspect-video flex items-center justify-center">
              <img src={preview} alt="Preview" className="max-h-full object-contain" />
            </div>
            <div className="flex justify-center space-x-4">
              <button onClick={() => { setPreview(null); setFile(null); setResult(null); }} className="px-6 py-2.5 rounded-xl border border-slate-600 hover:bg-slate-800 transition">
                Clear
              </button>
              <button onClick={handleUpload} disabled={loading} className="px-6 py-2.5 rounded-xl bg-brand-primary text-slate-900 font-semibold hover:bg-amber-400 transition flex items-center">
                {loading ? <><Loader2 size={18} className="animate-spin mr-2"/> Analyzing...</> : 'Analyze Image'}
              </button>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-500/20 text-red-400 p-4 rounded-xl flex items-center">
          <AlertTriangle className="mr-3" /> {error}
        </div>
      )}

      {result && <ResultCard result={result} />}
    </div>
  );
}

function SimulationView() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const simulate = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`${API_URL}/simulate`);
      if (res.data.error) setError(res.data.error);
      else setResult(res.data);
    } catch (err) {
      setError("Failed to connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8 text-center">
        <div className="inline-flex items-center space-x-2 bg-brand-primary/20 text-brand-primary px-3 py-1 rounded-full text-sm font-medium mb-4">
          <PlaySquare size={16} /> <span>DATASET SIMULATION MODE</span>
        </div>
        <h2 className="text-3xl font-bold text-white tracking-tight">Sequential Dataset Processing</h2>
        <p className="text-slate-400 mt-1">Source: Actual Dataset (Not live CCTV)</p>
      </header>

      <div className="text-center mb-8">
        <button onClick={simulate} disabled={loading} className="px-8 py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-500 transition shadow-lg shadow-indigo-600/30 flex items-center mx-auto text-lg">
          {loading ? <><Loader2 size={24} className="animate-spin mr-3"/> Processing next image...</> : 'Process Next Image from Dataset'}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/20 text-red-400 p-4 rounded-xl flex items-center max-w-lg mx-auto">
          <AlertTriangle className="mr-3" /> {error}
        </div>
      )}

      {result && <ResultCard result={result} />}
    </div>
  );
}

function HistoryView() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/history`)
      .then(res => setHistory(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white tracking-tight">Prediction History</h2>
        <p className="text-slate-400 mt-1">Log of all processed images and risk assessments</p>
      </header>

      <div className="glass-panel rounded-2xl overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-800/50 border-b border-white/10 text-slate-300 text-sm">
              <th className="px-6 py-4 font-medium">Timestamp</th>
              <th className="px-6 py-4 font-medium">Image Source</th>
              <th className="px-6 py-4 font-medium">Detected Classes</th>
              <th className="px-6 py-4 font-medium">Alert Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {history.map(row => {
              let isAlert = false;
              if (row.alert_interpretation) {
                isAlert = row.alert_interpretation.includes('ALERT');
              } else {
                try {
                  const confs = JSON.parse(row.confidence || '[]');
                  isAlert = confs.some(c => parseFloat(c) > 0.5);
                } catch {}
              }
              
              const classes = JSON.parse(row.detected_classes || '[]');
              
              return (
                <tr key={row.id} className="hover:bg-white/5 transition">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                    {new Date(row.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-white">{row.image_name}</div>
                    <div className="text-xs text-brand-primary">{row.source}</div>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-300">
                    {classes.length > 0 ? classes.join(', ') : 'None'}
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-500/20 text-slate-400">
                      Alerts Disabled (No proven risk rule)
                    </span>
                  </td>
                </tr>
              )
            })}
            {history.length === 0 && (
              <tr>
                <td colSpan="4" className="px-6 py-8 text-center text-slate-500 italic">No prediction history found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ================= COMPONENTS =================

const StatCard = ({ title, value, icon: Icon, color = 'text-brand-primary' }) => (
  <div className="glass-panel rounded-2xl p-6 flex flex-col justify-between group hover:border-white/20 transition-colors">
    <div className="flex justify-between items-start mb-4">
      <h3 className="text-slate-400 font-medium">{title}</h3>
      {Icon && <Icon size={20} className={color} />}
    </div>
    <p className={`text-3xl font-bold ${typeof value === 'number' || typeof value === 'string' ? 'text-white' : ''}`}>{value}</p>
  </div>
);

const ResultCard = ({ result }) => {
  const isAlert = false; // No fake alerts
  
  // Calculate relative positions for bounding boxes
  const nativeWidth = result.image_width || 1024;
  const nativeHeight = result.image_height || 1024;
  const bboxes = result.bounding_boxes || [];
  
  const getImageUrl = () => {
    return `http://127.0.0.1:8000${result.annotated_image_url}`;
  };

  return (
    <div className="glass-panel rounded-3xl p-8 mt-6 border border-white/10 animate-in fade-in slide-in-from-bottom-4 shadow-xl">
      <div className="flex flex-col md:flex-row gap-8">
        <div className="flex-1 space-y-6">
          <div>
            <h3 className="text-sm text-slate-400 font-semibold tracking-wider uppercase">Source File</h3>
            <p className="text-xl text-white font-medium break-all">{result.image_name || "Uploaded/Simulated Image"}</p>
          </div>
          
          <div className="relative rounded-xl overflow-hidden bg-black/50 aspect-video flex items-center justify-center">
             <img src={getImageUrl()} alt="Result" className="max-h-full object-contain relative" style={{ width: '100%', height: '100%' }} />
          </div>

          <div>
            <h3 className="text-sm text-slate-400 font-semibold tracking-wider uppercase mb-3">Model Output</h3>
            {result.detections && result.detections.length > 0 ? (
              <div className="space-y-2">
                {result.detections.map((det, idx) => (
                  <div key={idx} className="flex justify-between items-center bg-slate-800/50 p-3 rounded-lg border border-white/5">
                    <span className="font-medium text-white">Class: {det.class_name} (ID: {det.class_id})</span>
                    <span className="text-brand-primary text-sm font-mono">{(det.confidence * 100).toFixed(1)}% conf</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-500 italic">No objects detected.</p>
            )}
          </div>
        </div>
        
        <div className="md:w-72">
          <div className={`p-6 rounded-2xl h-full border bg-slate-800/30 border-slate-700/50`}>
            <h3 className="text-sm font-semibold tracking-wider uppercase mb-4 text-white">Alert Interpretation</h3>
            
            <div className="flex items-center mb-4">
              <Info size={32} className="text-blue-400 mr-3" />
              <span className={`text-xl font-bold text-blue-400`}>
                Object Detection Only
              </span>
            </div>
            
            <p className="text-sm text-slate-300 leading-relaxed font-mono">
              {result.alert_interpretation}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const LoadingSpinner = () => (
  <div className="flex flex-col items-center justify-center h-[60vh]">
    <Loader2 size={48} className="animate-spin text-brand-primary mb-4" />
    <p className="text-slate-400">Loading data...</p>
  </div>
);
