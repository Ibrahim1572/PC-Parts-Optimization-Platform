import React from 'react';

export default function BudgetForm({ budget, setBudget }) {
  return (
    <div className="space-y-4">
        <label className="block text-[10px] text-on-surface-variant font-mono tracking-widest uppercase">TARGET_BUDGET</label>
        <div className="flex items-baseline gap-2">
            <span className="text-4xl font-bold text-primary font-mono">$</span>
            <span className="text-6xl font-black text-primary font-mono tracking-tighter">{budget}</span>
        </div>
        <input 
            className="w-full mt-4" 
            max="5000" min="500" step="50" 
            type="range" 
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
        />
        <div className="flex justify-between text-[10px] font-mono text-outline">
            <span>MIN: $500</span>
            <span>MAX: $5000</span>
        </div>
    </div>
  );
}
