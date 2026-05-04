/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      "colors": {
          "surface-container": "#1f1f25",
          "primary-container": "#2792ff",
          "on-surface-variant": "#c0c7d6",
          "tertiary-container": "#e37103",
          "error": "#ffb4ab",
          "primary-fixed": "#d4e3ff",
          "secondary-fixed-dim": "#aac8f9",
          "primary": "#a5c8ff",
          "surface-container-highest": "#35343a",
          "surface-tint": "#a5c8ff",
          "on-tertiary-fixed": "#311300",
          "surface-container-low": "#1b1b20",
          "on-secondary-fixed-variant": "#284871",
          "primary-fixed-dim": "#a5c8ff",
          "surface-container-high": "#2a292f",
          "on-background": "#e4e1e9",
          "inverse-surface": "#e4e1e9",
          "on-secondary": "#0c3159",
          "outline-variant": "#404753",
          "on-primary-fixed-variant": "#004786",
          "on-error": "#690005",
          "secondary": "#aac8f9",
          "secondary-container": "#2b4a74",
          "on-primary-fixed": "#001c3a",
          "inverse-primary": "#005faf",
          "on-secondary-fixed": "#001c3a",
          "tertiary-fixed": "#ffdbc7",
          "outline": "#8a919f",
          "on-tertiary-container": "#471e00",
          "on-error-container": "#ffdad6",
          "error-container": "#93000a",
          "on-surface": "#e4e1e9",
          "tertiary-fixed-dim": "#ffb688",
          "on-tertiary": "#512400",
          "surface-bright": "#39383e",
          "secondary-fixed": "#d4e3ff",
          "on-primary": "#00315f",
          "surface-dim": "#131318",
          "tertiary": "#ffb688",
          "surface-variant": "#35343a",
          "surface": "#131318",
          "surface-container-lowest": "#0e0e13",
          "inverse-on-surface": "#303036",
          "on-tertiary-fixed-variant": "#733600",
          "on-secondary-container": "#9cbaea",
          "on-primary-container": "#002a53",
          "background": "#131318"
      },
      "borderRadius": {
          "none": "0",
          "DEFAULT": "0",
          "lg": "0",
          "xl": "0",
          "full": "0"
      },
      "fontFamily": {
          "headline": ["Space Grotesk"],
          "body": ["Space Grotesk"],
          "label": ["Space Grotesk"]
      }
    }
  },
  plugins: [],
}
