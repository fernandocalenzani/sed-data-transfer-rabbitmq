import * as crypto from "crypto";
import { NextFunction, Request, Response } from "express";
import { Forbidden } from "http-errors";
import { generalConfig } from "../../infra/config/_index";

export const authClient = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
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

export const authApi = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const api_key = (req.headers?.authorization?.replace("Bearer ", "") ??
      null) as string;

    const key_verified = checkApiKey(
      process.env.BACKEND_SECRET_KEY || "",
      api_key,
      generalConfig.expirations.apikey,
      process.env.BACKEND_SECRET_DATA || ""
    );

    if (key_verified) {
      return next();
    } else {
      return next(new Error(`Erro: invalid API key`));
    }
  } catch (err) {
    return next(new Error(`${err}`));
  }
};

function checkApiKey(
  secretKey: string,
  apiKey: string,
  expireAt: number,
  data: string
): boolean {
  apiKey = apiKey.replace("-", "+").replace("_", "/");
  const partes = apiKey.split(".");

  if (partes.length !== 2) {
    console.error("Erro: Formato de chave inválido");
    return false;
  }

  const timestamp = parseInt(partes[0], 10);
  const agora = Math.floor(Date.now() / 1000);

  if (agora - timestamp > expireAt) {
    console.error("Erro: Chave expirada");
    return false;
  }

  const dados = `${timestamp}:${data}`;
  const hash_hmac = crypto
    .createHmac("sha256", secretKey)
    .update(dados)
    .digest("base64");

  return hash_hmac === partes[1];
}
