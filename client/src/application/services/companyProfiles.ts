import apiClient from './apiAxios'
import { CompanyProfile } from '@/types/interfaces'

export const fetchCompanyProfile = async (
  symbol: string
): Promise<CompanyProfile> => {
  try {
    const response = await apiClient.get(`/company-profiles/`, {
      params: { symbol },
    })
    return response.data
  } catch (error) {
    console.error(
      `Failed to fetch company profile for symbol: ${symbol}`,
      error
    )
    throw error
  }
}
