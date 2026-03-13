import { ArtifactList } from "@/components/artifact-list";
import { fetchArtifacts } from "@/lib/api";

export default async function RunDetailPage({ params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;
  const artifacts = await fetchArtifacts(runId);
  return (
    <main className="mx-auto max-w-6xl px-6 py-10 lg:px-10">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Run Detail</p>
      <h1 className="mt-3 font-display text-5xl text-shale">Artifacts for {runId}</h1>
      <div className="mt-8">
        <ArtifactList artifacts={artifacts} />
      </div>
    </main>
  );
}

