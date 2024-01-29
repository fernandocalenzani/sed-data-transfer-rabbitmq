import { Schema, model } from "mongoose";
import { generalConfig } from "../../infra/config/_index";
import { IClientSchema } from "../../packages/app_types/_index";

const clientSchema = new Schema<IClientSchema>(
  {
    name: { type: String, required: true },
    email: { type: String, required: true },
    password: { type: String, required: true, select: false },
    profilePicture: { type: Object, required: false, default: null },
    cpfCnpj: { type: String, required: false, default: null },
    address: { type: Object, required: false, default: null },
    phoneNumber: { type: String, required: false, default: null },
    birth: { type: Date, required: false, default: null },
    token: {
      type: Object,
      expires: generalConfig.expirations.tokens,
      required: false,
      select: false,
      default: null,
    },
    tokenUpdateLogin: {
      type: Object,
      expires: generalConfig.expirations.tokens,
      required: false,
      select: false,
      default: null,
    },
    verified: { type: Boolean, default: false },
    isDeleted: { type: Boolean, default: false, select: false },
  },

  {
    timestamps: true,
    versionKey: "__v",
  }
);

export default model<IClientSchema>("client_Profiles", clientSchema);
