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
  projectConfig: {
    host: process.env.BACKEND_HOST,
    port: process.env.BACKEND_PORT,
  },
};
