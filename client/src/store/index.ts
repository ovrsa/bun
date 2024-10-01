import { createStore } from 'vuex';
import auth from './modules/auth';
import companyProfile from "./modules/companyProfile";

const store = createStore({
  modules: {
    auth,
    companyProfile,
  },
});

export default store;
