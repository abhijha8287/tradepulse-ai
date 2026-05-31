import { MetricCard, Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function GlobalPage() {
  const { markets } = await api.global();
  const groups = {
    "US Markets": ["IXIC", "GSPC", "DJI"],
    "Currency": ["USDINR"],
    "Asian Markets": ["N225", "HSI", "SSEC"],
    "Commodities": ["CL", "GC", "SI"],
    "Bonds": ["US10Y"]
  };

  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">Global Market Analysis</h1>
      <p className="mb-6 text-sm text-muted">US indices, USD/INR, Asia, commodities, and bond yields with daily, weekly, and monthly context.</p>
      <div className="space-y-4">
        {Object.entries(groups).map(([title, symbols]) => (
          <Panel title={title} key={title}>
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {markets.filter((item) => symbols.includes(item.symbol)).map((item) => <MetricCard key={item.symbol} item={item} />)}
            </div>
          </Panel>
        ))}
      </div>
    </AppShell>
  );
}
