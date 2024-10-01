import apiClient from './apiAxios';

interface Financial {
  fiscal_year: number;
  total_revenue: number | null;
  normalized_ebitda: number | null;
  stockholders_equity: number | null;
  free_cash_flow: number | null;
  capital_expenditures: number | null;
  total_assets: number | null;
  total_liabilities: number | null;
  gross_profit: number | null;
  net_income_loss: number | null;
  operating_expenses: number | null;
  created_at: string;
}

interface CompanyFinancials {
  ticker: string;
  start_year: number | null;
  end_year: number | null;
  total: number;
  financials: Financial[];
}

export const fetchCompanyFinancials = async (symbol: string): Promise<CompanyFinancials> => {
  try {
    const response = await apiClient.get(`/company-financials/`, {
      params: { symbol },
    });
    console.log(`Fetched company financials for symbol: ${symbol}`, response.data);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch company financials for symbol: ${symbol}`, error);
    throw error;
  }
};
