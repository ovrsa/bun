class UsersController < ApplicationController
    def index
      @users = User.includes(user_categories: [:category, { user_items: :item }]).all
      render json: @users.as_json(include: {
        user_categories: {
          include: {
            category: { only: [:id, :categoryName] },
            user_items: { include: { item: { only: [:id, :itemName] } } }
          }
        }
      })
    end
  
    def create
      @user = User.new(user_params)
      if @user.save
        render json: @user, status: :created
      else
        render json: @user.errors, status: :unprocessable_entity
      end
    end
  
    private
  
    def user_params
      params.require(:user).permit(:userName, :userIcon)
    end
  end