class CreateCompanies < ActiveRecord::Migration[7.1]
  def change
    create_table :companies do |t|
      t.string :name
      t.string :sector
      t.string :industry
      t.string :city
      t.string :country
      t.string :website
      t.text :description

      t.timestamps
    end
  end
end
