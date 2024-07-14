class User < ApplicationRecord
    has_many :user_categories
    has_many :categories, through: :user_categories
    has_many :user_items, through: :user_categories
    has_many :items, through: :user_items
end
