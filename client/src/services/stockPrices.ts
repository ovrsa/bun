import { stockPricesState } from '@/types/interfaces'
import apiClient from './apiAxios'

export const fetchStockPrices = async (
  symbol: string
): Promise<stockPricesState> => {
  try {
    const response = await apiClient.get(import.meta.env.VITE_API_STOCK_PRICES, {
      params: { symbol },
    })
    return response.data
  } catch (error) {
    console.error(`Failed to fetch Stock Prices for symbol: ${symbol}`, error)
    throw error
  }
}
