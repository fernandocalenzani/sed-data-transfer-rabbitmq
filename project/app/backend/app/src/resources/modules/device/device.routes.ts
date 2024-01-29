import { Request, Response, Router } from "express";
import { IUserAuth } from "../../../packages/app_types/_index";
import {
  IClientSchema,
  IDeviceSchema,
} from "../../../packages/app_types/schemas/_index";
import { authApi, authClient } from "../../middleware/_index";
import Service from "./device.service";
import * as Validator from "./device.validator";

const routes = Router();

routes.post(
  "/create",
  Validator.createValidator,
  async (req: Request, res: Response) => {
    return new Promise(async (resolve) => {
      const payload = req.body as unknown as IDeviceSchema;
      return await Service.create(req, res, payload);
    });
  }
);

routes.put(
  "/edit",
  authClient,
  Validator.updateValidator,
  async (req: Request, res: Response) => {
    return new Promise(async (resolve) => {
      const payload = req.body as unknown as IDeviceSchema;
      const _id = req.query._id as string;
      const userAuth: IUserAuth = {
        _id: "",
        email: "",
        name: "",
      };

      return await Service.update(req, res, payload, userAuth);
    });
  }
);

routes.delete("/delete", authClient, async (req: Request, res: Response) => {
  return new Promise(async (resolve) => {
    const payload = req.body as unknown as IClientSchema;
    const _id = req.query._id as string;
    const userAuth: IUserAuth = {
      _id: "",
      email: "",
      name: "",
    };

    return await Service.delete(req, res, userAuth, _id);
  });
});

routes.get("/read-by-id", authClient, async (req: Request, res: Response) => {
  return new Promise(async (resolve) => {
    const payload = req.body as unknown as IClientSchema;
    const _id = req.query._id as string;
    const userAuth: IUserAuth = {
      _id: "",
      email: "",
      name: "",
    };

    return await Service.readById(req, res, userAuth, _id);
  });
});

routes.get("/read-all", authApi, async (req: Request, res: Response) => {
  return new Promise(async (resolve) => {
    return await Service.readAll(req, res);
  });
});

export default routes;
