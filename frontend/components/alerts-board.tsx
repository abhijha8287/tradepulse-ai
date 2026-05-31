"use client";

import { API_BASE, type AlertRule } from "@/lib/api";
import { cn } from "@/lib/utils";
import { BellRing, Mail, Smartphone } from "lucide-react";
import { useState } from "react";

export function AlertsBoard({ initialAlerts }: { initialAlerts: AlertRule[] }) {
  const [alerts, setAlerts] = useState(initialAlerts);
  const [busy, setBusy] = useState<string | null>(null);

  async function toggleAlert(alert: AlertRule) {
    setBusy(alert.id);
    const response = await fetch(`${API_BASE}/api/v1/alerts/${alert.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled: !alert.enabled })
    });
    const data = await response.json();
    setAlerts(data.alerts);
    setBusy(null);
  }

  return (
    <div className="grid gap-3 xl:grid-cols-2">
      {alerts.map((alert) => (
        <article key={alert.id} className="rounded-lg border border-line bg-panel2 p-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-md border border-line px-2 py-1 text-xs text-muted">{alert.alert_type}</span>
                <span className={cn("rounded-md px-2 py-1 text-xs font-semibold", alert.enabled ? "bg-buy/10 text-buy" : "bg-line text-muted")}>{alert.enabled ? "Enabled" : "Paused"}</span>
              </div>
              <h2 className="mt-3 text-base font-semibold">{alert.label}</h2>
            </div>
            <button
              onClick={() => void toggleAlert(alert)}
              disabled={busy === alert.id}
              className={cn("relative h-6 w-11 rounded-full border border-line transition disabled:opacity-50", alert.enabled ? "bg-buy" : "bg-canvas")}
              aria-label={`Toggle ${alert.label}`}
            >
              <span className={cn("absolute top-1 h-4 w-4 rounded-full bg-white transition", alert.enabled ? "left-6" : "left-1")} />
            </button>
          </div>
          <p className="mt-3 text-sm leading-6 text-muted">{alert.threshold}</p>
          <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-muted">
            <span className="flex items-center gap-1"><BellRing size={14} /> {alert.channel.includes("Push") ? "Push" : "Rules engine"}</span>
            {alert.channel.includes("Email") ? <span className="flex items-center gap-1"><Mail size={14} /> Email</span> : null}
            {alert.channel.includes("Push") ? <span className="flex items-center gap-1"><Smartphone size={14} /> Mobile</span> : null}
            <span>{alert.last_triggered ? `Last ${formatUtc(alert.last_triggered)}` : "No recent trigger"}</span>
          </div>
        </article>
      ))}
    </div>
  );
}

function formatUtc(value: string) {
  return `${new Date(value).toISOString().replace("T", " ").slice(0, 16)} UTC`;
}
