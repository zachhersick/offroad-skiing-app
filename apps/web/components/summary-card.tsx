import { type ReactNode } from "react";

interface SummaryCardProps {
  eyebrow: string;
  title: string;
  children: ReactNode;
}

export function SummaryCard({ eyebrow, title, children }: SummaryCardProps) {
  return (
    <article className="rounded-[1.75rem] border border-ridge/10 bg-white p-5 shadow-terrain">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/50">{eyebrow}</p>
      <h3 className="mt-2 font-display text-2xl text-shale">{title}</h3>
      <div className="mt-4 text-sm text-ridge/80">{children}</div>
    </article>
  );
}

