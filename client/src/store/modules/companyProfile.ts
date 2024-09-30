import { Module } from 'vuex';

interface CompanyProfile {
  company_name: string;
  ticker: string;
  country: string;
  currency: string;
  exchange: string;
  ipo_date: string;
  market_capitalization: number;
  phone: string;
  share_outstanding: number;
  website_url: string;
  logo_url: string;
  finnhub_industry: string;
}

interface CompanyProfileState {
  profile: CompanyProfile | null;
  loading: boolean;
  error: string | null;
}

const state: CompanyProfileState = {
  profile: null,
  loading: false,
  error: null,
};

const companyProfileModule: Module<CompanyProfileState, any> = {
  namespaced: true,
  state,
  mutations: {
    SET_PROFILE(state, profile: CompanyProfile) {

      state.profile = profile;
    },
    SET_LOADING(state, loading: boolean) {
      state.loading = loading;
    },
    SET_ERROR(state, error: string | null) {
      state.error = error;
    },
  },
  actions: {
    async fetchCompanyProfile({ commit }, symbol: string) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      try {
        const response = await fetch(`http://localhost:8000/api/company-profile/?symbol=${symbol}`);
        if (!response.ok) {
          throw new Error('Failed to fetch company profile.');
        }
        const data: CompanyProfile = await response.json();
        commit('SET_PROFILE', data);
      } catch (error: any) {
        commit('SET_ERROR', error.message || 'An error occurred while fetching data.');
      } finally {
        commit('SET_LOADING', false);
      }
    },
    clearProfile({ commit }) {
      commit('SET_PROFILE', null);
    },
  },
  getters: {
    profile: (state) => state.profile,
    loading: (state) => state.loading,
    error: (state) => state.error,
  },
};

export default companyProfileModule;
