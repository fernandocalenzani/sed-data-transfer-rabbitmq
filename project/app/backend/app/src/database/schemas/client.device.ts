import { Schema, model } from "mongoose";
import { IDeviceSchema } from "../../packages/app_types/_index";

const deviceSchema = new Schema<IDeviceSchema>(
  {
    client: {
      type: String,
      ref: "client_Profiles",
      required: true,
    },
    name: { type: String, required: false },
    description: { type: String, required: false },
    coords: [{ type: Number, required: false }],
    ip: { type: String, required: true, default: null },
    sn: { type: String, required: true, default: null },
    port: { type: String, required: true, default: null },
    status: { type: Boolean, required: false, default: false },
    info: [{ type: String, default: false }],

    isDeleted: { type: Boolean, default: false, select: false },
  },

  {
    timestamps: true,
    versionKey: "__v",
  }
);

export default model<IDeviceSchema>("client_Devices", deviceSchema);
