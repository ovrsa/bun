class CreateFinancialSummaries < ActiveRecord::Migration[7.1]
  def change
    create_table :financial_summaries do |t|
      t.references :company, null: false, foreign_key: true
      t.integer :fiscal_year
      t.decimal :revenue
      t.decimal :net_income
      t.decimal :assets
      t.decimal :liabilities

      t.timestamps
    end
  end
end
