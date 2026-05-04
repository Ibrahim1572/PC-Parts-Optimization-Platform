import React from 'react';

export default function BudgetSplitSlider({ split, setSplit }) {
  return (
    <div className="space-y-4">
        <label className="block text-[10px] text-on-surface-variant font-mono tracking-widest uppercase">HARDWARE_BIAS_RATIO</label>
        <div className="flex justify-between text-[10px] font-mono text-outline mb-2">
            <span>GPU ({split}%)</span>
            <span>CPU ({100 - split}%)</span>
        </div>
        <div className="h-8 w-full bg-surface-container-lowest flex">
            <div className="h-full bg-primary" style={{ width: `${split}%` }}></div>
            <div className="h-full bg-surface-container-highest" style={{ width: `${100 - split}%` }}></div>
        </div>
        <input 
            className="w-full" 
            max="100" min="0" 
            type="range" 
            value={split}
            onChange={(e) => setSplit(Number(e.target.value))}
        />
        <p className="text-[10px] text-outline font-mono italic leading-relaxed uppercase">
            // {split > 60 ? 'BIASING TOWARD GPU FOR GRAPHICS PERFORMANCE.' : split < 40 ? 'BIASING TOWARD CPU FOR COMPUTE HEAVY TASKS.' : 'BALANCED ALLOCATION FOR HYBRID WORKLOADS.'}
        </p>
    </div>
  );
}
