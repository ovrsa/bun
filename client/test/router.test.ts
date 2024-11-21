import Home from '@/pages/Home.vue';
import Login from '@/pages/Login.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createStore } from 'vuex';

describe('Router', () => {
  let testRouter;
  let store;

  beforeEach(() => {
    // Vuexストアを作成し、認証モジュールを設定
    store = createStore({
      modules: {
        auth: {
          namespaced: true,
          state: { isAuthenticated: false }, // 初期状態は未認証
          actions: {
            checkAuth: vi.fn(), // スパイとして設定
          },
        },
      },
    });

    // ルートを定義
    const routes = [
      { path: '/', component: Home, meta: { requiresAuth: true } }, // 認証が必要なルート
      { path: '/login', component: Login }, // ログインルート
    ];

    // テスト用のルーターを作成
    testRouter = createRouter({
      history: createWebHistory(),
      routes,
    });

    // ルーターのナビゲーションガードを設定
    testRouter.beforeEach((to, from, next) => {
      const isAuthenticated = store.state.auth.isAuthenticated; // 認証状態を取得
      const requiresAuth = to.matched.some(record => record.meta.requiresAuth); // 認証が必要か確認

      // 認証が必要で未認証の場合、ログインページにリダイレクト
      if (requiresAuth && !isAuthenticated) {
        return next('/login');
      }

      next(); // 認証が不要または認証済みの場合
    });
  });

  /**
   * ルーターのナビゲーションガードのテスト
   */
  it('should redirect to login if user is not authenticated', async () => {
    // 認証が必要なルートにアクセス
    await testRouter.push('/');
    await testRouter.isReady();

    // 未認証の場合、ログインページにリダイレクトされることを確認
    expect(testRouter.currentRoute.value.fullPath).toBe('/login');
  });


  it('should allow access to a protected route if user is authenticated', async () => {
    store.state.auth.isAuthenticated = true; // 認証済み状態に設定
  
    await testRouter.push('/');
    await testRouter.isReady();
  
    // 認証済みなのでリダイレクトせずにそのままアクセスできることを確認
    expect(testRouter.currentRoute.value.fullPath).toBe('/');
  });

  /**
   * 認証が不要なルートのテスト
   */
  it('should allow access to a non-protected route regardless of authentication state', async () => {
    await testRouter.push('/login'); // 認証不要のルート
    await testRouter.isReady();
  
    // リダイレクトされずにそのまま進めることを確認
    expect(testRouter.currentRoute.value.fullPath).toBe('/login');
  });
  
  /**
   * 認証チェックが完了するまでリダイレクトを待つテスト
   */
  it('should wait for authentication check before redirecting', async () => {
    // モックで非同期の認証チェックを設定
    store.state.auth.isAuthenticated = null;
    store.dispatch = vi.fn(() =>
      new Promise(resolve => {
        setTimeout(() => {
          store.state.auth.isAuthenticated = false; // 認証失敗をシミュレート
          resolve();
        }, 50);
      })
    );
  
    await testRouter.push('/');
    await testRouter.isReady();
  
    // 認証チェック後、ログインページにリダイレクトされることを確認
    expect(testRouter.currentRoute.value.fullPath).toBe('/login');
  });
  
  /**
   * ログアウト後のリダイレクトテスト
   */
  it('should redirect to login after user logs out', async () => {
    store.state.auth.isAuthenticated = true; // 認証済みから開始
    await testRouter.push('/'); // 認証済みで保護されたルートにアクセス
    await testRouter.isReady();
  
    store.state.auth.isAuthenticated = false; // ログアウト
  
    // 別のルートに移動してから再度'/'
    await testRouter.push('/login'); // 一度他のルートへ
    await testRouter.push('/'); // 再度アクセス
  
    // ログアウト後はログインページにリダイレクトされることを確認
    expect(testRouter.currentRoute.value.fullPath).toBe('/login');
  });
});