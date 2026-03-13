import Link from "next/link";

const productPillars = [
  {
    title: "Planner Agent",
    body: "Breaks goals into ordered, reviewable steps for off-road and ski planning."
  },
  {
    title: "Execution Workspace",
    body: "Tracks recommendations, checklists, artifacts, and approval-gated side effects."
  },
  {
    title: "Setup Intelligence",
    body: "Scores trips against the user profile, vehicle capability, or ski quiver fit."
  }
];

export default function HomePage() {
  return (
    <main className="mx-auto min-h-screen max-w-7xl px-6 py-10 lg:px-10">
      <section className="rounded-[2.5rem] border border-white/10 bg-shale/75 px-8 py-10 text-white shadow-terrain backdrop-blur lg:px-12 lg:py-14">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.4em] text-frost/70">TerrainPilot</p>
          <h1 className="mt-4 font-display text-5xl leading-tight lg:text-7xl">
            Plan rugged trips and ski days with bounded autonomous agents.
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-frost/80">
            TerrainPilot combines setup tracking, trail and resort context, packing workflows, and audited agent runs
            into one real planning workspace.
          </p>
        </div>
        <div className="mt-10 flex flex-wrap gap-4">
          <Link className="rounded-full bg-canyon px-6 py-3 text-sm font-semibold text-white" href="/dashboard">
            Open workspace
          </Link>
          <Link className="rounded-full border border-white/20 px-6 py-3 text-sm font-semibold text-white" href="/planner">
            Explore the planner
          </Link>
        </div>
      </section>

      <section className="mt-10 grid gap-5 lg:grid-cols-3">
        {productPillars.map((pillar) => (
          <article key={pillar.title} className="rounded-[1.75rem] border border-ridge/10 bg-white p-6 shadow-terrain">
            <h2 className="font-display text-3xl text-shale">{pillar.title}</h2>
            <p className="mt-4 text-sm leading-6 text-ridge/75">{pillar.body}</p>
          </article>
        ))}
      </section>
    </main>
  );
}

