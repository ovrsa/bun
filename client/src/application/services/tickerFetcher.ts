import apiClient from './apiAxios';
import { ref } from 'vue'

export const tickerList = ref<{ value: string; label: string }[]>([])


export const fetchTickerList = async (query: string) => {
  try {
    const response = await apiClient.get('/tickers/', { params: { query } })
    return response.data.map((ticker: { Symbol: string; Name: string }) => ({
      value: ticker.Symbol,
      label: ticker.Name
    }))
  } catch (error) {
    console.error('Error fetching tickers:', error)
    return []
  }
}