import fs from "fs";
import path from "path";

export const generalConfig = {
  expirations: {
    jwt: "10d",
    refreshJwt: "15min",
    tokens: 1 * 60 * 1000,
    standBySender: 5 * 60 * 1000,
  },
  pagination: {
    size: "10",
  },
  urls: {
    verifyAccount: `/services/confirm-account?token=`,
  },
  permissions: {
    client: ["read", "write"],
  },
  projectConfig: JSON.parse(fs.readFileSync(
    path.resolve(__dirname, "../../config/project_config.json"), "utf-8")),
};
