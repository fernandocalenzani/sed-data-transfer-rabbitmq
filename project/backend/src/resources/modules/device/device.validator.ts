import { NextFunction, Request, Response } from "express";
import { BadRequest } from "http-errors";
import { z } from "zod";

export const createSchema = z.object({
  client: z.string(),
  name: z.string(),
  description: z.string(),
  coords: z.array(z.number()),
  ip: z.string().nullable(),
  sn: z.string(),
  port: z.string().nullable(),
  status: z.boolean(),
});

export const updateSchema = z.object({
  _id: z.string(),
  name: z.string().optional(),
  description: z.string().optional(),
  coords: z.array(z.number()).optional(),
  ip: z.string().optional(),
  services: z.array(z.string()),
  sn: z.string().optional(),
  port: z.string().optional(),
  status: z.boolean().optional(),
  info: z.string().optional(),
});

export const createValidator = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const payload = req.body;

    req.body = createSchema.parse(payload);
    return next();
  } catch (err) {
    console.error(err);
    return next(new BadRequest(`Error: ${err}`));
  }
};

export const updateValidator = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const payload = req.body;

    req.body = updateSchema.parse(payload);
    return next();
  } catch (err) {
    console.error(err);
    return next(new BadRequest(`Error: ${err}`));
  }
};
