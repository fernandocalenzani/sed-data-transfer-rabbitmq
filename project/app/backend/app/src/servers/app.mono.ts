import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import cors from "cors";
import "dotenv/config";
import express from "express";
import requestRateLimit from "express-rate-limit";
import "reflect-metadata";
import { dbConnection } from "../database/connection/_index";
import * as generalConfig from "../infra/config/_index";
import { corsOptions, limitRequest } from "../infra/config/_index";
import * as routes from "../resources/routes/_index";

const apiGroups = {
  apiG1: [routes.readsApi],
};

async function setupFunction(routers: express.Router[]) {
  const instance = express();

  instance.use(cors(corsOptions));
  instance.use(cookieParser());
  instance.use(express.json());
  instance.use(requestRateLimit(limitRequest.app));
  instance.use(bodyParser.urlencoded({ extended: true }));

  dbConnection.createConnection(process.env.MONGO_HOST || "");

  routers.forEach((router) => {
    instance.use(router);
  });

  instance.listen(
    `${generalConfig.generalConfig.projectConfig.host}:${generalConfig.generalConfig.projectConfig.port}`,
    () => {
      console.log(
        "listening env: " + generalConfig.generalConfig.projectConfig.port
      );
    }
  );
}

setupFunction(apiGroups.apiG1);
