import React from 'react';

export default function ComboResultCard({ rank, id, gpu, vram, tdp, gpuScore, cpu, cores, socket, cpuStability, log, isRank1 }) {
  return (
    <div className={`bg-surface-container border ${isRank1 ? 'border-primary-container glow-rank-1' : 'border-outline-variant'} relative flex flex-col`}>
        <div className={`absolute top-0 left-0 ${isRank1 ? 'bg-primary-container text-on-primary-container' : 'bg-surface-container-high text-on-surface'} px-3 py-1 font-bold text-[10px] tracking-widest uppercase`}>
            RANK_{rank}
        </div>
        <div className="absolute top-0 right-0 p-3 text-[10px] text-outline font-mono">ID: {id}</div>
        
        <div className="p-6 pt-12 flex-1">
            <div className="mb-8 border-b border-outline-variant/20 pb-6">
                <span className={`text-[8px] ${isRank1 ? 'text-primary' : 'text-on-surface-variant'} tracking-widest font-bold uppercase mb-2 block`}>GPU_MODULE</span>
                <h3 className="text-xl font-black mb-4">{gpu}</h3>
                <div className="flex flex-wrap gap-2 mb-4">
                    <span className={`text-[9px] border ${isRank1 ? 'border-primary text-primary' : 'border-outline-variant text-outline'} px-2 py-0.5 font-mono`}>{vram}</span>
                    <span className="text-[9px] border border-outline-variant text-outline px-2 py-0.5 font-mono">{tdp}</span>
                </div>
                <div className="space-y-1">
                    <div className="flex justify-between text-[8px] font-mono uppercase text-on-surface-variant"><span>PERF_SCORE</span><span>{gpuScore}</span></div>
                    <div className="h-1 w-full bg-surface-container-highest"><div className={`h-full ${isRank1 ? 'bg-primary' : 'bg-primary/60'}`} style={{ width: `${gpuScore}%` }}></div></div>
                </div>
            </div>

            <div>
                <span className={`text-[8px] ${isRank1 ? 'text-primary' : 'text-on-surface-variant'} tracking-widest font-bold uppercase mb-2 block`}>CPU_CORE</span>
                <h3 className="text-xl font-black mb-4">{cpu}</h3>
                <div className="flex flex-wrap gap-2 mb-4">
                    <span className={`text-[9px] border ${isRank1 ? 'border-primary text-primary' : 'border-outline-variant text-outline'} px-2 py-0.5 font-mono`}>{cores}</span>
                    <span className="text-[9px] border border-outline-variant text-outline px-2 py-0.5 font-mono">{socket}</span>
                </div>
                <div className="space-y-1">
                    <div className="flex justify-between text-[8px] font-mono uppercase text-on-surface-variant"><span>STABILITY</span><span>{cpuStability}</span></div>
                    <div className="h-1 w-full bg-surface-container-highest"><div className={`h-full ${isRank1 ? 'bg-primary' : 'bg-primary/60'}`} style={{ width: `${cpuStability}%` }}></div></div>
                </div>
            </div>
        </div>

        <div className="bg-surface-container-low p-4 mt-auto">
            <span className="text-[8px] text-outline font-mono uppercase block mb-1">OPTIMIZATION_LOG:</span>
            <p className={`text-[10px] ${isRank1 ? 'text-primary-fixed' : 'text-on-surface-variant'} leading-tight font-mono uppercase`}>
                {log}
            </p>
        </div>
    </div>
  );
}
