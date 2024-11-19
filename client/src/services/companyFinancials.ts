import { CompanyFinancials } from '@/types/interfaces'
import apiClient from './apiAxios'

export const fetchCompanyFinancials = async (
  symbol: string
): Promise<CompanyFinancials> => {
  try {
    const response = await apiClient.get(import.meta.env.VITE_API_COMPANY_FINANCIALS, {
      params: { symbol },
    })
    return response.data
  } catch (error) {
    console.error(
      `Failed to fetch company financials for symbol: ${symbol}`,
      error
    )
    throw error
  }
}
