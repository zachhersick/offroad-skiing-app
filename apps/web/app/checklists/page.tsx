const checklistGroups = [
  {
    title: "Off-road trip checklist",
    items: ["Offline map", "Recovery strap", "First aid kit", "Tire repair kit"]
  },
  {
    title: "Ski storm-day checklist",
    items: ["Helmet and goggles", "Dry layers", "Wax kit", "Avalanche app or notes"]
  }
];

export default function ChecklistsPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-10 lg:px-10">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Packing Lists</p>
      <h1 className="mt-3 font-display text-5xl text-shale">Editable checklist workspace</h1>
      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {checklistGroups.map((group) => (
          <article key={group.title} className="rounded-[1.75rem] border border-ridge/10 bg-white p-6 shadow-terrain">
            <h2 className="font-display text-2xl text-shale">{group.title}</h2>
            <ul className="mt-4 space-y-3 text-sm text-ridge/80">
              {group.items.map((item) => (
                <li key={item} className="flex items-center gap-3">
                  <input type="checkbox" className="size-4" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </main>
  );
}

