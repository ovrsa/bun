import { fetchTickerList } from '@/application/services/tickerFetcher'
import debounce from 'lodash/debounce'
import { ref, watch } from 'vue'
import { useStore } from 'vuex'

const selectedTicker = ref(localStorage.getItem('selectedTicker') || '')
const searchTerm = ref('')
const filteredTickerList = ref<{ value: string; label: string }[]>([])

export function useTicker() {
  const store = useStore()

  const selectTicker = async (ticker: { value: string; label: string }) => {
    selectedTicker.value = ticker.label
    localStorage.setItem('selectedTicker', ticker.label)

    try {
      await store.dispatch('companyProfile/fetchCompanyProfile', ticker.value)
      await store.dispatch('companyFinancials/fetchCompanyFinancials', ticker.value)
      await store.dispatch('stockPrices/fetchStockPrices', ticker.value)
    } catch (error) {
      console.error('Dispatch failed:', error)
    }
  }

  // デバウンスを使用してsearchTermの変更を監視
  const debouncedFetchTickerList = debounce(async (newTerm: string) => {
    if (newTerm) {
      filteredTickerList.value = await fetchTickerList(newTerm)
    } else {
      filteredTickerList.value = []
    }
  }, 1000)

  // watchを使ってsearchTermの変更に応じてデバウンス処理を呼び出し
  watch(searchTerm, async (newTerm) => {
    debouncedFetchTickerList(newTerm)
    if (newTerm) {
      filteredTickerList.value = await fetchTickerList(newTerm)
    } else {
      filteredTickerList.value = []
    }
  })

  return {
    searchTerm,
    selectedTicker,
    filteredTickerList,
    selectTicker,
  }
}