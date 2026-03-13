import Link from "next/link";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/planner", label: "Planner" },
  { href: "/setup", label: "Setup" },
  { href: "/trips", label: "Trips" },
  { href: "/history", label: "History" },
  { href: "/checklists", label: "Checklists" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/approvals", label: "Approvals" },
  { href: "/auth", label: "Auth" }
];

export function TopNav() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-shale/85 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4 lg:px-10">
        <Link href="/" className="font-display text-2xl text-white">
          TerrainPilot
        </Link>
        <nav className="hidden flex-wrap gap-4 text-sm text-frost/80 md:flex">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="transition hover:text-white">
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}

