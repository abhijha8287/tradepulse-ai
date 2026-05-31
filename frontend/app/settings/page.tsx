import { Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";

export default function SettingsPage() {
  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">Settings</h1>
      <p className="mb-6 text-sm text-muted">Manage profile, notification channels, alert thresholds, and dashboard defaults.</p>
      <Panel title="Preferences">
        <div className="grid gap-4 md:grid-cols-2">
          {["Email alerts", "Push notifications", "VIX spike alert", "FII/DII flow alert"].map((item) => (
            <label key={item} className="flex items-center justify-between rounded-lg border border-line bg-panel2 p-4 text-sm">
              {item}
              <input type="checkbox" defaultChecked className="h-4 w-4 accent-buy" />
            </label>
          ))}
        </div>
      </Panel>
    </AppShell>
  );
}
