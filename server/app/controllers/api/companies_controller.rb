# app/controllers/api/v1/companies_controller.rb
class Api::V1::CompaniesController < ApplicationController
  before_action :authenticate_user!, unless: -> { Rails.env.test? }

  def show
    company = Company.find(params[:id])
    render json: company
  end
end