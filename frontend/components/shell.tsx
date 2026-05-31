import Link from "next/link";
import { AutoRefresh } from "@/components/auto-refresh";
import { Bell, Brain, ChartCandlestick, Gauge, Globe2, Home, ListChecks, Search, Settings, ShieldCheck, Siren } from "lucide-react";

const nav = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/global", label: "Global Markets", icon: Globe2 },
  { href: "/india", label: "Indian Markets", icon: ChartCandlestick },
  { href: "/news", label: "News Intelligence", icon: Gauge },
  { href: "/insights", label: "AI Insights", icon: Brain },
  { href: "/watchlist", label: "Watchlist", icon: ListChecks },
  { href: "/alerts", label: "Alerts", icon: Siren },
  { href: "/admin", label: "Admin", icon: ShieldCheck },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function AppShell({ children, marketStatus = "Pre-open" }: { children: React.ReactNode; marketStatus?: string }) {
  return (
    <div className="min-h-screen bg-canvas text-ink">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 border-r border-line bg-panel lg:block">
        <div className="flex h-16 items-center border-b border-line px-5">
          <div>
            <div className="text-lg font-semibold">TradePulse AI</div>
            <div className="text-xs text-muted">Institutional market brain</div>
          </div>
        </div>
        <nav className="space-y-1 p-3">
          {nav.map((item) => (
            <Link key={item.href} href={item.href} className="flex h-10 items-center gap-3 rounded-md px-3 text-sm text-muted transition hover:bg-panel2 hover:text-ink">
              <item.icon size={17} />
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 items-center gap-3 border-b border-line bg-canvas/92 px-4 backdrop-blur md:px-6">
          <div className="flex h-10 min-w-0 flex-1 items-center gap-2 rounded-md border border-line bg-panel px-3">
            <Search size={17} className="text-muted" />
            <input className="w-full bg-transparent text-sm outline-none placeholder:text-muted" placeholder="Search indices, events, news, alerts" />
          </div>
          <div className="hidden rounded-md border border-line bg-panel px-3 py-2 text-sm md:block">
            <span className="text-muted">Market:</span> <span className="font-medium text-buy">{marketStatus}</span>
          </div>
          <AutoRefresh />
          <button className="grid h-10 w-10 place-items-center rounded-md border border-line bg-panel" aria-label="Notifications">
            <Bell size={17} />
          </button>
          <div className="grid h-10 w-10 place-items-center rounded-md bg-info text-sm font-bold text-white">TP</div>
        </header>
        <main className="p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
