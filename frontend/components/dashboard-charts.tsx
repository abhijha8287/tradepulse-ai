"use client";

import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function FlowBarChart({ data }: { data: { date: string; fii: number; dii: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <CartesianGrid stroke="#20283a" vertical={false} />
        <XAxis dataKey="date" stroke="#8b98ad" fontSize={12} />
        <YAxis stroke="#8b98ad" fontSize={12} />
        <Tooltip contentStyle={{ background: "#121827", border: "1px solid #20283a" }} />
        <Bar dataKey="fii" fill="#4da3ff" />
        <Bar dataKey="dii" fill="#20c997" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function ExpectedMoveChart({ low, spot, high }: { low: number; spot: number; high: number }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={[{ name: "Low", value: low }, { name: "Spot", value: spot }, { name: "High", value: high }]}>
        <Area dataKey="value" stroke="#f4b942" fill="#f4b94222" />
        <Tooltip contentStyle={{ background: "#121827", border: "1px solid #20283a" }} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
