import { NextFunction, Request, Response } from "express";
import { Forbidden } from "http-errors";

export const authClient = async (req: Request, res: Response, next: NextFunction) => {
  try {
    return next();
    const jwt = (req.headers?.authorization?.replace("Bearer ", "") ?? null) as
      | string
      | null;

    if (!jwt) {
      return next(new Forbidden("Usuário não possui autorizaçao"));
    }

    return next();
  } catch (err) {
    return next(new Error(`${err}`));
  }
};
