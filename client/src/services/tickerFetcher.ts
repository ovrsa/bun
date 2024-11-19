import { ref } from 'vue';
import apiClient from './apiAxios';

export const tickerList = ref<{ value: string; label: string }[]>([])


export const fetchTickerList = async (query: string) => {
  try {
    const response = await apiClient.get(import.meta.env.VITE_API_TICKERS, { params: { query } })
    return response.data.map((ticker: { Symbol: string; Name: string }) => ({
      value: ticker.Symbol,
      label: ticker.Name
    }))
  } catch (error) {
    console.error('Error fetching tickers:', error)
    return []
  }
}