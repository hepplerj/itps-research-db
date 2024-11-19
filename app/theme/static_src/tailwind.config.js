// app/theme/static_src/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Adjust these paths according to your project structure
    "../../templates/**/*.html",
    "../../**/templates/**/*.html",
    "../../**/static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        iona: {
          white: "#fff",
          maroon: "#6f2c3e",
          gold: "#f0ab00",
          "light-gray": "#e0e1dd",
          "medium-gray": "#adafaf",
          "dark-gray": "#565a5c",
          "deep-blue": "#0046ad",
          "sea-blue": "#63b1e5",
          "aqua-green": "#76d2b6",
        },
      },
      fontFamily: {
        sans: [
          '"Work Sans"',
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Ubuntu",
          "sans-serif",
        ],
        serif: [
          '"PT Serif"',
          "ui-serif",
          "Georgia",
          "Cambria",
          "Times New Roman",
          "Times",
          "serif",
        ],
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "Consolas",
          "Monaco",
          "monospace",
        ],
      },
      spacing: {
        container: "clamp(16rem, 66vw, 75rem)",
        section: "clamp(2rem, 5vw, 4rem)",
        xs: "clamp(0.75rem, 1vw, 1rem)",
        sm: "clamp(1rem, 2vw, 1.5rem)",
        md: "clamp(1.5rem, 3vw, 2rem)",
        lg: "clamp(2rem, 4vw, 3rem)",
      },
      fontSize: {
        body: "clamp(1rem, 1.2vw, 1.2rem)",
      },
    },
  },
  plugins: [],
};
