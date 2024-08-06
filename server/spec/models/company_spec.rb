require 'rails_helper'

RSpec.describe Company, type: :model do
  # 有効な属性値の場合
  it 'is valid with valid attributes' do
    company = Company.new(name: 'Test Company', sector: 'Tech', industry: 'Software', city: 'Tokyo', country: 'Japan', website: 'http://test.com', description: 'A test company')
    expect(company).to be_valid
  end

  # 無効な属性値の場合
  it 'is not valid without a name' do
    company = Company.new(name: nil)
    expect(company).not_to be_valid
  end

  it 'is not valid without a sector' do
    company = Company.new(sector: nil)
    expect(company).not_to be_valid
  end

  it 'is not valid without an industry' do
    company = Company.new(industry: nil)
    expect(company).not_to be_valid
  end
end