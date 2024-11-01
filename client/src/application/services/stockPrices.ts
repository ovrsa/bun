import apiClient from './apiAxios'

interface stockPrices {
  date: string
  close: number
  high: number
  low: number
  moving_average_20: number
  moving_average_50: number
  moving_average_200: number
  rsi: number
  volume: number
}

export const fetchStockPrices = async (
  symbol: string
): Promise<stockPrices> => {
  try {
    const response = await apiClient.get(`/stock-prices/`, {
      params: { symbol },
    })
    console.log(`Fetched Stock Prices for symbol: ${symbol}`, response.data)
    return response.data
  } catch (error) {
    console.error(`Failed to fetch Stock Prices for symbol: ${symbol}`, error)
    throw error
  }
}
