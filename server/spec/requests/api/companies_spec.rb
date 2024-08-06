require 'rails_helper'

RSpec.describe "Api::V1::Companies", type: :request do
  describe "GET /api/v1/companies/:id" do
    let(:user) { FactoryBot.create(:user) }
    let(:company) do
      FactoryBot.create(:company, 
        name: "TestCo",
        sector: "Tech",
        industry: "Software",
        city: "Tokyo",
        country: "Japan",
        website: "https://testco.com",
        description: "A leading tech company"
      )
    end

    before do
      sign_in user
      allow_any_instance_of(Api::V1::CompaniesController).to receive(:authenticate_user!).and_return(true)
      get api_v1_company_path(company), headers: { "Host" => "localhost" }
    end

    it "returns the company information" do
      expect(response).to have_http_status(200)
      data = JSON.parse(response.body)
      expect(data['name']).to eq("TestCo")
      expect(data['sector']).to eq("Tech")
      expect(data['industry']).to eq("Software")
      expect(data['city']).to eq("Tokyo")
      expect(data['country']).to eq("Japan")
      expect(data['website']).to eq("https://testco.com")
      expect(data['description']).to eq("A leading tech company")
    end
  end
end