"use client";

import { cn, formatSigned } from "@/lib/utils";
import type { MarketItem } from "@/lib/api";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { Area, AreaChart, ResponsiveContainer } from "recharts";

export function Panel({ title, children, action }: { title: string; children: React.ReactNode; action?: React.ReactNode }) {
  return (
    <section className="rounded-lg border border-line bg-panel shadow-glow">
      <div className="flex min-h-12 items-center justify-between border-b border-line px-4">
        <h2 className="text-sm font-semibold tracking-wide">{title}</h2>
        {action}
      </div>
      <div className="p-4">{children}</div>
    </section>
  );
}

export function MetricCard({ item }: { item: MarketItem }) {
  const positive = item.day_change >= 0;
  const data = item.month_trend.map((value, index) => ({ index, value }));

  return (
    <div className="rounded-lg border border-line bg-panel2 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm text-muted">{item.name}</div>
          <div className="mt-1 text-xl font-semibold">{item.value.toLocaleString("en-IN")} <span className="text-xs text-muted">{item.currency}</span></div>
        </div>
        <span className={cn("flex items-center gap-1 rounded-md px-2 py-1 text-xs font-semibold", positive ? "bg-buy/10 text-buy" : "bg-sell/10 text-sell")}>
          {positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
          {formatSigned(item.day_change)}
        </span>
      </div>
      <div className="mt-4 h-14">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <Area type="monotone" dataKey="value" stroke={positive ? "#20c997" : "#ff5b6e"} fill={positive ? "#20c99722" : "#ff5b6e22"} strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-3 flex justify-between text-xs text-muted">
        <span>Week {formatSigned(item.week_change)}</span>
        <span>{item.symbol}</span>
      </div>
    </div>
  );
}

export function SentimentGauge({ score, label }: { score: number; label: string }) {
  return (
    <div>
      <div className="relative h-4 overflow-hidden rounded-full bg-line">
        <div className="h-full rounded-full bg-gradient-to-r from-sell via-warn to-buy" style={{ width: `${score}%` }} />
      </div>
      <div className="mt-3 flex items-end justify-between">
        <div>
          <div className="text-4xl font-semibold">{score}</div>
          <div className="text-sm text-muted">Market mood meter</div>
        </div>
        <div className="rounded-md border border-line px-3 py-2 text-sm font-semibold">{label}</div>
      </div>
    </div>
  );
}
