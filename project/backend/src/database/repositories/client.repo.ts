import * as Model from "../schemas/_index";
import { BaseRepository } from "./abstract.repo";

export const clientProfileRepository = new BaseRepository(
  Model.clientProfileModel
);

export const clientDeviceRepository = new BaseRepository(Model.deviceModel);
