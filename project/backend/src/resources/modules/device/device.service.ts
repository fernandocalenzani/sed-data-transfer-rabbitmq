import { Request, Response } from "express";
import {
  clientDeviceRepository,
  clientProfileRepository,
} from "../../../database/repositories/_index";
import { IDeviceSchema, IUserAuth } from "../../../packages/app_types/_index";

export class Service {
  public async create(
    req: Request,
    res: Response,
    payload: IDeviceSchema
  ): Promise<object> {
    try {
      const user = await clientProfileRepository.find({
        _id: payload.client,
      });

      if (user.length <= 0) {
        return res.status(404).json({ message: "Client not found" });
      }

      const data = await clientDeviceRepository.createOne({
        ...payload,
        info: `[${new Date()}] Device created`,
      });

      return res.status(201).json(data);
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }

  public async update(
    req: Request,
    res: Response,
    payload: IDeviceSchema,
    userJwt: IUserAuth
  ): Promise<object> {
    try {
      const device = await clientDeviceRepository.find({
        _id: payload._id,
      });

      if (device.length <= 0) {
        return res.status(404).json({ message: "Device not found" });
      }

      const data = await clientDeviceRepository.updateOne(payload._id, {
        ...payload,
        $push: { info: `[${new Date()}] Device updated - ${payload.info}` },
      });

      return res.status(201).json(data);
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
      const device = await clientDeviceRepository.find({
        _id: _id,
      });

      if (device.length <= 0) {
        return res.status(404).json({ message: "Device not found" });
      }

      await clientDeviceRepository.deleteOne(_id, {
        name: "Deleted Profile",
      });

      return res.status(200).json({
        message: "Dispositivo deletado com sucesso",
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
      const result = await clientDeviceRepository.find({
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
      const result = await clientDeviceRepository.find({
        status: true,
      });

      return res.status(200).json(result);
    } catch (err: any) {
      console.error(err);
      return res.status(500).json({ message: "Server error: " + err.message });
    }
  }
}

export default new Service();
