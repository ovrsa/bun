import apiClient from './apiAxios'

interface CompanyProfile {
  company_name: string
  exchange: string
  market_category: string
  industry: string
  sector: string
  address: string
  phone_number: string
  website: string
  founding_year: number
  employee_count: number
  outstanding_shares: number
  market_capitalization: number
  average_trading_volume_10d: number
  business_description: string
}

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
