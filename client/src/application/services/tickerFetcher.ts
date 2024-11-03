import apiClient from './apiAxios';
import { ref } from 'vue'

export const tickerList = ref<{ value: string; label: string }[]>([])

export const fetchTickerList = async () => {
  try {
    const response = await apiClient.get('/tickers')
    console.log('response:', response.data)
    tickerList.value = response.data.map((ticker: { Symbol: string; Name: string }) => ({
      value: ticker.Symbol,
      label: ticker.Name.trim(),
    }))
  } catch (error) {
    console.error('Error fetching tickers:', error)
  }
}