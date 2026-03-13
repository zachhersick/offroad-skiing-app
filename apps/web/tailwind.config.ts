import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ridge: "#173728",
        canyon: "#9b5a2a",
        frost: "#d7e8ef",
        shale: "#101816",
        sand: "#f4ecdf"
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        body: ["ui-sans-serif", "system-ui"]
      },
      boxShadow: {
        terrain: "0 20px 60px rgba(16, 24, 22, 0.18)"
      }
    }
  },
  plugins: []
};

export default config;

