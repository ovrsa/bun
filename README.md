# Bun

## 概要
株価チャート

## 使用技術

### Infrastructure
- Docker
- Docker Compose : 3.8

### Frontend
- vite: 5.2.0
- vue: 3.4.21
- typescript: 5.2.2
- axios: 1.6.8
- pinia: 2.1.7
- postcss: 8.4.38
- tailwindcss: 3.4.3
- vue-router: 4.0.13
- vuex: 4.0.2

### Backend
- Ruby: 3.1.5
- rails: 7.1.3
- devise: 4.9.4
- jwt: 2.1.1
- bcrypt: 3.1.18
- pry: 0.14.1
- rspec: 3.12.0
- factory_bot: 6.2.1

## 環境構築

### 前提条件
- DockerおよびDocker Composeがインストールされていること

### ローカルでの立ち上げ

1. リポジトリをクローン

2.	Docker Composeで環境を立ち上げる
```bash
docker-compose up --build
```
以下のURLでアプリケーションにアクセスできる

    • フロントエンド: http://localhost:5173
    • バックエンドAPI: http://localhost:3000
    • データベースはPostgreSQLがlocalhost:5432で動作

## コンテナの内容

### db

    • イメージ: postgres:13
    • 環境変数:
    • POSTGRES_USER=postgres
    • POSTGRES_PASSWORD=password
    • POSTGRES_DB=app_development
    • ボリューム:
    • db-data:/var/lib/postgresql/data

### web

    • ビルドコンテキスト: ./server
    • コマンド: bash -c "./wait-for-it.sh db:5432 -- rm -f tmp/pids/server.pid && bundle exec rails s -b '0.0.0.0'"
    • ボリューム:
    • ./server:/rails
    • ./wait-for-it.sh:/wait-for-it.sh
    • ポート: 3000:3000
    • 依存関係: db
    • 環境変数:
    • DATABASE_URL=postgres://postgres:password@db:5432/app_development
    • RAILS_ENV=development

### client

    • ビルドコンテキスト: ./client
    • コマンド: /bin/sh -c "npm install && npm run dev -- --host 0.0.0.0"
    • ボリューム:
    • ./client:/usr/src/app
    • ポート: 5173:5173 