"use client";

import { API_BASE, type WatchlistItem } from "@/lib/api";
import { cn } from "@/lib/utils";
import { Plus, Trash2 } from "lucide-react";
import { useState } from "react";

export function WatchlistBoard({ initialName, initialItems }: { initialName: string; initialItems: WatchlistItem[] }) {
  const [items, setItems] = useState(initialItems);
  const [symbol, setSymbol] = useState("");
  const [busy, setBusy] = useState<string | null>(null);

  async function addSymbol() {
    const cleanSymbol = symbol.trim().toUpperCase();
    if (!cleanSymbol) return;
    setBusy("add");
    const response = await fetch(`${API_BASE}/api/v1/watchlist`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: cleanSymbol })
    });
    const data = await response.json();
    setItems(data.items);
    setSymbol("");
    setBusy(null);
  }

  async function removeSymbol(target: string) {
    setBusy(target);
    const response = await fetch(`${API_BASE}/api/v1/watchlist/${target}`, { method: "DELETE" });
    const data = await response.json();
    setItems(data.items);
    setBusy(null);
  }

  return (
    <div>
      <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="text-sm font-semibold">{initialName}</div>
          <div className="text-xs text-muted">{items.length} symbols monitored for price, news, and AI context</div>
        </div>
        <div className="flex min-w-0 gap-2">
          <input
            value={symbol}
            onChange={(event) => setSymbol(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") void addSymbol();
            }}
            placeholder="Add symbol"
            className="h-10 min-w-0 rounded-md border border-line bg-canvas px-3 text-sm outline-none placeholder:text-muted"
          />
          <button onClick={() => void addSymbol()} disabled={busy === "add"} className="grid h-10 w-10 place-items-center rounded-md border border-line bg-info text-white disabled:opacity-50" aria-label="Add symbol">
            <Plus size={17} />
          </button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="text-muted">
            <tr>
              <th className="pb-3">Symbol</th>
              <th className="pb-3">Price</th>
              <th className="pb-3">Change</th>
              <th className="pb-3">News</th>
              <th className="pb-3">AI Summary</th>
              <th className="pb-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.symbol} className="border-t border-line">
                <td className="py-3">
                  <div className="font-semibold">{item.symbol}</div>
                  <div className="text-xs text-muted">{item.name}</div>
                </td>
                <td>{item.price ? item.price.toLocaleString("en-IN") : "Queued"}</td>
                <td className={cn(item.change >= 0 ? "text-buy" : "text-sell")}>{item.change >= 0 ? "+" : ""}{item.change.toFixed(2)}%</td>
                <td>{item.news_count}</td>
                <td className="max-w-md text-muted">{item.ai_summary}</td>
                <td className="text-right">
                  <button onClick={() => void removeSymbol(item.symbol)} disabled={busy === item.symbol} className="inline-grid h-9 w-9 place-items-center rounded-md border border-line bg-panel2 disabled:opacity-50" aria-label={`Remove ${item.symbol}`}>
                    <Trash2 size={15} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
