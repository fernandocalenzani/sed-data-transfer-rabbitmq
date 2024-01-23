import {
  IAddress,
  IFile,
  IPermissions,
  ITokenUpdateData,
} from "../interfaces/_index";
import { IMongoDefaults } from "./shared";

export interface IClientSchema extends IMongoDefaults {
  name: string;
  email: string;
  password: string;
  profilePicture?: IFile;
  birth?: Date;
  cpfCnpj: string;
  address?: IAddress;
  phoneNumber: string;
  token?: ITokenUpdateData;
  tokenUpdateLogin?: ITokenUpdateData;
  permissions?: IPermissions;
  verified: boolean;
}
