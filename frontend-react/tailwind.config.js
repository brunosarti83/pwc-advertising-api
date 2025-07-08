const {heroui} = require("@heroui/react");

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{ts,js,tsx,jsx}",
    "./node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [heroui({
    defaultTheme: "dark"
  })],
}

