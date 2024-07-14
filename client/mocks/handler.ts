// src/mocks/handlers.ts
import { rest } from "msw";

export const handlers = [
  rest.get("/api/user", (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ id: 1, name: "John Doe" })
    );
  }),

  rest.post("/api/login", (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ token: "fake-token" })
    );
  }),
];
