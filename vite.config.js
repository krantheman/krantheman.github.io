import { fileURLToPath, URL } from "node:url";
import { resolve } from "path";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
	base: "./",
	plugins: [vue(), tailwindcss()],
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},
	build: {
		rollupOptions: {
			input: {
				main: resolve(__dirname, "index.html"),
				404: resolve(__dirname, "public/404.html"),
			},
		},
	},
});
