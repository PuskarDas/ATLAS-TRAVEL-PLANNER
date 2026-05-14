import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy /api to the FastAPI app so the browser always calls the same origin as the
// Vite dev server (localhost:3000 or your LAN IP). Avoids CORS failures when using
// "Network" URLs like http://192.168.x.x:3000/.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
