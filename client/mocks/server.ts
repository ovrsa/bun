import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// サーバーを作成
export const server = setupServer(...handlers);
