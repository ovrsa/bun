## 概要 
会社名を入力すると、以下の情報を計算し画面に表示します：
- 株価情報：時系列の株価推移
- 会社情報：事業内容や基本データ
- 財務情報：過去の業績や財務指標


## 機能紹介
- 株価チャート描画
  - 対象期間を選択可能なインタラクティブチャートで株価を視覚的に表示。
- 会社情報表示
  - 事業概要や基本的な会社データを出力。
- 財務情報の表示
  - 過去5年分の業績や財務指標を一覧で確認可能。


## 使用画面
![action](https://github.com/user-attachments/assets/686bfb97-2aa9-48a9-881b-9c8587867bc5)
| Login | Signup | Home/Chart | Home/Summary
| :---: | :---: | :---: | :---: |
| ![Login](https://github.com/user-attachments/assets/81688793-7fea-47c8-b6ef-ae0b8aa954b7) | ![Signup](https://github.com/user-attachments/assets/7d675c24-1bb9-46e9-92c2-93432d0d9c30) | ![Home](https://github.com/user-attachments/assets/33e35d7d-64ab-4fda-99de-7d0c6945a7bc) |![Home](https://github.com/user-attachments/assets/c209a374-05ac-4271-805e-8430844097f3) |
| Loginを実施 | Signupを実施 | 株価グラフ表示 | 会社情報,財務情報表示 |

## URL
https://bunapp.top/

test account: 
- email: test@test.com
- password: test

## Architecture
![Architecture](https://github.com/user-attachments/assets/c35fff82-dd67-44fb-8888-420b5cd0e74c)

## 使用技術
### Infrastructure
- Docker
- Docker Compose

### Frontend
- **Vite**: ^5.1.4
- **Vitest**: ^2.1.5
- **Axios**: ^1.6.8
- **Pinia**: ^2.1.7
- **Vue**: ^3.4.31
- **Vue Router**: ^4.0.13
- **Vuex**: ^4.0.2
- **MSW**: ^1.2.1
- **ESLint**: ^8.57.0
- **Tailwind CSS**: ^3.4.4
- **TypeScript**: ^5.5.3
- **Prettier**: ^3.3.3

### Backend
- **Django**: >=4.2,<5.0
- **Psycopg2-binary**: >=2.9.7
- **Gunicorn**: >=20.1.0
- **Django Allauth**: >=0.54.0
- **Django CORS Headers**: >=3.13.0
- **Django REST Framework**: >=3.14.0
- **Flake8**: >=6.1.0
- **Black**: >=23.9.1
- **MySQLclient**: >=2.1
- **Requests Cache**: >=0.7.4
- **Python Dotenv**: ==1.0.0
- **yfinance**: >= 0.2.0

# 環境構築
- DockerおよびDocker Composeがインストール済みであること

## 前提条件
- DockerおよびDocker Composeがインストールされていること

## ローカルでの立ち上げ

1. リポジトリをクローン

2. Docker Composeで環境を立ち上げる
   ```bash
   docker-compose up --build
   ```
