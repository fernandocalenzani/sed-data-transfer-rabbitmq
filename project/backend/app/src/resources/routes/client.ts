import { Router } from "express";
import ClientProfileRoutes from "../modules/client/client.routes";
const router = Router();

export const readsApi = router.use("/client-profile", ClientProfileRoutes);
