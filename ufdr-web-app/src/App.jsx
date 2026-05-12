import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Plus, MessageSquare, Shield, FileText, Ticket, Moon, Sun, Send,
  Terminal, User, Activity, Layout, Search, BarChart2, Info, ArrowLeft,
  Clock, RotateCcw, ChevronRight, Download, Users, ExternalLink, Loader2,
  AlertTriangle, CheckCircle, MoreVertical, Trash2, Edit3, X, Network, Maximize2,
  BookOpen, Layers, Database, HardDrive, Share2, ZoomIn, ZoomOut, RefreshCw,
  BadgeCheck, Fingerprint
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion, AnimatePresence } from 'framer-motion';
import mermaid from 'mermaid';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

// Investigating Officer ID Card
const OfficerIDCard = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9, y: 5 }}
      className="absolute top-full right-0 mt-6 w-80 bg-[#16171a] border border-white/10 rounded-[2.5rem] shadow-[0_30px_60px_rgba(0,0,0,0.8)] overflow-hidden z-[200] backdrop-blur-3xl"
    >
      <div className="h-2 bg-forensic-green shadow-[0_0_15px_rgba(0,255,65,0.5)]"></div>
      <div className="p-8">
        <div className="flex items-center gap-6 mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-forensic-green to-transparent p-0.5 shadow-2xl">
            <div className="w-full h-full bg-[#16171a] rounded-[0.9rem] flex items-center justify-center text-forensic-green">
              <Fingerprint size={32} />
            </div>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <div className="w-2 h-2 rounded-full bg-forensic-green animate-pulse"></div>
              <span className="text-[9px] font-black uppercase tracking-[0.3em] text-forensic-green">Active Duty</span>
            </div>
            <h3 className="text-xl font-black italic uppercase tracking-tighter text-white">Aman Choudhary</h3>
          </div>
        </div>

        <div className="space-y-6">
          <div className="pb-4 border-b border-white/5">
            <p className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-500 mb-1">Designation</p>
            <p className="text-sm font-bold text-gray-200">Senior Investigating Officer</p>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-500 mb-1">Unit</p>
              <p className="text-[11px] font-bold text-gray-200">Forensic Unit 01</p>
            </div>
            <div>
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-500 mb-1">Badge ID</p>
              <p className="text-[11px] font-bold text-forensic-green font-jetbrains tracking-wider">SIO-1024-AC</p>
            </div>
          </div>
          <div className="pt-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <BadgeCheck size={14} className="text-blue-500" />
              <span className="text-[9px] font-black uppercase tracking-widest text-gray-500">Security Verified</span>
            </div>
            <span className="text-[9px] font-black uppercase tracking-widest text-gray-700 font-jetbrains italic">Clearance: TS/SCI</span>
          </div>
        </div>
      </div>
      <div className="bg-white/5 p-4 text-center border-t border-white/5">
        <p className="text-[8px] font-black text-gray-500 uppercase tracking-[0.4em]">UFDR COMMAND // GLOBAL RESPONSE FORCE</p>
      </div>
    </motion.div>
  );
};

// Officer Avatar Component
const OfficerAvatar = () => {
  const [isHovered, setIsHovered] = useState(false);
  return (
    <div className="relative" onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)}>
      <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-forensic-green/30 to-transparent border border-forensic-green/40 flex items-center justify-center text-forensic-green font-black text-lg shadow-2xl cursor-help hover:border-forensic-green transition-all">AC</div>
      <AnimatePresence>
        {isHovered && <OfficerIDCard />}
      </AnimatePresence>
    </div>
  );
};

// Forensic Evidence Card (The Hover Preview)
const EvidenceCard = ({ title, snippet, id, type }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 5, scale: 0.98 }}
      className="absolute z-[200] bottom-full mb-4 left-1/2 -translate-x-1/2 w-80 bg-[#1a1b1e] border border-white/10 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden backdrop-blur-3xl"
    >
      <div className="p-4 border-b border-white/5 bg-white/[0.02] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-forensic-green/20 text-forensic-green rounded-lg">
            {type === 'database' ? <Database size={14} /> : <FileText size={14} />}
          </div>
          <span className="text-[11px] font-black uppercase tracking-widest text-gray-400 truncate max-w-[150px]">{title}</span>
        </div>
        <div className="text-[9px] font-jetbrains text-gray-600 uppercase tracking-tighter italic">Source Verified</div>
      </div>
      <div className="p-5 space-y-3">
        <h4 className="text-white font-bold text-sm leading-tight line-clamp-2">{title}</h4>
        <p className="text-gray-500 text-[11px] leading-relaxed line-clamp-3 italic">"{snippet || "Telemetric data trace from enterprise forensic log."}"</p>
        <div className="flex items-center justify-between pt-2">
          <span className="text-[9px] font-black text-forensic-green uppercase tracking-[0.2em]">{id || "DOC_ID: 1042-X"}</span>
          <ExternalLink size={12} className="text-gray-700" />
        </div>
      </div>
    </motion.div>
  );
};

// Citation Pill with Hover State
const CitationPill = ({ label, index, evidence }) => {
  const [isHovered, setIsHovered] = useState(false);
  return (
    <span className="relative inline-block align-baseline group" onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)}>
      <sup className="mx-0.5 pointer-events-auto">
        <span className="inline-flex items-center justify-center bg-white text-black text-[9px] font-black px-1.5 py-0.5 rounded-full hover:bg-forensic-green transition-all cursor-help shadow-sm border border-white/20">
          {index + 1}
        </span>
      </sup>
      <AnimatePresence>
        {isHovered && (
          <EvidenceCard title={label} snippet={evidence?.content || "Historical forensic log entry."} id={evidence?.id || `CID-${index}`} type="file" />
        )}
      </AnimatePresence>
    </span>
  );
};

// Component to render the "Sources" bar at the top of messages
const SourceBar = ({ text, evidenceSet = [] }) => {
  const citations = [...new Set(text.match(/【[^】]+】/g) || [])];
  const [hoveredIdx, setHoveredIdx] = useState(null);
  if (citations.length === 0) return null;
  return (
    <div className="flex items-center gap-3 mb-8 animate-in fade-in slide-in-from-top-2 duration-700">
      <div className="flex -space-x-3">
        <div className="w-7 h-7 rounded-full bg-forensic-green border-2 border-chat-bg flex items-center justify-center text-black shadow-lg z-30"><Database size={12} /></div>
        <div className="w-7 h-7 rounded-full bg-blue-500 border-2 border-chat-bg flex items-center justify-center text-white shadow-lg z-20"><HardDrive size={12} /></div>
        <div className="w-7 h-7 rounded-full bg-orange-500 border-2 border-chat-bg flex items-center justify-center text-white shadow-lg z-10"><Shield size={12} /></div>
      </div>
      <div className="flex items-center gap-3 bg-white/5 border border-white/10 rounded-2xl px-5 py-2 shadow-2xl backdrop-blur-xl group relative">
        <span className="text-[10px] font-black uppercase tracking-[0.3em] text-gray-500 border-r border-white/10 pr-4 mr-1">Sources</span>
        <div className="flex gap-3">
          {citations.slice(0, 4).map((c, i) => {
            const label = c.replace(/[【】]/g, '');
            const evidence = evidenceSet[i] || {};
            return (
              <div key={i} className="relative" onMouseEnter={() => setHoveredIdx(i)} onMouseLeave={() => setHoveredIdx(null)}>
                <span className="text-[11px] font-bold text-forensic-green/80 hover:text-forensic-green transition-colors cursor-help flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-forensic-green/40"></div> {label.substring(0, 18)}{label.length > 18 ? '...' : ''}
                </span>
                <AnimatePresence>{hoveredIdx === i && (<EvidenceCard title={label} snippet={evidence.content} id={evidence.id || `LOG-${i}`} type="database" />)}</AnimatePresence>
              </div>
            );
          })}
          {citations.length > 4 && (<span className="text-[10px] font-bold text-gray-600 flex items-center">+{citations.length - 4} MORE</span>)}
        </div>
      </div>
    </div>
  );
};

// Custom Markdown Components
const getMarkdownComponents = (evidenceSet = []) => ({
  text: ({ value }) => {
    const parts = value.split(/(【[^】]+】)/g);
    let citationCount = 0;
    return parts.map((part, i) => {
      if (part.startsWith('【') && part.endsWith('】')) {
        const sourceName = part.slice(1, -1);
        const idx = citationCount++;
        return <CitationPill key={i} label={sourceName} index={idx} evidence={evidenceSet[idx]} />;
      }
      return part;
    });
  }
});

const Typewriter = ({ text, speed = 8, evidenceSet = [], onComplete }) => {
  const [displayedText, setDisplayedText] = useState('');
  useEffect(() => {
    let i = 0;
    const timer = setInterval(() => {
      setDisplayedText(text.slice(0, i));
      i++;
      if (i > text.length) { clearInterval(timer); if (onComplete) onComplete(); }
    }, speed);
    return () => clearInterval(timer);
  }, [text, onComplete]);
  return (
    <div>
      <SourceBar text={text} evidenceSet={evidenceSet} />
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={getMarkdownComponents(evidenceSet)}>{displayedText}</ReactMarkdown>
    </div>
  );
};

const ForensicGraph = ({ chart }) => {
  const [svg, setSvg] = useState('');

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'loose', fontFamily: 'JetBrains Mono', themeVariables: { primaryColor: '#00ff41', primaryTextColor: '#fff', primaryBorderColor: '#00ff41', lineColor: '#00ff41', secondaryColor: '#ff4136', tertiaryColor: '#202123' } });
  }, []);

  useEffect(() => {
    if (chart && chart.trim()) {
      const renderGraph = async () => {
        try {
          const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
          const { svg } = await mermaid.render(id, chart);
          setSvg(svg);
        } catch (err) { console.error(err); }
      };
      renderGraph();
    }
  }, [chart]);

  return (
    <div className="w-full h-full bg-[#0b0c0e] rounded-[2.5rem] border border-white/5 relative overflow-hidden group shadow-2xl">
      <TransformWrapper
        initialScale={0.7}
        centerOnInit={true}
        minScale={0.01}
        maxScale={15}
        limitToBounds={false}
        centerZoomedOut={true}
      >
        {({ zoomIn, zoomOut, resetTransform, centerView }) => (
          <>
            <div className="absolute top-10 right-10 z-50 flex flex-col gap-3 bg-black/80 backdrop-blur-2xl border border-white/10 p-2.5 rounded-3xl shadow-2xl opacity-0 group-hover:opacity-100 transition-all duration-500 scale-90 group-hover:scale-100">
              <button onClick={() => zoomIn()} className="p-3.5 hover:bg-forensic-green/20 rounded-2xl text-gray-400 hover:text-forensic-green transition-all shadow-lg"><ZoomIn size={22} /></button>
              <button onClick={() => zoomOut()} className="p-3.5 hover:bg-forensic-green/20 rounded-2xl text-gray-400 hover:text-forensic-green transition-all shadow-lg"><ZoomOut size={22} /></button>
              <button onClick={() => { resetTransform(); setTimeout(() => centerView(), 150); }} className="p-3.5 hover:bg-forensic-green/20 rounded-2xl text-gray-400 hover:text-forensic-green transition-all shadow-lg"><RefreshCw size={22} /></button>
            </div>
            <div className="absolute bottom-10 left-10 z-50 px-6 py-3 bg-forensic-green/5 backdrop-blur-3xl border border-forensic-green/20 rounded-full opacity-40 group-hover:opacity-100 transition-opacity pointer-events-none">
              <span className="text-[10px] font-black uppercase tracking-[0.4em] text-forensic-green italic">Navigation Active // Use Mouse to Explore</span>
            </div>
            <TransformComponent wrapperClassName="!w-full !h-full" contentClassName="!w-full !h-full !flex !items-center !justify-center">
              {svg ? (
                <div className="forensic-graph-svg cursor-grab active:cursor-grabbing transition-all flex items-center justify-center p-40" dangerouslySetInnerHTML={{ __html: svg }} />
              ) : (
                <div className="flex flex-col items-center gap-6 text-gray-700"><Loader2 className="animate-spin" size={40} /><p className="text-[11px] font-black uppercase tracking-[0.5em] italic animate-pulse">Syncing Shard Topology...</p></div>
              )}
            </TransformComponent>
          </>
        )}
      </TransformWrapper>
    </div>
  );
};

const App = () => {
  const [view, setView] = useState('welcome');
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [sessionData, setSessionData] = useState(null);
  const [tickets, setTickets] = useState([]);

  const [investigationProgress, setInvestigationProgress] = useState(0);
  const [investigationMessage, setInvestigationMessage] = useState('');
  const [isInvestigating, setIsInvestigating] = useState(false);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [customQuery, setCustomQuery] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [showGraph, setShowGraph] = useState(false);

  const [activeMenuId, setActiveMenuId] = useState(null);
  const [isRenameModalOpen, setIsRenameModalOpen] = useState(false);
  const [newName, setNewName] = useState('');
  const [renameTargetId, setRenameTargetId] = useState(null);

  const chatEndRef = useRef(null);

  useEffect(() => { fetchSessions(); fetchTickets(); }, []);

  const fetchSessions = async () => {
    try { const { data } = await axios.get('/api/sessions'); setSessions(data); } catch (err) { console.error(err); }
  };

  const fetchTickets = async () => {
    try { const { data } = await axios.get('/api/tickets'); setTickets(data); } catch (err) { console.error(err); }
  };

  const loadSession = async (id) => {
    if (isInvestigating && currentSessionId === id) { setView('investigating'); return; }
    try {
      setCurrentSessionId(id);
      const { data } = await axios.get(`/api/session/${id}`);
      if (!data.report && isInvestigating) { setView('investigating'); return; }
      setSessionData(data);
      const rawHistory = data.chat_history || [];
      setMessages(rawHistory.filter(m => m.role && m.role !== 'system').map(m => ({
        role: (m.role === 'assistant' || m.role === 'ai') ? 'ai' : 'user',
        content: m.content || m.message || "", isOld: true
      })));
      setView('report');
      setShowGraph(false);
      setActiveMenuId(null);
    } catch (err) { console.error(err); }
  };

  const switchView = (newView) => {
    if (view === 'chat' && newView !== 'chat') { setMessages(prev => prev.map(m => ({ ...m, isOld: true }))); }
    setView(newView);
  };

  const startInvestigation = async (query) => {
    if (isInvestigating || !query.trim()) return;
    setIsInvestigating(true);
    setView('investigating');
    setInvestigationProgress(5);
    setInvestigationMessage('Parallel Retrieval...');
    setMessages([{ role: 'user', content: query }]);
    try {
      const { data } = await axios.post('/api/investigate', { query });
      const sessionId = data.session_id;
      setCurrentSessionId(sessionId);
      setTimeout(() => fetchSessions(), 800);
      pollStatus(sessionId);
    } catch (err) { setView('welcome'); setIsInvestigating(false); }
  };

  const pollStatus = async (sessionId) => {
    const interval = setInterval(async () => {
      try {
        const { data } = await axios.get(`/api/status/${sessionId}`);
        if (data.progress !== undefined) {
          setInvestigationProgress(data.progress);
          setInvestigationMessage(data.message || 'Analyzing...');
        }
        if (data.status === 'complete') {
          clearInterval(interval);
          const sessionResp = await axios.get(`/api/session/${sessionId}`);
          setSessionData(sessionResp.data);
          const rawHistory = sessionResp.data.chat_history || [];
          setMessages(rawHistory.filter(m => m.role !== 'system').map(m => ({
            role: (m.role === 'assistant' || m.role === 'ai') ? 'ai' : 'user',
            content: m.content || m.message || "", isOld: true
          })));
          setView('report');
          setIsInvestigating(false);
          fetchSessions();
        } else if (data.status === 'failed') { clearInterval(interval); setIsInvestigating(false); setView('welcome'); }
      } catch (err) { console.error(err); }
    }, 1000);
  };

  const handleSend = async () => {
    if (!input.trim() || isInvestigating) return;
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev.map(m => ({ ...m, isOld: true })), { role: 'user', content: userMsg }]);
    try {
      const { data } = await axios.post('/api/chat', { session_id: currentSessionId, message: userMsg });
      setMessages(prev => [...prev, { role: 'ai', content: data.response, isOld: false }]);
    } catch (err) { setMessages(prev => [...prev, { role: 'ai', content: "Evidence Stream Severed." }]); }
  };

  const exitToNew = () => {
    if (isInvestigating) return;
    setCurrentSessionId(null);
    setSessionData(null);
    setMessages([]);
    setView('welcome');
    setCustomQuery('');
    setShowGraph(false);
  };

  const markMessageAsOld = (idx) => {
    setMessages(prev => {
      const next = [...prev];
      if (next[idx]) next[idx].isOld = true;
      return next;
    });
  };

  return (
    <div className="flex h-screen bg-chat-bg font-inter text-white overflow-hidden selection:bg-forensic-green/30">
      {/* Rename Modal */}
      {isRenameModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-xl">
          <div className="bg-sidebar-bg border border-white/10 p-12 rounded-[3.5rem] w-full max-w-lg shadow-2xl">
            <div className="flex items-center gap-4 mb-8">
              <div className="p-3 bg-forensic-green/10 text-forensic-green rounded-2xl"><Edit3 size={24} /></div>
              <h3 className="text-2xl font-black uppercase italic">Rename Dossier</h3>
            </div>
            <input type="text" value={newName} onChange={(e) => setNewName(e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-[1.5rem] p-6 mb-10 text-xl focus:outline-none focus:border-forensic-green" />
            <div className="flex gap-4">
              <button onClick={() => setIsRenameModalOpen(false)} className="flex-1 p-5 rounded-2xl border border-white/10 hover:bg-white/5 font-bold uppercase tracking-widest">Cancel</button>
              <button onClick={() => axios.patch(`/api/session/${renameTargetId}`, { new_query: newName }).then(() => { setIsRenameModalOpen(false); fetchSessions(); })} className="flex-1 p-5 rounded-2xl bg-forensic-green text-black font-black uppercase tracking-widest shadow-xl shadow-forensic-green/20">Apply</button>
            </div>
          </div>
        </div>
      )}

      {/* Sidebar */}
      <aside className={`bg-sidebar-bg flex flex-col border-r border-white/10 transition-all duration-700 ease-in-out relative z-30 ${isSidebarOpen ? 'w-96' : 'w-0 overflow-hidden'}`}>
        <div className="p-8 flex flex-col h-full">
          <button onClick={exitToNew} className="flex items-center justify-center gap-4 w-full bg-white/[0.02] border border-white/5 p-6 rounded-[2rem] hover:bg-white/[0.06] hover:border-forensic-green/40 transition-all text-sm font-black uppercase tracking-widest shadow-2xl mb-12">
            <Plus size={20} className="text-forensic-green" /> New Analysis
          </button>

          <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar pr-2">
            {sessions.map(s => (
              <div key={s.id} className="relative group">
                <button onClick={() => loadSession(s.id)} className={`flex items-center gap-4 w-full p-5 rounded-[1.8rem] text-[12px] text-left transition-all ${currentSessionId === s.id ? 'bg-white/10 text-forensic-green shadow-xl' : 'text-gray-500 hover:bg-white/[0.02] hover:text-gray-300'}`}>
                  <Shield size={12} className={currentSessionId === s.id ? 'text-forensic-green' : 'text-gray-700'} />
                  <span className="truncate font-bold flex-1">{s.query}</span>
                </button>
                <button onClick={(e) => { e.stopPropagation(); setActiveMenuId(activeMenuId === s.id ? null : s.id); }} className="absolute right-4 top-1/2 -translate-y-1/2 p-2 opacity-0 group-hover:opacity-100 transition-all text-gray-600 hover:text-white"><MoreVertical size={16} /></button>
                {activeMenuId === s.id && (
                  <div className="absolute right-0 top-16 z-[100] bg-sidebar-bg/95 border border-white/10 rounded-[1.5rem] shadow-2xl p-3 w-56 backdrop-blur-2xl">
                    <button onClick={() => { setRenameTargetId(s.id); setNewName(s.query); setIsRenameModalOpen(true); setActiveMenuId(null); }} className="flex items-center gap-4 w-full p-4 rounded-xl hover:bg-white/5 text-[11px] font-bold text-gray-400 hover:text-white"><Edit3 size={14} /> Rename Dossier</button>
                    <button onClick={() => axios.delete(`/api/session/${s.id}`).then(() => { if (currentSessionId === s.id) exitToNew(); fetchSessions(); })} className="flex items-center gap-4 w-full p-4 rounded-xl hover:bg-red-500/10 text-[11px] font-bold text-red-500/60 hover:text-red-500"><Trash2 size={14} /> Purge Evidence</button>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-auto space-y-4 pt-10 border-t border-white/5">
            <button onClick={() => switchView('about')} className={`flex items-center gap-4 w-full p-4 rounded-2xl transition-all ${view === 'about' ? 'bg-forensic-green/10 text-forensic-green' : 'text-gray-600 hover:text-white'}`}><Users size={18} /> <span className="text-[11px] font-black uppercase tracking-[0.2em]">Team Infraglyph</span></button>
            <button onClick={() => switchView('tickets')} className={`flex items-center gap-4 w-full p-4 rounded-2xl transition-all ${view === 'tickets' ? 'bg-forensic-red/10 text-forensic-red' : 'text-gray-600 hover:text-white'}`}><Ticket size={18} /> <span className="text-[11px] font-black uppercase tracking-[0.2em]">Escalations</span></button>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col bg-chat-bg relative">
        <header className="h-24 border-b border-white/10 flex items-center justify-between px-12 bg-chat-bg/60 backdrop-blur-3xl z-40">
          <div className="flex items-center gap-8">
            <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="p-4 hover:bg-white/5 rounded-2xl text-gray-500"><Layout size={24} /></button>
            <h1 className="text-sm font-black tracking-[0.4em] uppercase italic">UFDR <span className="text-forensic-green">COMMAND</span></h1>
          </div>

          <AnimatePresence>
            {currentSessionId && !isInvestigating && (
              <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="flex bg-white/[0.02] p-2 rounded-[2rem] border border-white/10 shadow-2xl backdrop-blur-xl">
                <button onClick={() => switchView('report')} className={`px-12 py-3 rounded-[1.5rem] text-[11px] font-black tracking-[0.2em] transition-all ${view === 'report' ? 'bg-forensic-green text-black shadow-lg shadow-forensic-green/30' : 'text-gray-500'}`}>REPORT</button>
                <button onClick={() => switchView('chat')} className={`px-12 py-3 rounded-[1.5rem] text-[11px] font-black tracking-[0.2em] transition-all ${view === 'chat' ? 'bg-forensic-green text-black shadow-lg shadow-forensic-green/30' : 'text-gray-500'}`}>CHAT</button>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="flex items-center gap-4">
            <button onClick={() => window.location.reload()} className="p-3 text-gray-600 hover:text-forensic-green transition-all"><RotateCcw size={22} /></button>
            <OfficerAvatar />
          </div>
        </header>

        <div className="flex-1 relative overflow-hidden z-0">
          <AnimatePresence mode="wait">
            {view === 'welcome' && (
              <motion.div key="welcome" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="h-full flex flex-col items-center justify-center text-center px-4 overflow-y-auto">
                <div className="space-y-6 max-w-4xl py-20">
                  <div className="w-24 h-24 bg-gradient-to-br from-forensic-green/20 to-transparent text-forensic-green rounded-[2.5rem] flex items-center justify-center mx-auto border border-forensic-green/30 shadow-2xl"><Shield size={48} /></div>
                  <h2 className="text-6xl font-black tracking-tighter uppercase italic">Infraglyph <span className="text-forensic-green">UFDR</span></h2>
                  <p className="text-gray-500 font-medium text-xl">Autonomous Forensic Intelligence & Evidence Synthesis</p>

                  <div className="max-w-2xl mx-auto w-full relative mt-16 mb-20 group">
                    <input type="text" value={customQuery} onChange={(e) => setCustomQuery(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && startInvestigation(customQuery)} placeholder="Enter investigation parameters..." className="relative w-full bg-white/[0.03] border border-white/10 rounded-[1.8rem] py-7 px-10 text-xl focus:outline-none focus:border-forensic-green transition-all shadow-2xl backdrop-blur-2xl" />
                    <button onClick={() => startInvestigation(customQuery)} className="absolute right-5 top-5 bg-forensic-green text-black p-4 rounded-2xl hover:scale-110 active:scale-95 transition-all shadow-xl shadow-forensic-green/20"><Search size={24} /></button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                    {[
                      { label: "Analyze suspicious logins", query: "Analyze all suspicious login events in Jan 2010" },
                      { label: "Audit file transfers", query: "Audit all high-volume file transfers for user FEB0306" },
                      { label: "Map attack surface", query: "Generate a full attack surface map for user CSC0217" },
                      { label: "Data exfiltration audit", query: "Investigate possible data exfiltration in Feb 2010" }
                    ].map((item, idx) => (
                      <button key={idx} onClick={() => startInvestigation(item.query)} className="bg-white/[0.02] border border-white/5 p-8 rounded-[2rem] hover:bg-white/[0.05] hover:border-forensic-green/40 transition-all group backdrop-blur-md">
                        <div className="flex justify-between items-center mb-2"><span className="font-bold text-gray-200 text-lg">{item.label}</span><ChevronRight size={20} className="text-gray-600 group-hover:text-forensic-green transition-colors" /></div>
                        <p className="text-[10px] text-gray-500 font-jetbrains uppercase tracking-widest">RAG ENGINE: READY</p>
                      </button>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {view === 'report' && (
              <motion.div key="report" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full flex flex-col bg-chat-bg relative">
                {showGraph && (
                  <div className="absolute inset-0 z-50 bg-sidebar-bg/95 backdrop-blur-xl p-12 flex flex-col">
                    <div className="flex justify-between items-center mb-8">
                      <div className="flex items-center gap-4"><Network className="text-forensic-green" size={32} /><h3 className="text-2xl font-black uppercase italic tracking-wider">Enterprise Attack Surface Topology</h3></div>
                      <button onClick={() => setShowGraph(false)} className="p-4 bg-white/5 rounded-2xl hover:bg-red-500/10 text-gray-500 hover:text-red-500 transition-all"><X size={24} /></button>
                    </div>
                    <div className="flex-1 min-h-0"><ForensicGraph chart={sessionData?.graph_code} /></div>
                  </div>
                )}

                <div className="flex-1 overflow-y-auto p-10 md:p-24 max-w-6xl mx-auto w-full custom-scrollbar">
                  <div className="flex justify-between items-start mb-16 pb-8 border-b border-white/10">
                    <div className="flex-1 pr-10">
                      <div className="flex items-center gap-3 text-forensic-green mb-4"><Terminal size={18} /><span className="text-[11px] font-black tracking-[0.4em] uppercase">Investigative Dossier</span></div>
                      <h2 className="text-4xl font-black leading-tight mb-4">{sessionData?.query || "Forensic Report"}</h2>
                      <div className="flex items-center gap-6 text-[10px] font-jetbrains text-gray-500 uppercase tracking-widest"><span>VERDICT: GENERATED</span><span className="h-4 w-px bg-white/10"></span><span>CASE HASH: {sessionData?.case_id?.substring(0, 16)}</span></div>
                    </div>
                    <div className="flex flex-col gap-3">
                      <button onClick={() => switchView('chat')} className="group relative bg-forensic-green text-black px-12 py-5 rounded-[1.5rem] font-black hover:shadow-[0_0_40px_rgba(0,255,65,0.3)] transition-all flex items-center gap-4 overflow-hidden">
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                        <MessageSquare size={22} className="relative z-10" /> <span className="relative z-10 text-lg uppercase">Interrogate</span>
                      </button>
                      <button onClick={() => setShowGraph(true)} className="bg-white/5 border border-white/10 text-white px-12 py-4 rounded-[1.5rem] font-bold hover:bg-white/10 transition-all flex items-center justify-center gap-3">
                        <Network size={18} className="text-forensic-green" /> VIEW TOPOLOGY
                      </button>
                    </div>
                  </div>
                  <div className="markdown-body prose prose-invert max-w-none">
                    <SourceBar text={sessionData?.report || ''} evidenceSet={sessionData?.evidence_set || []} />
                    <ReactMarkdown remarkPlugins={[remarkGfm]} components={getMarkdownComponents(sessionData?.evidence_set || [])}>{sessionData?.report}</ReactMarkdown>
                  </div>
                </div>
              </motion.div>
            )}

            {view === 'chat' && (
              <motion.div key="chat" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full flex flex-col relative">
                <div className="flex-1 overflow-y-auto pt-6 pb-48 custom-scrollbar">
                  {messages.map((msg, idx) => (
                    <div key={idx} className={`py-14 px-8 md:px-56 flex gap-10 ${msg.role === 'ai' ? 'bg-white/[0.015] border-y border-white/[0.04]' : ''}`}>
                      <div className={`w-12 h-12 rounded-2xl flex-shrink-0 flex items-center justify-center shadow-xl ${msg.role === 'ai' ? 'bg-forensic-green text-black' : 'bg-white/5 text-white border border-white/10'}`}>{msg.role === 'ai' ? <Shield size={24} /> : <User size={24} />}</div>
                      <div className="flex-1 markdown-body prose prose-invert text-lg">
                        {msg.role === 'ai' && !msg.isOld ? (
                          <Typewriter text={msg.content} evidenceSet={sessionData?.evidence_set || []} onComplete={() => markMessageAsOld(idx)} />
                        ) : (
                          <>
                            {msg.role === 'ai' && <SourceBar text={msg.content} evidenceSet={sessionData?.evidence_set || []} />}
                            <ReactMarkdown remarkPlugins={[remarkGfm]} components={getMarkdownComponents(sessionData?.evidence_set || [])}>{msg.content}</ReactMarkdown>
                          </>
                        )}
                      </div>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>
                <div className="absolute bottom-0 left-0 right-0 p-10 bg-gradient-to-t from-chat-bg via-chat-bg to-transparent">
                  <div className="max-w-4xl mx-auto relative group">
                    <textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())} placeholder="Interrogate findings..." className="relative w-full bg-sidebar-bg/95 border border-white/10 rounded-[1.8rem] py-7 px-10 text-lg focus:outline-none focus:border-forensic-green/50 transition-all shadow-2xl backdrop-blur-2xl" rows={1} /><button onClick={handleSend} className="absolute right-5 bottom-5 p-4 bg-forensic-green text-black rounded-2xl hover:scale-110 shadow-xl shadow-forensic-green/20"><Send size={24} /></button>
                  </div>
                </div>
              </motion.div>
            )}

            {view === 'investigating' && <motion.div key="investigating" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full flex flex-col items-center justify-center text-center px-10"><div className="relative mb-16"><div className="absolute inset-0 bg-forensic-green/10 blur-[150px] rounded-full"></div><div className="w-40 h-40 border-[8px] border-forensic-green/10 border-t-forensic-green rounded-full animate-spin relative z-10 shadow-[0_0_50px_rgba(0,255,65,0.15)]"></div><div className="absolute inset-0 flex items-center justify-center text-forensic-green font-black text-3xl z-20 italic">{investigationProgress}%</div></div><div className="max-w-xl w-full"><div className="h-2 w-full bg-white/5 rounded-full overflow-hidden mb-6 border border-white/10 p-0.5"><motion.div initial={{ width: 0 }} animate={{ width: `${investigationProgress}%` }} className="h-full bg-forensic-green rounded-full shadow-[0_0_20px_rgba(0,255,65,0.6)]" /></div><h2 className="text-3xl font-black tracking-[0.3em] text-white uppercase italic mb-4">Autonomous Reasoning</h2><p className="text-forensic-green font-jetbrains text-xs animate-pulse tracking-[0.5em] uppercase font-bold">{investigationMessage}</p></div></motion.div>}

            {view === 'tickets' && (
              <motion.div key="tickets" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full p-16 overflow-y-auto max-w-6xl mx-auto w-full custom-scrollbar">
                <div className="flex items-center gap-6 mb-16"><div className="p-4 bg-forensic-red/20 text-forensic-red rounded-3xl"><Ticket size={32} /></div><h2 className="text-4xl font-black">Escalation Terminal</h2></div>
                <div className="grid grid-cols-1 gap-6">
                  {tickets.length === 0 ? <div className="p-32 text-center text-gray-600 border-2 border-dashed border-white/5 rounded-[3rem] font-black uppercase tracking-widest italic opacity-50">No active escalations recorded.</div> : tickets.map(t => (
                    <div key={t.ticket_id} className="bg-white/[0.02] border border-white/5 p-8 rounded-[2rem] flex justify-between items-center hover:border-forensic-red/40 transition-all group">
                      <div className="space-y-3">
                        <div className="flex items-center gap-4"><span className="font-jetbrains text-forensic-red text-sm font-black">{t.ticket_id}</span><span className="text-[10px] bg-white/5 px-3 py-1 rounded-full text-gray-500 uppercase font-black">{t.category}</span></div>
                        <h3 className="font-bold text-2xl group-hover:text-white transition-colors">{t.summary}</h3>
                        <p className="text-xs text-gray-600 font-medium">{new Date(t.timestamp).toLocaleString()}</p>
                      </div>
                      <div className="text-right"><span className={`px-6 py-2 rounded-full text-xs font-black uppercase tracking-widest ${t.status === 'OPEN' ? 'bg-forensic-red/10 text-forensic-red' : 'bg-green-500/10 text-green-500'}`}>{t.status}</span></div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {view === 'about' && (
              <motion.div key="about" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} className="h-full flex items-center justify-center p-12">
                <div className="max-w-6xl w-full bg-gradient-to-br from-white/[0.04] to-transparent rounded-[4rem] border border-white/10 p-24 relative overflow-hidden backdrop-blur-3xl">
                  <div className="absolute -top-32 -right-32 p-12 opacity-5 text-forensic-green rotate-12"><Shield size={500} /></div>
                  <div className="flex items-center gap-8 mb-16"><div className="p-6 bg-forensic-green text-black rounded-[2.5rem] shadow-2xl"><Users size={40} /></div><div><h2 className="text-6xl font-black tracking-tighter italic uppercase">Infraglyph <span className="text-forensic-green">Team</span></h2><p className="text-gray-500 font-jetbrains mt-2 tracking-[0.3em]">UNIT 01 // FORENSIC INTELLIGENCE</p></div></div>
                  <p className="text-gray-300 text-3xl leading-snug mb-20 font-light max-w-4xl">We architect autonomous reasoning engines to bridge the chasm between <span className="text-white font-medium italic">massive telemetry</span> and <span className="text-forensic-green font-medium italic">actionable forensic truth</span>.</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-16">
                    {["Urvi Kava", "Harsh Patel", "Prisha Khalasi", "Aman Choudhary"].map((name, i) => (
                      <div key={i} className="group cursor-default text-center">
                        <div className="w-24 h-24 bg-white/[0.03] rounded-[3rem] mx-auto mb-8 border border-white/5 flex items-center justify-center font-black text-3xl group-hover:border-forensic-green group-hover:text-forensic-green transition-all duration-500 group-hover:scale-110 shadow-2xl">{name[0]}</div>
                        <p className="font-black text-xl mb-1">{name}</p><p className="text-[10px] text-gray-600 uppercase font-black tracking-widest">Infraglyph Unit</p>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <footer className="h-16 border-t border-white/10 flex items-center justify-between px-12 text-[10px] text-gray-700 uppercase tracking-[0.4em] font-black bg-chat-bg/80 backdrop-blur-3xl z-40">
          <div className="flex items-center gap-4"><Shield size={14} className="text-forensic-green" /><span>Forensic Intelligence Command // © 2026 Infraglyph</span></div>
          <div className="flex gap-12"><button className="hover:text-forensic-green transition-colors">Core Telemetry</button><button className="hover:text-forensic-green transition-colors">DLP Shards</button><button className="hover:text-forensic-green transition-colors">Enterprise Map</button></div>
        </footer>
      </main>
      <style>{`
        .forensic-graph-svg { display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; height: 100% !important; }
        .forensic-graph-svg svg { width: auto !important; height: auto !important; max-width: none !important; max-height: none !important; margin: 0 !important; filter: drop-shadow(0 0 30px rgba(0,255,65,0.2)); }
        .forensic-graph-svg .node rect, .forensic-graph-svg .node circle, .forensic-graph-svg .node polygon { fill: #0b0c0e !important; stroke: #00ff41 !important; stroke-width: 3.5px !important; }
        .forensic-graph-svg .label { color: #fff !important; font-family: 'JetBrains Mono', monospace !important; font-size: 16px !important; font-weight: 900 !important; }
        .forensic-graph-svg .edgePath path { stroke: #00ff41 !important; stroke-width: 3px !important; opacity: 0.8 !important; }
        .forensic-graph-svg .edgeLabel { color: #00ff41 !important; font-family: 'JetBrains Mono' !important; font-size: 12px !important; font-weight: bold !important; }
        .react-transform-component { cursor: grab !important; width: 100% !important; height: 100% !important; display: flex !important; align-items: center !important; justify-content: center !important; }
        .react-transform-component:active { cursor: grabbing !important; }
      `}</style>
    </div>
  );
};

export default App;
