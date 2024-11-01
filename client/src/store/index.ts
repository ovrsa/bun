import { createStore, Store } from 'vuex'
import { InjectionKey } from 'vue'
import companyFinancials, {
  CompanyFinancialsState,
} from './modules/companyFinancials'
import stockPrices, { StockPricesState } from './modules/stockPrices'
import companyProfile, { CompanyProfileState } from './modules/companyProfile'
import auth, { AuthState } from './modules/auth'

export interface RootState {
  companyProfile: CompanyProfileState
  companyFinancials: CompanyFinancialsState
  stockPrices: StockPricesState
  auth: AuthState
}

export const Key: InjectionKey<Store<RootState>> = Symbol()

const store = createStore({
  modules: {
    auth,
    companyProfile,
    companyFinancials,
    stockPrices,
  },
})

export default store
