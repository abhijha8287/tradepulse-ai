"use client";

import { RefreshCw } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const REFRESH_MS = 60_000;

export function AutoRefresh() {
  const router = useRouter();
  const [lastRefresh, setLastRefresh] = useState(() => new Date());

  useEffect(() => {
    const interval = window.setInterval(() => {
      router.refresh();
      setLastRefresh(new Date());
    }, REFRESH_MS);
    return () => window.clearInterval(interval);
  }, [router]);

  return (
    <div className="hidden items-center gap-2 rounded-md border border-line bg-panel px-3 py-2 text-xs text-muted xl:flex">
      <RefreshCw size={14} />
      <span>Auto {lastRefresh.toISOString().slice(11, 16)} UTC</span>
    </div>
  );
}
