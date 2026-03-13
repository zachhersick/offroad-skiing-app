import type { ArtifactRecord } from "@/lib/types";

export function ArtifactList({ artifacts }: { artifacts: ArtifactRecord[] }) {
  return (
    <div className="grid gap-4">
      {artifacts.map((artifact) => (
        <article key={artifact.id} className="rounded-[1.5rem] border border-ridge/10 bg-white p-5 shadow-terrain">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-2xl text-shale">{artifact.artifact_type}</h3>
            <span className="rounded-full bg-ridge/10 px-3 py-1 text-xs uppercase tracking-[0.2em] text-ridge">
              artifact
            </span>
          </div>
          <pre className="mt-4 overflow-auto rounded-2xl bg-shale p-4 text-xs text-frost">
            {JSON.stringify(artifact.payload, null, 2)}
          </pre>
        </article>
      ))}
    </div>
  );
}

