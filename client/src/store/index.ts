import { createStore } from 'vuex';
import auth from './modules/auth';
import companyProfile from "./modules/companyProfile";
import companyFinancials from "./modules/companyFinancials";
import stockPrices from './modules/stockPrices';

const store = createStore({
  modules: {
    auth,
    companyProfile,
    companyFinancials,
    stockPrices
  },
});

export default store;
