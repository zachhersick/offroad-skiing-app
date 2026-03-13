import type { Route } from "next";
import Link from "next/link";

import { SummaryCard } from "@/components/summary-card";
import { fetchDashboard } from "@/lib/api";

const workspaceLinks = [
  { href: "/planner", label: "Trip Planner", desc: "Structured request intake and agent runs." },
  { href: "/setup", label: "Garage + Quiver", desc: "Vehicles, skis, and gear inventory." },
  { href: "/approvals", label: "Approval Queue", desc: "Review live-condition and shell requests." },
  { href: "/runs/run_seed", label: "Artifact Viewer", desc: "Inspect plan, checklist, and review JSON." }
] as const;

export default async function DashboardPage() {
  const snapshot = await fetchDashboard();
  return (
    <main className="mx-auto max-w-7xl px-6 py-10 lg:px-10">
      <div className="flex items-end justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-ridge/60">Workspace</p>
          <h1 className="mt-3 font-display text-5xl text-shale">Mission control for TerrainPilot</h1>
        </div>
        <Link href="/planner" className="rounded-full bg-ridge px-5 py-3 text-sm font-semibold text-white">
          New run
        </Link>
      </div>

      <section className="mt-8 grid gap-5 lg:grid-cols-3">
        <SummaryCard eyebrow="Profile" title={snapshot.profile.display_name}>
          <p>{snapshot.profile.home_region}</p>
          <p className="mt-2">Comfort rating: {snapshot.profile.comfort_rating} / 5</p>
        </SummaryCard>
        <SummaryCard eyebrow="Garage" title={`${snapshot.vehicles.length} vehicle${snapshot.vehicles.length === 1 ? "" : "s"}`}>
          <ul className="space-y-2">
            {snapshot.vehicles.map((vehicle) => (
              <li key={vehicle.id}>{vehicle.name}</li>
            ))}
          </ul>
        </SummaryCard>
        <SummaryCard eyebrow="Runs" title={`${snapshot.runs.length} recent agent runs`}>
          <ul className="space-y-2">
            {snapshot.runs.map((run) => (
              <li key={run.id}>
                <span className="font-medium">{run.title}</span> · {run.status}
              </li>
            ))}
          </ul>
        </SummaryCard>
      </section>

      <section className="mt-10 grid gap-5 lg:grid-cols-4">
        {workspaceLinks.map((item) => (
          <Link key={item.href} href={item.href as Route} className="rounded-[1.75rem] border border-ridge/10 bg-white p-5 shadow-terrain">
            <p className="text-xs uppercase tracking-[0.25em] text-ridge/50">Surface</p>
            <h2 className="mt-2 font-display text-2xl text-shale">{item.label}</h2>
            <p className="mt-3 text-sm text-ridge/75">{item.desc}</p>
          </Link>
        ))}
      </section>
    </main>
  );
}
