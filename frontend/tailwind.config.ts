import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#07090f",
        panel: "#0d111b",
        panel2: "#121827",
        line: "#20283a",
        muted: "#8b98ad",
        ink: "#e8eefc",
        buy: "#20c997",
        sell: "#ff5b6e",
        warn: "#f4b942",
        info: "#4da3ff"
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(255,255,255,0.05), 0 18px 50px rgba(0,0,0,0.35)"
      }
    }
  },
  plugins: []
};

export default config;
