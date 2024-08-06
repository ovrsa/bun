## 概要
株価チャート

## インフラストラクチャー

### Docker
- **Docker Composeバージョン**: 3.8

#### サービス
- **client**: フロントエンド
- **server**: Railsアプリケーション
- **db**: PostgreSQLデータベース
- **nginx**: リバースプロキシサーバー

#### ボリューム
- **db-data**: データベースデータの永続化

#### ネットワーク
- **bun_app_network**: ブリッジネットワーク

## フロントエンド

### 技術スタック
- **Vue 3** (v3.4.31)
- **Vite** (v5.2.0)
- **Tailwind CSS**
- **Typescript**

### ライブラリ
- **Vue Router** (v4.0.13)
- **Pinia** (v2.1.7)
- **Axios** (v1.6.8)
- **D3** (v7.9.0)
- **ESLint & Prettier**

### フロントエンドテスト
- **Vitest**
- **MSW (Mock Service Worker)**
- **Testing Library**

## バックエンド

### 技術スタック
- **Ruby on Rails 7** (>= 7.1.3.2)
- **PostgreSQL**

### 主要なGem
- **Devise**
- **pg**
- **Puma**
- **RuboCop**
- **BCrypt** (v3.1.7)

### 開発・テスト環境用Gem
- **RSpec-rails** (~> 6.0.0)
- **Faker**
- **FactoryBot Rails**

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

    フロントエンド: http://localhost:5173
    バックエンドAPI: http://localhost:3000
    データベースはPostgreSQLがlocalhost:5432で動作