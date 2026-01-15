/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [ 
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'brand-yellow': '#FDE68A',
        'brand-yellow-100': '#FEF9C3',
        'brand-red': '#DC2626',
        'brand-red-dark': '#B91C1C'
      }
    },
  },
  plugins: [],
};
