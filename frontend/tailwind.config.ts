import type { Config } from 'tailwindcss'

export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            backgroundImage: {
                "gradient-hero": "var(--gradient-hero)"
            }
        },
    },
    plugins: [],
} satisfies Config