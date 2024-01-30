import { CorsOptions } from "cors";

export const corsOptions = {
  origin: [``, ``],
  credentials: true,
  maxAge: 3600,
  exposedHeaders: ["*", "Authorization", "Set-Cookie", "X-Custom-Header"],
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
  allowedHeaders: [
    "Content-Type",
    "Authorization",
    "x-csrf-token",
    "Access-Control-Allow-Headers",
  ],
} as CorsOptions;
