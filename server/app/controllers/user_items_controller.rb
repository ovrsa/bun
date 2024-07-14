class UserItemsController < ApplicationController
    def index
        @user_items = UserItem.all
        render json: @user_items
    end

    def create
        @user_item = UserItem.new(user_item_params)
        if @user_item.save
            render json: @user_item, status: :created
        else
            render json: @user_item.errors, status: :unprocessable_entity
        end
    end

    private

    def user_item_params
        params.require(:user_item).permit(:user_id, :user_category_id, :item_id)
    end
end
