import { MetricCard, Panel, SentimentGauge } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function IndiaPage() {
  const data = await api.indian();
  return (
    <AppShell marketStatus={data.market_status}>
      <h1 className="mb-1 text-2xl font-semibold">Indian Market Analysis</h1>
      <p className="mb-6 text-sm text-muted">NIFTY, gap bias, FII/DII activity, options positioning, and expected move.</p>
      <div className="grid gap-4 lg:grid-cols-3">
        {data.indian_markets.map((item) => <MetricCard key={item.symbol} item={item} />)}
      </div>
      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <Panel title="Open Interest Analysis">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <Stat label="Highest Call OI" value={data.oi.highest_call_oi.toLocaleString("en-IN")} />
            <Stat label="Highest Put OI" value={data.oi.highest_put_oi.toLocaleString("en-IN")} />
            <Stat label="PCR Ratio" value={data.oi.pcr_ratio.toFixed(2)} />
            <Stat label="Max Pain" value={data.oi.max_pain.toLocaleString("en-IN")} />
          </div>
          <p className="mt-4 rounded-lg border border-line bg-panel2 p-3 text-sm leading-6 text-muted">{data.oi.interpretation}</p>
        </Panel>
        <Panel title="India VIX Expected Move">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <Stat label="VIX" value={data.vix.current.toFixed(2)} />
            <Stat label="Move" value={data.vix.expected_move.toFixed(0)} />
            <Stat label="Expected High" value={data.vix.expected_high.toFixed(0)} />
            <Stat label="Expected Low" value={data.vix.expected_low.toFixed(0)} />
          </div>
          <p className="mt-4 text-xs leading-5 text-muted">Expected Move = (Index Price x VIX) / (100 x sqrt(365))</p>
        </Panel>
        <Panel title="India Sentiment">
          <SentimentGauge score={data.sentiment.score} label={data.sentiment.label} />
        </Panel>
      </div>
    </AppShell>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-panel2 p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 text-lg font-semibold">{value}</div>
    </div>
  );
}
