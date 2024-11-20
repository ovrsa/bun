import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from '../mocks/server';

// MSW サーバーのライフサイクル設定
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
