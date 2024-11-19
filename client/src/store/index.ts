import {
  AuthState,
  CompanyFinancialsState,
  CompanyProfileState,
  stockPricesState,
} from '@/types/interfaces'
import { InjectionKey } from 'vue'
import { createStore, Store } from 'vuex'
import auth from './modules/auth'
import companyFinancials from './modules/companyFinancials'
import companyProfile from './modules/companyProfile'
import stockPrices from './modules/stockPrices'

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
