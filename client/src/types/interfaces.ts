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
