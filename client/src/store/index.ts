import { createStore, Store } from 'vuex'
import { InjectionKey } from 'vue'
import companyFinancials from './modules/companyFinancials'
import stockPrices from './modules/stockPrices'
import companyProfile from './modules/companyProfile'
import auth from './modules/auth'
import {
  CompanyFinancialsState,
  CompanyProfileState,
  stockPricesState,
  AuthState,
} from '@/types/interfaces'

export interface RootState {
  companyProfile: CompanyProfileState
  companyFinancials: CompanyFinancialsState
  stockPrices: stockPricesState
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
