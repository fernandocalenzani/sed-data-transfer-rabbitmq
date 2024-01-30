import { Router } from "express";
import ClientProfileRoutes from "../modules/client/client.routes";
import DeviceRoutes from "../modules/device/device.routes";

const router = Router();

export const clientApi = router.use("/api/client-profile", ClientProfileRoutes);

export const deviceApi = router.use("/api/device", DeviceRoutes);
