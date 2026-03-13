import { fetchTrips } from "@/lib/api";

export default async function TripsPage() {
  const trips = await fetchTrips();
  return (
    <main className="mx-auto max-w-6xl px-6 py-10 lg:px-10">
      <p className="text-xs uppercase tracking-[0.3em] text-ridge/60">Trips</p>
      <h1 className="mt-3 font-display text-5xl text-shale">Saved plans and field notes</h1>
      <div className="mt-8 grid gap-4">
        {trips.map((trip: (typeof trips)[number]) => (
          <article key={trip.id} className="rounded-[1.75rem] border border-ridge/10 bg-white p-6 shadow-terrain">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-display text-2xl text-shale">{trip.title}</h2>
                <p className="mt-2 text-sm text-ridge/75">
                  {trip.region} · {trip.mode} · {trip.status}
                </p>
              </div>
            </div>
            <p className="mt-4 text-sm text-ridge/80">{trip.objective}</p>
          </article>
        ))}
      </div>
    </main>
  );
}

