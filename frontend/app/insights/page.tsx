import { Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function InsightsPage() {
  const insights = await api.insights();
  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">AI Market Brain</h1>
      <p className="mb-6 text-sm text-muted">Generated pre-market, hourly intraday, and end-of-day summaries with factor attribution.</p>
      <div className="grid gap-4 xl:grid-cols-3">
        <Panel title="Daily Pre-Market Summary"><p className="text-sm leading-6 text-muted">{insights.pre_market}</p></Panel>
        <Panel title="Intraday Summary"><p className="text-sm leading-6 text-muted">{insights.intraday}</p></Panel>
        <Panel title="End Of Day Summary"><p className="text-sm leading-6 text-muted">{insights.end_of_day}</p></Panel>
      </div>
      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <List title="Bullish Factors" items={insights.bullish_factors} />
        <List title="Bearish Factors" items={insights.bearish_factors} />
        <List title="Risks" items={insights.risks} />
      </div>
    </AppShell>
  );
}

function List({ title, items }: { title: string; items: string[] }) {
  return <Panel title={title}><div className="space-y-2 text-sm text-muted">{items.map((item) => <div key={item}>{item}</div>)}</div></Panel>;
}
