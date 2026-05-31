import { Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function AdminPage() {
  const health = await api.adminHealth();
  const cards = [
    ["API", health.api],
    ["Database", health.database],
    ["Redis", health.redis],
    ["Worker queue", health.workers],
  ];

  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">Admin Panel</h1>
      <p className="mb-6 text-sm text-muted">Operational controls for APIs, users, logs, news sources, and system health.</p>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map(([item, status]) => (
          <Panel title={item} key={item}><div className="text-2xl font-semibold capitalize text-buy">{status}</div><p className="mt-2 text-sm text-muted">Reported by the FastAPI admin health endpoint.</p></Panel>
        ))}
      </div>
      <div className="mt-4 grid gap-4 xl:grid-cols-[0.8fr_1.2fr]">
        <Panel title="Performance">
          <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-1">
            <Stat label="Cache hit rate" value={`${health.cache_hit_rate.toFixed(1)}%`} />
            <Stat label="Average API response" value={`${health.avg_response_ms} ms`} />
            <Stat label="Active users" value={health.active_users.toLocaleString("en-IN")} />
          </div>
        </Panel>
        <Panel title="News Sources">
          <div className="grid gap-2 md:grid-cols-2">
            {health.news_sources.map((source) => (
              <div key={source} className="rounded-lg border border-line bg-panel2 p-3 text-sm text-muted">{source}</div>
            ))}
          </div>
        </Panel>
      </div>
      <div className="mt-4">
        <Panel title="Recent Logs">
          <div className="space-y-2">
            {health.recent_logs.map((log) => (
              <div key={log.message} className="flex flex-col gap-1 rounded-lg border border-line bg-panel2 p-3 text-sm md:flex-row md:items-center md:gap-3">
                <span className="w-14 font-semibold text-info">{log.level}</span>
                <span className="text-muted">{log.message}</span>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </AppShell>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-panel2 p-3">
      <div className="text-xs text-muted">{label}</div>
      <div className="mt-1 text-xl font-semibold">{value}</div>
    </div>
  );
}
