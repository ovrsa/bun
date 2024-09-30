import apiClient from './apiAxios';

interface CompanyProfile {
  company_name: string;
  ticker: string;
  country: string;
  currency: string;
  exchange: string;
  ipo_date: string;
  market_capitalization: number;
  phone: string;
  share_outstanding: number;
  website_url: string;
  logo_url: string;
  finnhub_industry: string;
}

export const fetchCompanyProfile = async (symbol: string): Promise<CompanyProfile> => {
  try {
    const response = await apiClient.get(`/company-profile/`, {
      params: { symbol },
    });
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch company profile for symbol: ${symbol}`, error);
    throw error;
  }
};
