import { createStore } from 'vuex';
import auth from './modules/auth';
import companyProfile from "./modules/companyProfile";
import companyFinancials from "./modules/companyFinancials";

const store = createStore({
  modules: {
    auth,
    companyProfile,
    companyFinancials
  },
});

export default store;
