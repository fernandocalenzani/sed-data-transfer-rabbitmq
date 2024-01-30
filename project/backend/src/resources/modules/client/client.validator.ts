import { NextFunction, Request, Response } from "express";
import { BadRequest } from "http-errors";
import { z } from "zod";

const CreateUserSchema = z.object({
  name: z.string().refine(
    (value) => {
      const namePattern = /^[A-Z][a-z]+ [A-Z][a-z]+$/;
      return namePattern.test(value);
    },
    { message: "O nome deve estar no formato 'Nome Sobrenome'" }
  ),
  email: z.string().email("Email mal formatado"),
  password: z
    .string()
    .min(8, "A senha deve ter no mínimo 8 caracteres")
    .max(40, "A senha deve ter no máximo 40 caracteres"),
});

const updateUserSchema = z.object({
  name: z.string().refine(
    (value) => {
      const namePattern = /^[A-Z][a-z]+ [A-Z][a-z]+$/;
      return namePattern.test(value);
    },
    { message: "O nome deve estar no formato 'Nome Sobrenome'" }
  ),
  cpfCnpj: z.string(),
  birth: z.string(),
  address: z.object({
    street: z.string(),
    number: z.number(),
    neighborhood: z.string(),
    zipcode: z.string(),
    city: z.string(),
    complement: z.string(),
    state: z.string(),
    coords: z.object({
      latitude: z.number(),
      longitude: z.number(),
    }),
  }),
});

export const createClientValidator = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const payload = req.body;

    req.body = CreateUserSchema.parse(payload);
    return next();
  } catch (err) {
    console.error(err);
    return next(new BadRequest(`Error: ${err}`));
  }
};

export const updateClientValidator = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const payload = req.body;

    req.body = updateUserSchema.parse(payload);
    return next();
  } catch (err) {
    console.error(err);
    return next(new BadRequest(`Error: ${err}`));
  }
};
