import { dashboardSnapshot } from "@/lib/mock-data";
import { SummaryCard } from "@/components/summary-card";

export default function SetupPage() {
  const snapshot = dashboardSnapshot;
  return (
    <main className="mx-auto max-w-7xl px-6 py-10 lg:px-10">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Setup Manager</p>
        <h1 className="mt-3 font-display text-5xl text-shale">Garage, quiver, and gear fit</h1>
      </div>
      <section className="mt-8 grid gap-5 lg:grid-cols-2">
        <SummaryCard eyebrow="Vehicle" title={snapshot.vehicles[0].name}>
          <p>{snapshot.vehicles[0].drivetrain.toUpperCase()} · {snapshot.vehicles[0].tire_size_inches}&quot; tires</p>
        </SummaryCard>
        <SummaryCard eyebrow="Ski Quiver" title={snapshot.ski_quivers[0].name}>
          <ul className="space-y-2">
            {snapshot.ski_quivers[0].skis.map((ski) => (
              <li key={ski.name}>
                {ski.name} · {ski.waist_mm}mm
              </li>
            ))}
          </ul>
        </SummaryCard>
      </section>
    </main>
  );
}

