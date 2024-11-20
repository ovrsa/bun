import { rest } from 'msw';

export const handlers = [
  rest.post('/api/auth/login/', async (req, res, ctx) => {
    const { email, password } = await req.json();
    if (email === 'test@example.com' && password === 'password') {
      return res(ctx.status(200), ctx.json({ token: 'fake-token' }));
    }
    return res(ctx.status(401), ctx.json({ error: 'Invalid credentials' }));
  }),

  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ id: 1, name: 'John Doe' }));
  }),

  rest.post('/api/login', async (req, res, ctx) => {
    const { email, password } = await req.json();
    if (email === 'test@example.com' && password === 'password') {
      return res(ctx.status(200), ctx.json({ token: 'fake-token' }));
    }
    return res(ctx.status(401), ctx.json({ error: 'Invalid credentials' }));
  }),
];
