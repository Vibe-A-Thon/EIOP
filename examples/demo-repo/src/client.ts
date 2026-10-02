import { handleRequest } from "./service";

export function dispatch(payload: string) {
  return handleRequest(payload);
}