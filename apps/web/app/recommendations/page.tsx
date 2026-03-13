const recommendationCards = [
  {
    title: "Otay Backbone",
    score: "92.4",
    body: "Best off-road fit for a mostly stock truck seeking a conservative half-day trail."
  },
  {
    title: "Storm Board 112",
    score: "86.8",
    body: "Top ski pick for a Mammoth storm day based on quiver width and terrain bias."
  }
];

export default function RecommendationsPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-10 lg:px-10">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Recommendation Results</p>
      <h1 className="mt-3 font-display text-5xl text-shale">Ranked options with rationale</h1>
      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {recommendationCards.map((card) => (
          <article key={card.title} className="rounded-[1.75rem] border border-ridge/10 bg-white p-6 shadow-terrain">
            <p className="text-xs uppercase tracking-[0.2em] text-ridge/50">Score {card.score}</p>
            <h2 className="mt-2 font-display text-2xl text-shale">{card.title}</h2>
            <p className="mt-4 text-sm text-ridge/80">{card.body}</p>
          </article>
        ))}
      </div>
    </main>
  );
}
