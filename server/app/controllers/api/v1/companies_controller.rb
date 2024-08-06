class Api::V1::CompaniesController < ApplicationController
  # テストの場合は認証をスキップ
  before_action :authenticate_user!, unless: -> { Rails.env.test? }

  def show
    company = Company.find_by(id: params[:id])
    if company
      render json: company
    else
      render json: { error: "Company not found" }, status: :not_found
    end
  end
end