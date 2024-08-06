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
- **Vue 3** (v3.4.31): プログレッシブフレームワーク
- **Vite** (v5.2.0): 高速フロントエンドビルドツール
- **Tailwind CSS**: 効率的なスタイルシート作成
- **Typescript**: 静的型付けを提供

### ライブラリ
- **Vue Router** (v4.0.13): ルーティング管理
- **Pinia** (v2.1.7): 状態管理
- **Axios** (v1.6.8): HTTPリクエスト
- **D3** (v7.9.0): データ視覚化
- **ESLint & Prettier**: コードの品質とフォーマット

### テストツール
- **Vitest**: テストランナー
- **MSW (Mock Service Worker)**: APIモックツール
- **Testing Library**: ユーザインターフェースのテスト

## バックエンド

### 技術スタック
- **Ruby on Rails 7** (>= 7.1.3.2)
- **PostgreSQL**

### 主要なGem
- **Devise**: 認証システム
- **pg**: PostgreSQLアダプタ
- **Puma**: HTTPサーバー
- **RuboCop**: コーディング規約
- **BCrypt** (v3.1.7): パスワードハッシュ化

### 開発・テスト環境用Gem
- **RSpec-rails** (~> 6.0.0): テストフレームワーク
- **Faker**: ダミーデータ生成
- **FactoryBot Rails**: テストデータセットアップ

## 環境構築

### 前提条件
- DockerおよびDocker Composeがインストールされていること

### ローカルでの立ち上げ

1. リポジトリをクローン

2. Docker Composeで環境を立ち上げる
   ```bash
   docker-compose up --build