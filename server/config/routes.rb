Rails.application.routes.draw do
  root to: 'home#index'

  get 'home/index'
  devise_for :users

  get "up" => "rails/health#show", as: :rails_health_check

  namespace :api do
    namespace :v1 do
      get 'companies/index'
      get 'companies/show'
      get 'companies/create'
      get 'companies/update'
      get 'companies/destroy'
      resources :companies, only: [:index, :show, :create, :update, :destroy]
    end
  end

end
