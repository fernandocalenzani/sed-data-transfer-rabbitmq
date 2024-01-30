import { Request, Response, Router } from "express";
import { IUserAuth } from "../../../packages/app_types/_index";
import { IClientSchema } from "../../../packages/app_types/schemas/_index";
import { authApi, authClient } from "../../middleware/_index";
import ClientService from "./client.service";
import * as Validator from "./client.validator";

const routes = Router();

routes.post(
  "/create",
  Validator.createClientValidator,
  async (req: Request, res: Response) => {
    return new Promise(async (resolve) => {
      const payload = req.body as unknown as IClientSchema;

      return await ClientService.create(req, res, payload);
    });
  }
);

routes.put(
  "/edit",
  authClient,
  Validator.updateClientValidator,
  async (req: Request, res: Response) => {
    return new Promise(async (resolve) => {
      const payload = req.body as unknown as IClientSchema;
      const _id = req.query._id as string;
      const userAuth: IUserAuth = {
        _id: "",
        email: "",
        name: "",
      };

      return await ClientService.update(req, res, payload, userAuth, _id);
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

    return await ClientService.delete(req, res, userAuth, _id);
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

    return await ClientService.readById(req, res, userAuth, _id);
  });
});

routes.get("/read-all", authApi, async (req: Request, res: Response) => {
  return new Promise(async (resolve) => {
    return await ClientService.readAll(req, res);
  });
});

export default routes;
