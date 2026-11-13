/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        kali: {
          bg: '#0a0d14',
          card: '#101622',
          cardHover: '#161f30',
          border: '#1e293b',
          borderLight: '#334155',
          cyan: '#00d2ff',
          cyanHover: '#38bdf8',
          blue: '#1e70bf',
          green: '#00ff88',
          red: '#f43f5e',
          amber: '#fbbf24',
          textMuted: '#94a3b8'
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace']
      }
    },
  },
  plugins: [],
}
