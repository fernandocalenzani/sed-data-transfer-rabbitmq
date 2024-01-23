import { Request } from "express";
import IP from "ip";
import lodash from "lodash";

export async function getRequestIp(req: Request) {
  const userIp = await existIp(req);
  console.warn(userIp);
  return userIp;
}

async function existIp(req: Request) {
  if (!lodash.isEmpty(req.headers["x-forwarded-for"])) {
    return (req.headers["x-forwarded-for"] as string[])[0];
  } else if (req.headers["x-appengine-user-ip"]) {
    return (req.headers["x-appengine-user-ip"] as string[])[0];
  } else {
    return IP.address();
  }
}
