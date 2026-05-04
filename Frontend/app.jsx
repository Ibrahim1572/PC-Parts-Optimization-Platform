import React, { useState } from 'react';
import BudgetForm from './components/BudgetForm';
import UseCaseSelector from './components/UseCaseSelector';
import BudgetSplitSlider from './components/BudgetSplitSlider';
import ComboResultCard from './components/ComboResultCard';

export default function App() {
  const [budget, setBudget] = useState(2450);
  const [useCase, setUseCase] = useState("gaming_1080p");
  const [split, setSplit] = useState(65);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleOptimize = async () => {
    setLoading(true);
    setError(null);
    try {
        const res = await fetch(`http://localhost:8000/recommend?budget_usd=${budget}&use_case=${useCase}&gpu_budget_split=${split / 100}`);
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Failed to fetch data");
        }
        const data = await res.json();
        setResults(data.results);
    } catch (err) {
        setError(err.message);
    } finally {
        setLoading(false);
    }
  };

  return (
    <>
      <nav className="fixed top-0 w-full z-50 flex justify-between items-center px-6 py-3 bg-slate-950/80 backdrop-blur-xl border-b-0">
        <div className="flex items-center gap-8">
            <div className="flex flex-col">
                <span className="text-xl font-black text-blue-400 tracking-widest font-mono uppercase">PC BUILD OPTIMIZER</span>
                <span className="text-[10px] text-slate-500 font-mono tracking-[0.2em] mt-[-4px]">v1.4 // SYSTEM OPTIMIZATION ENGINE</span>
            </div>
            <div className="hidden md:flex gap-6">
                <a className="font-mono uppercase tracking-tighter text-sm text-blue-400 border-b-2 border-blue-400 pb-1 hover:text-blue-300 transition-colors duration-150" href="#">COMPONENTS</a>
                <a className="font-mono uppercase tracking-tighter text-sm text-slate-500 hover:text-blue-300 transition-colors duration-150" href="#">BUILDS</a>
                <a className="font-mono uppercase tracking-tighter text-sm text-slate-500 hover:text-blue-300 transition-colors duration-150" href="#">BENCHMARKS</a>
            </div>
        </div>
        <div className="flex items-center gap-4">
            <span className="material-symbols-outlined text-blue-400 cursor-pointer scale-95 active:duration-75">settings</span>
            <span className="material-symbols-outlined text-blue-400 cursor-pointer scale-95 active:duration-75">terminal</span>
        </div>
      </nav>

      <aside className="fixed left-0 top-0 h-full flex flex-col pt-16 bg-slate-950 w-20 border-r-0 z-40 hidden md:flex">
        <div className="flex flex-col items-center py-6 gap-8">
            <div className="flex flex-col items-center group cursor-pointer text-blue-400 bg-blue-400/10 border-r-2 border-blue-400 w-full py-3">
                <span className="material-symbols-outlined mb-1">dashboard</span>
                <span className="font-mono text-[8px] uppercase">DASHBOARD</span>
            </div>
            <div className="flex flex-col items-center group cursor-pointer text-slate-600 hover:bg-slate-900 hover:text-slate-300 w-full py-3">
                <span className="material-symbols-outlined mb-1">memory</span>
                <span className="font-mono text-[8px] uppercase">HARDWARE</span>
            </div>
            <div className="flex flex-col items-center group cursor-pointer text-slate-600 hover:bg-slate-900 hover:text-slate-300 w-full py-3">
                <span className="material-symbols-outlined mb-1">analytics</span>
                <span className="font-mono text-[8px] uppercase">TELEMETRY</span>
            </div>
        </div>
      </aside>

      <main className="md:pl-20 pt-20 px-6 pb-12 max-w-7xl mx-auto">
        <section className="mt-8 mb-12 bg-surface-container-low p-8 border-l-4 border-primary">
            <div className="flex justify-between items-start mb-10">
                <div>
                    <h2 className="text-on-surface-variant font-mono text-xs mb-1 tracking-widest uppercase">CONFIGURATION_PARAMETERS</h2>
                    <p className="text-primary font-bold text-lg tracking-tight">ENGINE OVERRIDE ACTIVE</p>
                </div>
                <div className="text-right">
                    <span className="text-[10px] text-outline font-mono uppercase tracking-widest">COORD_REF: 001-ALPHA</span>
                </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                <BudgetForm budget={budget} setBudget={setBudget} />
                <UseCaseSelector useCase={useCase} setUseCase={setUseCase} />
                <BudgetSplitSlider split={split} setSplit={setSplit} />
            </div>

            <div className="mt-12 flex justify-center">
                <button 
                  onClick={handleOptimize}
                  disabled={loading}
                  className={`${loading ? 'opacity-50' : ''} bg-primary-container text-on-primary-container font-black py-5 px-16 text-sm tracking-[0.3em] uppercase hover:bg-primary transition-all active:scale-95 shadow-[0_0_20px_rgba(39,146,255,0.3)]`}>
                    {loading ? "PROCESSING..." : "OPTIMIZE BUILD"}
                </button>
            </div>
        </section>

        {error && (
            <div className="bg-error-container text-on-error-container p-4 mb-8 border border-error">
                <p className="font-mono text-sm tracking-widest">ERROR: {error}</p>
            </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {!results && !loading && !error && (
                <div className="col-span-3 text-center text-outline font-mono text-sm uppercase p-8 border border-outline-variant/20 border-dashed">
                    AWAITING PARAMETERS... CLICK OPTIMIZE TO GENERATE COMBO BUILDS.
                </div>
            )}
            
            {results && results.map((res, idx) => (
                <ComboResultCard 
                    key={res.gpu.id + "-" + res.cpu.id}
                    rank={`0${idx + 1}`} 
                    id={`X-${res.cpu.id}${res.gpu.id}`.substring(0, 5)} 
                    gpu={res.gpu.product_name} 
                    vram={res.gpu.mem_size_mb ? `${Math.round(res.gpu.mem_size_mb/1024)}GB VRAM` : "N/A VRAM"} 
                    tdp={res.cpu.tdp_watts ? `~${res.cpu.tdp_watts}W SYSTEM` : "N/A TDP"} 
                    gpuScore={Math.round(res.combo_score * 10) / 10} 
                    cpu={res.cpu.cpu_name} 
                    cores={res.cpu.cores ? `${res.cpu.cores} CORES` : "N/A CORES"} 
                    socket={res.cpu.socket || "N/A"} 
                    cpuStability={res.cpu.cpu_mark ? Math.min((res.cpu.cpu_mark / 40000) * 100, 100).toFixed(1) : "80.0"} 
                    log={res.reason} 
                    isRank1={idx === 0} 
                />
            ))}
        </div>
      </main>
    </>
  );
}
