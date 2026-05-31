import { Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

export const dynamic = "force-dynamic";

export default async function NewsPage() {
  const [{ news }, { events }] = await Promise.all([api.news(), api.events()]);
  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">News Intelligence Center</h1>
      <p className="mb-6 text-sm text-muted">Filtered high-impact monetary policy, macro, geopolitical, commodity, budget, election, and manufacturing news.</p>
      <div className="grid gap-4 xl:grid-cols-[1.25fr_0.75fr]">
        <Panel title="High Impact Feed">
          <div className="space-y-3">
            {news.map((item) => (
              <article key={item.id} className="rounded-lg border border-line bg-panel2 p-4">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-md border border-line px-2 py-1 text-xs text-muted">{item.category}</span>
                  <span className={cn("rounded-md px-2 py-1 text-xs font-semibold", item.sentiment === "Bullish" ? "bg-buy/10 text-buy" : item.sentiment === "Bearish" ? "bg-sell/10 text-sell" : "bg-warn/10 text-warn")}>{item.sentiment}</span>
                  <span className="rounded-md bg-info/10 px-2 py-1 text-xs text-info">Impact {item.impact_score}/10</span>
                  <span className="text-xs text-muted">{item.source}</span>
                </div>
                <h2 className="mt-3 text-lg font-semibold">{item.headline}</h2>
                <p className="mt-2 text-sm leading-6 text-muted">{item.summary}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {item.affected_markets.map((market) => <span key={market} className="rounded-md bg-canvas px-2 py-1 text-xs text-muted">{market}</span>)}
                </div>
              </article>
            ))}
          </div>
        </Panel>
        <Panel title="Macro Calendar">
          <div className="space-y-3">
            {events.map((event) => (
              <article key={event.id} className="rounded-lg border border-line bg-panel2 p-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="rounded-md border border-line px-2 py-1 text-xs text-muted">{event.country}</span>
                  <span className="rounded-md bg-info/10 px-2 py-1 text-xs text-info">Impact {event.importance}/10</span>
                </div>
                <h2 className="mt-3 text-sm font-semibold">{event.event_name}</h2>
                <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-muted">
                  <span>Forecast {event.forecast}</span>
                  <span>Previous {event.previous}</span>
                </div>
                <div className="mt-3 text-xs text-muted">{new Date(event.event_time).toLocaleString()}</div>
              </article>
            ))}
          </div>
        </Panel>
      </div>
    </AppShell>
  );
}
