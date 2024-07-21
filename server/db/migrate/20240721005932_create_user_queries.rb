class CreateUserQueries < ActiveRecord::Migration[7.1]
  def change
    create_table :user_queries do |t|
      t.references :user, null: false, foreign_key: true
      t.text :query

      t.timestamps
    end
  end
end
