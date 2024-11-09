/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html", // This ensures that Tailwind processes your HTML file
    "./src/**/*.{js,ts,jsx,tsx}", // Tailwind will look for classes in these files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
