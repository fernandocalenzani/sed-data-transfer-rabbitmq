import { getRequestIp } from '../../resources/helpers/_index';

export const limitRequest = {
  app: {
    windowMs: 5 * 60 * 1000,
    max: 500,
    message: 'message: Rate limit exceeded. Please try again later.',
    keyGenerator: getRequestIp,
  },
  loginClient: {
    windowMs: 5 * 60 * 1000,
    max: 5,
    message: 'message: Rate limit exceeded. Please, wait for 5 minutes and try again.',
    keyGenerator: getRequestIp,
  },
  loginMaster: {
    windowMs: 1 * 60 * 1000,
    max: 1,
    message: 'message: Rate limit exceeded. Please, wait for 1 minute and try again.',
    keyGenerator: getRequestIp,
  },
  providers: {
    windowMs: 5 * 60 * 1000,
    max: 1,
    message: 'message: Rate limit exceeded. Please, wait for 5 minutes and try again.',
    keyGenerator: getRequestIp,
  },
};
