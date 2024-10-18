import apiClient from './apiAxios';

interface Financial {
  fiscal_year: number;
  total_revenue: number;
  normalized_ebitda: number;
  stockholders_equity: number;
  free_cash_flow: number;
  capital_expenditures: number;
  total_assets: number;
  total_liabilities: number;
  gross_profit: number;
  net_income_loss: number;
  net_debt: number;
  enterprise_value: number;
  ebitda_margin: number;
  net_debt_to_ebitda: number;
  roa: number;
  roe: number;
  debt_to_equity: number;
  operating_margin: number;
  cash_from_operations: number;
  change_in_working_capital: number;
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
    // console.log(`Fetched company financials for symbol: ${symbol}`, response.data);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch company financials for symbol: ${symbol}`, error);
    throw error;
  }
};
