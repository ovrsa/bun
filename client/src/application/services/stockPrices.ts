import apiClient from './apiAxios'
import { stockPricesState } from '@/types/interfaces'

export const fetchStockPrices = async (
  symbol: string
): Promise<stockPricesState> => {
  try {
    const response = await apiClient.get(`/stock-prices/`, {
      params: { symbol },
    })
    return response.data
  } catch (error) {
    console.error(`Failed to fetch Stock Prices for symbol: ${symbol}`, error)
    throw error
  }
}
