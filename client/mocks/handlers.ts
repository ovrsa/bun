import { http } from 'msw';

/**
 * ログインAPIのモック
 * このファイルでは、APIリクエストに対するモックハンドラーを定義しています。
 * モックを使用することで、実際のAPIに依存せずにテストを行うことができます。
 */
export const handlers = [
  // ログインAPIのPOSTリクエストをモック
  http.post('/api/auth/login/', async (req, res, ctx) => {
    const { email, password } = await req.json();
    // 正しい認証情報が提供された場合
    if (email === 'test@example.com' && password === 'password') {
      return res(ctx.status(200), ctx.json({ token: 'fake-token' })); // 成功レスポンスを返す
    }
    // 認証情報が無効な場合
    return res(ctx.status(401), ctx.json({ error: 'Invalid credentials' })); // エラーレスポンスを返す
  }),

  // ユーザー情報取得APIのGETリクエストをモック
  http.get('/api/user', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ id: 1, name: 'John Doe' })); // 成功レスポンスを返す
  }),
];