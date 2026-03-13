import { fetchApprovals } from "@/lib/api";

export default async function ApprovalsPage() {
  const approvals = await fetchApprovals();
  return (
    <main className="mx-auto max-w-5xl px-6 py-10 lg:px-10">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Approval Queue</p>
      <h1 className="mt-3 font-display text-5xl text-shale">Human approval before risky actions</h1>
      <div className="mt-8 grid gap-4">
        {approvals.map((approval: (typeof approvals)[number]) => (
          <article key={approval.id} className="rounded-[1.75rem] border border-ridge/10 bg-white p-6 shadow-terrain">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-display text-2xl text-shale">{approval.action}</h2>
                <p className="mt-1 text-sm text-ridge/60">{approval.title}</p>
              </div>
              <span className="rounded-full bg-canyon/10 px-3 py-1 text-xs uppercase tracking-[0.2em] text-canyon">
                {approval.status}
              </span>
            </div>
            <p className="mt-3 text-sm text-ridge/75">{approval.reason}</p>
            <div className="mt-5 flex gap-3">
              <button className="rounded-full bg-ridge px-5 py-2 text-sm font-semibold text-white">Approve in run view</button>
            </div>
          </article>
        ))}
      </div>
    </main>
  );
}
