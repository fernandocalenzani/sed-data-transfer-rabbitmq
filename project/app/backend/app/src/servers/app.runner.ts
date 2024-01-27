import * as functions from "firebase-functions";
import "../infra/config/_index";
import * as routes from "../resources/routes/_index";
import App from "./app.setup";

const apiGroups = {
  api: [routes.readsApi],
};

/*----| SET: APP |----*/
App.databaseConnection();

/*----| SET: EXPORT FIREBASE JOBS |----*/
const funcConfig = {
  timeoutSeconds: 540,
  memory: "512MB",
} as functions.RuntimeOptions;
const region = "us-central1"; //"southamerica-east1";

export const reports = functions
  .runWith(funcConfig)
  .region(region)
  .https.onRequest(async (request, response) => {
    const routeFunction = await App.setupFunction(apiGroups.api);
    return routeFunction(request, response);
  });
