class UserCategoriesController < ApplicationController
    def index
        @user_categories = UserCategory.all
        render json: @user_categories
    end

    def create
        @user_category = UserCategory.new(user_category_params)
        if @user_category.save
            render json: @user_category, status: :created
        else
            render json: @user_category.errors, status: :unprocessable_entity
        end
    end

    private

    def user_category_params
        params.require(:user_category).permit(:user_id, :category_id)
    end
end