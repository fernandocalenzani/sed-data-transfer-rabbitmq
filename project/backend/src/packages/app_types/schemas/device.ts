import { IMongoDefaults } from "./shared";

export interface IDeviceSchema extends IMongoDefaults {
  client: string;
  name: string;
  description: string;
  coords: number[];
  ip: string | null;
  sn: string;
  port: string | null;
  status: boolean;
  info: String[] | null;
  isDeleted: boolean;
}
