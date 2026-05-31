import { Panel } from "@/components/cards";
import { AppShell } from "@/components/shell";
import { WatchlistBoard } from "@/components/watchlist-board";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function WatchlistPage() {
  const watchlist = await api.watchlist();
  return (
    <AppShell>
      <h1 className="mb-1 text-2xl font-semibold">Watchlist</h1>
      <p className="mb-6 text-sm text-muted">Track price, linked news, alerts, and AI stock summaries.</p>
      <Panel title="Primary Watchlist">
        <WatchlistBoard initialName={watchlist.name} initialItems={watchlist.items} />
      </Panel>
    </AppShell>
  );
}
