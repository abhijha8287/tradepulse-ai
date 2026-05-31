import { AppShell } from "@/components/shell";
import { MetricCard, Panel, SentimentGauge } from "@/components/cards";
import { ExpectedMoveChart, FlowBarChart } from "@/components/dashboard-charts";
import { api } from "@/lib/api";
import { Activity, AlertTriangle, Brain, Landmark } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const data = await api.dashboard();
  return (
    <AppShell marketStatus={data.market_status}>
      <div className="mb-6 flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Command Dashboard</h1>
          <p className="text-sm text-muted">Pre-market and intraday signal stack updated {new Date(data.generated_at).toLocaleString()}.</p>
        </div>
        <div className="rounded-md border border-line bg-panel px-3 py-2 text-sm text-muted">Target read time: under 5 minutes</div>
      </div>

      <div className="grid gap-4 xl:grid-cols-4">
        {data.global_markets.slice(0, 4).map((item) => <MetricCard item={item} key={item.symbol} />)}
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-[1.35fr_0.8fr]">
        <Panel title="AI Pre-Market Brief">
          <div className="flex gap-3">
            <Brain className="mt-1 shrink-0 text-info" size={22} />
            <p className="text-sm leading-6 text-ink">{data.ai_summary.pre_market}</p>
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-3">
            <SignalList title="Bullish" values={data.ai_summary.bullish_factors} tone="buy" />
            <SignalList title="Bearish" values={data.ai_summary.bearish_factors} tone="sell" />
            <SignalList title="Risks" values={data.ai_summary.risks} tone="warn" />
          </div>
        </Panel>
        <Panel title="Market Sentiment">
          <SentimentGauge score={data.sentiment.score} label={data.sentiment.label} />
          <div className="mt-4 space-y-2 text-sm text-muted">
            {data.sentiment.drivers.map((driver) => <div key={driver}>- {driver}</div>)}
          </div>
        </Panel>
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <Panel title="Institutional Flows">
          <div className="mb-4 grid grid-cols-2 gap-3">
            <Flow title="FII" value={data.flows.fii} />
            <Flow title="DII" value={data.flows.dii} />
          </div>
          <div className="h-56">
            <FlowBarChart data={data.flows.series as { date: string; fii: number; dii: number }[]} />
          </div>
        </Panel>
        <Panel title="VIX Expected Move">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <Flow title="India VIX" value={data.vix.current} plain />
            <Flow title="Move" value={data.vix.expected_move} plain />
            <Flow title="Expected High" value={data.vix.expected_high} plain />
            <Flow title="Expected Low" value={data.vix.expected_low} plain />
          </div>
          <div className="mt-5 h-28">
            <ExpectedMoveChart low={data.vix.expected_low} spot={data.vix.index_price} high={data.vix.expected_high} />
          </div>
        </Panel>
        <Panel title="High Impact News">
          <div className="space-y-3">
            {data.news.slice(0, 4).map((news) => (
              <div key={news.id} className="border-b border-line pb-3 last:border-0 last:pb-0">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-medium">{news.headline}</div>
                  <span className="rounded-md bg-info/10 px-2 py-1 text-xs text-info">{news.impact_score}/10</span>
                </div>
                <p className="mt-1 text-xs leading-5 text-muted">{news.summary}</p>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </AppShell>
  );
}

function SignalList({ title, values, tone }: { title: string; values: string[]; tone: "buy" | "sell" | "warn" }) {
  const icon = tone === "warn" ? <AlertTriangle size={16} /> : tone === "buy" ? <Activity size={16} /> : <Landmark size={16} />;
  const color = tone === "buy" ? "text-buy" : tone === "sell" ? "text-sell" : "text-warn";
  return (
    <div className="rounded-lg border border-line bg-panel2 p-3">
      <div className={`mb-2 flex items-center gap-2 text-sm font-semibold ${color}`}>{icon}{title}</div>
      <div className="space-y-2 text-xs leading-5 text-muted">{values.map((value) => <div key={value}>{value}</div>)}</div>
    </div>
  );
}

function Flow({ title, value, plain = false }: { title: string; value: number; plain?: boolean }) {
  const positive = value >= 0;
  return (
    <div className="rounded-lg border border-line bg-panel2 p-3">
      <div className="text-xs text-muted">{title}</div>
      <div className={plain ? "mt-1 text-lg font-semibold" : `mt-1 text-lg font-semibold ${positive ? "text-buy" : "text-sell"}`}>{plain ? value.toLocaleString("en-IN") : `${positive ? "+" : ""}${value.toLocaleString("en-IN")} Cr`}</div>
    </div>
  );
}
