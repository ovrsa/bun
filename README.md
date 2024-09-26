- [JA:](#ja)
  - [概要](#概要)
  - [技術スタック](#技術スタック)
    - [Docker](#docker)
      - [サービス](#サービス)
  - [フロントエンド](#フロントエンド)
    - [技術スタック:](#技術スタック-1)
    - [ライブラリ:](#ライブラリ)
    - [テスト:](#テスト)
  - [バックエンド](#バックエンド)
    - [技術スタック](#技術スタック-2)
    - [ライブラリ:](#ライブラリ-1)
    - [テスト:](#テスト-1)
  - [環境構築](#環境構築)
    - [前提条件](#前提条件)
    - [ローカルでの立ち上げ](#ローカルでの立ち上げ)
- [EN:](#en)
  - [Application Overview](#application-overview)
  - [Tech Stack](#tech-stack)
    - [Docker](#docker-1)
      - [Services](#services)
  - [Frontend](#frontend)
    - [Tech Stack:](#tech-stack-1)
    - [Libraries:](#libraries)
    - [Testing:](#testing)
  - [Backend](#backend)
    - [Tech Stack](#tech-stack-2)
    - [Libraries:](#libraries-1)
    - [Testing:](#testing-1)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Local Setup](#local-setup)

# JA:
## 概要
財務サマリー、企業情報、株価の取得・表示を行うウェブアプリケーション


## 技術スタック
- **Frontend**: TypeScript, Vue 3, Vite, Tailwind CSS
- **Backend**: Python(Django), MySQL

### Docker
- Docker compose 3.8

#### サービス
- **client**: フロントエンド
- **server**: バックエンド
- **db**: MySQLデータベース
- **nginx**:リバースプロキシサーバー

## フロントエンド

### 技術スタック:
- Vue 3 (v3.4.31)

### ライブラリ:
- Vue Router (v4.0.13): ルーティングとナビゲーション
- Vuex (v4.0.2): アプリケーション全体の状態管理
- Axios (v1.6.8): HTTPリクエストを実行
- ESLint & Prettier: コードの一貫性を保つためのリンティングとフォーマッティングツール

### テスト:
- Vitest: 単体テストの実行フレームワーク
- MSW (Mock Service Worker): モック
- Testing Library: UIのテスト

## バックエンド

### 技術スタック
- Django (v4.2): バックエンドフレームワーク
- Django Rest Framework (v3.14.0): RESTful APIの構築
- MySQL (v8.0.30): データストレージ用のデータベース

### ライブラリ:
- gunicorn: プロダクション環境でDjangoアプリを動作させるためのWSGIサーバー
- finnhub-python: Finnhub株式APIとやり取りするためのライブラリ
- django-allauth: ユーザー認証の処理
- django-cors-headers: クロスオリジンリソース共有（CORS）を管理


### テスト:
- pytest: 単体テストの記述と実行
- pytest-django: Django特有のテストを実行
- factory_boy: テストデータの生成
- Faker: テストデータの生成用のフェイクデータライブラリ
- flake8 & black: Pythonコードのリンティングとフォーマッティング


## 環境構築
- DockerおよびDocker Composeがインストール済みであること

### 前提条件
- DockerおよびDocker Composeがインストールされていること

### ローカルでの立ち上げ

1. リポジトリをクローン

2. Docker Composeで環境を立ち上げる
   ```bash
   docker-compose up --build
   ```

# EN:
## Application Overview
A web application for fetching and displaying financial summaries, company information, and stock prices.

## Tech Stack
- **Frontend**: TypeScript, Vue 3, Vite, Tailwind CSS
- **Backend**: Python(Django), MySQL

### Docker
- Docker compose 3.8

#### Services
- **client**: Frontend App
- **server**: Backend App
- **db**: MySQL Database
- **nginx**: Reverse Proxy Server

## Frontend

### Tech Stack:
- Vue 3 (v3.4.31)

### Libraries:
- **Vue Router** (v4.0.13): Routing
- **Vuex** (v4.0.2): State management
- **Axios** (v1.6.8): HTTP client
- **ESLint & Prettier**: Linting and formatting

### Testing:
- **Vitest**: Test runner
- **MSW (Mock Service Worker)**: API mocking tool
- **Testing Library**: UI testing

## Backend

### Tech Stack
- Django (v4.2): Web framework for the backend
- Django Rest Framework (v3.14.0): For building RESTful APIs
- MySQL (v8.0.30): Database for data storage


### Libraries:
- psycopg2-binary: PostgreSQL adapter for Python
- gunicorn: WSGI HTTP Server for running the Django app in production
- finnhub-python: For interacting with the Finnhub stock API
- django-allauth: For handling user authentication
- django-cors-headers: For managing Cross-Origin Resource Sharing (CORS)
- bcrypt: For securely hashing passwords

### Testing:
- pytest: For writing and executing unit tests
- pytest-django: Plugin for running Django-specific tests
- factory_boy: For creating test data
- Faker: For generating fake data in tests
flake8 & black: For linting and formatting Python code

## Setup

### Prerequisites
- Docker and Docker Compose are installed

### Local Setup

1. Clone the repository

2. Start the environment with Docker Compose
   ```bash
   docker-compose up --build
   ```