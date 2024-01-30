import bcrypt from "bcrypt";
import { Request, Response } from "express";
import { clientProfileRepository } from "../../../database/repositories/_index";
import { IClientSchema, IUserAuth } from "../../../packages/app_types/_index";

export class Service {
  public async create(
    req: Request,
    res: Response,
    payload: IClientSchema
  ): Promise<object> {
    try {
      const user = await clientProfileRepository.createOne({
        ...payload,
        token: {
          token: "encrypted",
          date: new Date(),
        },
        password: bcrypt.hashSync(payload.password, 10),
      });

      return res.status(201).json(user);
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }

  public async update(
    req: Request,
    res: Response,
    payload: IClientSchema,
    userJwt: IUserAuth,
    _id: string
  ): Promise<object> {
    try {
      const user = await clientProfileRepository.updateOne(_id, payload);

      return res.status(201).json(user);
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }

  public async delete(
    req: Request,
    res: Response,
    userJwt: IUserAuth,
    _id: string
  ): Promise<object> {
    try {
      await clientProfileRepository.deleteOne(_id, {
        name: "Deleted Profile",
        email: "",
        password: "",
        token: "",
        permissions: [""],
      });

      return res.status(200).json({
        message: "Usuário deletado com sucesso",
      });
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }

  public async readById(
    req: Request,
    res: Response,
    userJwt: IUserAuth,
    _id: string
  ): Promise<object> {
    try {
      const result = await clientProfileRepository.find({
        _id: _id,
      });

      return res.status(200).json(result);
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }

  public async readAll(req: Request, res: Response): Promise<object> {
    try {
      const result = await clientProfileRepository.find({});
      return res.status(200).json(result);
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }
}

export default new Service();
