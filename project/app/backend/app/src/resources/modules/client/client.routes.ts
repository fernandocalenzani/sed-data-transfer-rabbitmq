import { Request, Response, Router } from "express";
import { IUserAuth } from "../../../packages/app_types/_index";
import { IClientSchema } from "../../../packages/app_types/schemas/_index";
import { authClient } from "../../middleware/_index";
import ClientService from "./client.service";
import * as Validator from "./client.validator";

const routes = Router();

routes.post(
  "/createProfile",
  Validator.createClientValidator,
  async (req: Request, res: Response) => {
    return new Promise(async (resolve) => {
      const payload = req.body as unknown as IClientSchema;
      
      return await ClientService.createProfile(req, res, payload);
    });
  }
);

routes.put(
  "/editProfile",
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

      return await ClientService.updateProfile(
        req,
        res,
        payload,
        userAuth,
        _id
      );
    });
  }
);

routes.delete(
  "/deleteProfile",
  authClient,
  async (req: Request, res: Response) => {
    return new Promise(async (resolve) => {
      const payload = req.body as unknown as IClientSchema;
      const _id = req.query._id as string;
      const userAuth: IUserAuth = {
        _id: "",
        email: "",
        name: "",
      };

      return await ClientService.deleteProfile(req, res, userAuth, _id);
    });
  }
);

routes.get("/readProfile", authClient, async (req: Request, res: Response) => {
  return new Promise(async (resolve) => {
    const payload = req.body as unknown as IClientSchema;
    const _id = req.query._id as string;
    const userAuth: IUserAuth = {
      _id: "",
      email: "",
      name: "",
    };

    return await ClientService.readProfile(req, res, userAuth, _id);
  });
});

export default routes;
