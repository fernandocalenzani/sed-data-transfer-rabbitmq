import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import cors from "cors";
import "dotenv/config";
import express, { Express } from "express";
import requestRateLimit from "express-rate-limit";
import "reflect-metadata";
import { dbConnection } from "../database/connection/_index";
import { corsOptions, limitRequest } from "../infra/config/_index";

class App {
  private instance: Express;

  constructor() {
    this.instance = express();
  }

  public async databaseConnection() {
    await dbConnection.createConnection();
  }

  public async setupFunction(routers: express.Router[]) {
    this.instance.use(cors(corsOptions));
    this.instance.use(cookieParser());
    this.instance.use(express.json());
    this.instance.use(requestRateLimit(limitRequest.app));
    this.instance.use(bodyParser.urlencoded({ extended: true }));
    routers.forEach((router) => {
      this.instance.use(router);
    });

    return this.instance;
  }
}

export default new App();
