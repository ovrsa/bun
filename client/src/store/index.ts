// /src/store/index.ts
import { createStore } from 'vuex';
import auth from './modules/auth';  // auth モジュールをインポート

const store = createStore({
  modules: {
    auth,  // auth モジュールを登録
  },
});

export default store;
