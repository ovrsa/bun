export interface Category {
  id: string
  categoryName: string
}

export interface Item {
  id: string
  itemName: string
}

export interface UserItem {
  id: string
  item: Item
}

export interface UserCategory {
  id: string
  category: Category
  user_items: UserItem[]
}

export interface User {
  id: string
  userName: string
  userIcon: string
  created_at: string
  updated_at: string
  user_categories: UserCategory[]
}

export interface ButtonProps {
  type?: 'button' | 'submit' | 'reset'
  onClick?: () => void
}

export interface StockEntry {
  date: string
  close: number
  high: number
  low: number
  moving_average_20?: number
  moving_average_50?: number
  moving_average_200?: number
  volume: number
}

export interface Financial {
  fiscal_year: number
  total_revenue: number | null
  normalized_ebitda: number | null
  stockholders_equity: number | null
  free_cash_flow: number | null
  capital_expenditures: number | null
  total_assets: number | null
  total_liabilities: number | null
  gross_profit: number | null
  net_income_loss: number | null
  operating_expenses: number | null
  created_at: string
}

export interface CompanyFinancials {
  ticker: string
  start_year: number | null
  end_year: number | null
  total: number
  financials: Financial[]
}

export interface CompanyFinancialsState {
  data: CompanyFinancials | null
  loading: boolean
  error: string | null
}

export interface CompanyProfile {
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

export interface CompanyProfileState {
  profile: CompanyProfile | null
  loading: boolean
  error: string | null
}

export interface stockPricesState {
  data: stockPricesState[] | null
  loading: boolean
  error: string | null
}

export interface SymbolState {
  selectedSymbol: string | null
}

export interface AuthState {
  token: string | null
  error: string | null
}

export interface AuthState {
  isAuthenticated: boolean | null
}

export interface TickerState {
  tickerList: { Symbol: string; Name: string }[]
  selectedTicker: string
  searchTerm: string
}