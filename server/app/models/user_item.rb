class UserItem < ApplicationRecord
  belongs_to :user
  belongs_to :item
  belongs_to :user_category
end
