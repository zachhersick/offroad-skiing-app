"use client";

import { modeLabels, type Mode } from "@terrainpilot/shared";

interface ModeSwitchProps {
  mode: Mode;
  onChange: (mode: Mode) => void;
}

export function ModeSwitch({ mode, onChange }: ModeSwitchProps) {
  return (
    <div className="inline-flex rounded-full border border-white/20 bg-white/10 p-1 backdrop-blur">
      {(["offroad", "ski"] as const).map((option) => (
        <button
          key={option}
          type="button"
          onClick={() => onChange(option)}
          className={`rounded-full px-4 py-2 text-sm transition ${
            option === mode ? "bg-sand text-shale" : "text-white/75 hover:text-white"
          }`}
        >
          {modeLabels[option]}
        </button>
      ))}
    </div>
  );
}

