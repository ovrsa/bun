import apiClient from './apiAxios'
import { CompanyFinancials } from '@/types/interfaces'

export const fetchCompanyFinancials = async (
  symbol: string
): Promise<CompanyFinancials> => {
  try {
    const response = await apiClient.get(`/company-financials/`, {
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
