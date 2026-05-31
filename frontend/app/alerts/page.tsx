import { AlertsBoard } from "@/components/alerts-board";
import { Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function AlertsPage() {
  const { alerts } = await api.alerts();
  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">Alert System</h1>
      <p className="mb-6 text-sm text-muted">Monitor VIX spikes, FII flow changes, breaking news, OI shifts, and sentiment changes across push and email channels.</p>
      <Panel title="Trading Alerts">
        <AlertsBoard initialAlerts={alerts} />
      </Panel>
    </AppShell>
  );
}
