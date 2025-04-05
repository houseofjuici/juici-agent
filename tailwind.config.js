/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/frontend/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/frontend/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/frontend/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: '#d4d4d4',
            a: {
              color: '#00897B',
              '&:hover': {
                color: '#6A1B9A',
              },
            },
            h1: {
              color: '#6A1B9A',
            },
            h2: {
              color: '#6A1B9A',
            },
            h3: {
              color: '#6A1B9A',
            },
            strong: {
              color: '#6A1B9A',
            },
            code: {
              color: '#00897B',
              backgroundColor: '#1e1e1e',
              padding: '0.25rem 0.5rem',
              borderRadius: '0.25rem',
            },
            'code::before': {
              content: '""',
            },
            'code::after': {
              content: '""',
            },
            hr: {
              borderColor: '#2d2d2d',
            },
            ul: {
              li: {
                '&::marker': {
                  color: '#00897B',
                },
              },
            },
            ol: {
              li: {
                '&::marker': {
                  color: '#00897B',
                },
              },
            },
          },
        },
      },
      fontFamily: {
        mono: ['Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
} 