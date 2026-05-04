import React from 'react';

const USE_CASES = [
    { id: "gaming_1080p", label: "1080P GAMING" },
    { id: "gaming_1440p", label: "1440P GAMING" },
    { id: "gaming_4k", label: "4K GAMING" },
    { id: "ml_compute", label: "COMPUTE/ML" },
    { id: "general", label: "GENERAL USE" }
];

export default function UseCaseSelector({ useCase, setUseCase }) {
  return (
    <div className="space-y-4">
        <label className="block text-[10px] text-on-surface-variant font-mono tracking-widest uppercase">WORKLOAD_PRIORITY</label>
        <div className="flex flex-col gap-2">
            {USE_CASES.map(uc => {
                const isActive = useCase === uc.id;
                return (
                    <button 
                        key={uc.id}
                        onClick={() => setUseCase(uc.id)}
                        className={`${isActive ? 'bg-primary text-on-primary opacity-100' : 'bg-surface-container-high text-on-surface opacity-50'} font-bold py-2 px-4 text-xs tracking-widest text-left flex justify-between items-center hover:opacity-100 transition-opacity`}
                    >
                        {uc.label} <span className="material-symbols-outlined text-sm">{isActive ? 'check_box' : 'square'}</span>
                    </button>
                )
            })}
        </div>
    </div>
  );
}
