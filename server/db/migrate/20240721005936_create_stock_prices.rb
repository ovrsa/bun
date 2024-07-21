class CreateStockPrices < ActiveRecord::Migration[7.1]
  def change
    create_table :stock_prices do |t|
      t.references :company, null: false, foreign_key: true
      t.datetime :date
      t.decimal :open_price
      t.decimal :close_price
      t.decimal :high_price
      t.decimal :low_price
      t.integer :volume

      t.timestamps
    end
  end
end
