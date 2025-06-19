/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Scan all HTML files in the templates directory
    "./static/src/**/*.js",   // Scan JS files if we add any for interactivity
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
