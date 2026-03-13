import Link from "next/link";

import { fetchDashboard } from "@/lib/api";

export default async function HistoryPage() {
  const snapshot = await fetchDashboard();
  return (
    <main className="mx-auto max-w-6xl px-6 py-10 lg:px-10">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Task History</p>
      <h1 className="mt-3 font-display text-5xl text-shale">Agent runs and step logs</h1>
      <div className="mt-8 grid gap-4">
        {snapshot.runs.map((run) => (
          <Link key={run.id} href={`/runs/${run.id}`} className="rounded-[1.75rem] border border-ridge/10 bg-white p-6 shadow-terrain">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-2xl text-shale">{run.title}</h2>
              <span className="rounded-full bg-ridge/10 px-3 py-1 text-xs uppercase tracking-[0.2em] text-ridge">
                {run.status}
              </span>
            </div>
            <p className="mt-3 text-sm text-ridge/75">
              {run.mode} · created {new Date(run.createdAt).toLocaleString()}
            </p>
          </Link>
        ))}
      </div>
    </main>
  );
}

