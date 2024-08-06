class HomeController < ApplicationController
  def index
    render json: { message: "Welcome to the Bun API" }
  end
end
