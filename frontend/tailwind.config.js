/** @type {import('tailwindcss').Config} */
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#f8f9fa",   // light gray background
        input: "#ffffff",
        accent: "#2563eb", // blue
        ok: "#16a34a",   // green
        err: "#dc2626",  // red
        muted: "#6b7280" // gray-500
      }
    }
  },
  plugins: [],
}
