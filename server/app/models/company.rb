class Company < ApplicationRecord
  validates :name, :sector, :industry, presence: true
end