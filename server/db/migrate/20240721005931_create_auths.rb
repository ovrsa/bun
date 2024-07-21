class CreateAuths < ActiveRecord::Migration[7.1]
  def change
    create_table :auths do |t|
      t.references :user, null: false, foreign_key: true
      t.datetime :refresh_token_expires_at
      t.datetime :access_token_expires_at
      t.string :refresh_token
      t.string :access_token

      t.timestamps
    end
  end
end
