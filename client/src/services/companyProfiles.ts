import { CompanyProfile } from '@/types/interfaces'
import apiClient from './apiAxios'

export const fetchCompanyProfile = async (
  symbol: string
): Promise<CompanyProfile> => {
  try {
    const response = await apiClient.get(import.meta.env.VITE_API_COMPANY_PROFILES, {
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
