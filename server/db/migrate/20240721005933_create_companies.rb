class CreateCompanies < ActiveRecord::Migration[7.1]
  def change
    create_table :companies do |t|
      t.text :description
      t.string :name
      t.string :ticker
      t.string :sector
      t.string :industry

      t.timestamps
    end
  end
end
