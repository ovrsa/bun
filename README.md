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
![action](https://private-user-images.githubusercontent.com/92124533/388294560-6ff112a1-0898-499b-adda-a4e0e57a841b.GIF?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzIxNDQ4MDQsIm5iZiI6MTczMjE0NDUwNCwicGF0aCI6Ii85MjEyNDUzMy8zODgyOTQ1NjAtNmZmMTEyYTEtMDg5OC00OTliLWFkZGEtYTRlMGU1N2E4NDFiLkdJRj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTIwVDIzMTUwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTcwNjUyYjMxM2E0MzU4MzQwOGIwMzNhZGI0YWE4YjZhNTEzMGNiMDJlYjA1ODcxMjAzM2E2NTgzN2VjM2FjYjEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.hrvloW8gGFpYHutZCmSA2BCexWnbzAaHp2kF7fYxH24)
| Login | Signup | Home/Chart | Home/Summary
| :---: | :---: | :---: | :---: |
| ![Login](https://private-user-images.githubusercontent.com/92124533/388294263-7dd748a2-755c-4037-a462-d762692f3b3c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzIxNDQ4MDYsIm5iZiI6MTczMjE0NDUwNiwicGF0aCI6Ii85MjEyNDUzMy8zODgyOTQyNjMtN2RkNzQ4YTItNzU1Yy00MDM3LWE0NjItZDc2MjY5MmYzYjNjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTIwVDIzMTUwNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTVkMWI2ODllZWViZGQ0YjVkZTVkMjg1N2Q5YTQ3ZWRhZTdmOTgxYzU3OWU1OGRhNzZiODc0MGVjYWIxNjhkZmEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.cVUVTi1YYmDLeLxtxMJW_byx4u0FbmLL_zASWj6uTyc) | ![Signup](https://private-user-images.githubusercontent.com/92124533/388294590-7d675c24-1bb9-46e9-92c2-93432d0d9c30.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzIxNDQ4MDQsIm5iZiI6MTczMjE0NDUwNCwicGF0aCI6Ii85MjEyNDUzMy8zODgyOTQ1OTAtN2Q2NzVjMjQtMWJiOS00NmU5LTkyYzItOTM0MzJkMGQ5YzMwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTIwVDIzMTUwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWViMDBmNmU0YTY3NzgxNTQzNGQzMDllNjYwMTk0YzM5N2ZhNGY2ZTI3MDM4ODkwYzA4MjM1NDBjY2JhNmQ0MzMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.d0dC5cCjAXOp2yHJdygR557P1_L4kUYBQUHEwUGjThQ) | ![Home](https://private-user-images.githubusercontent.com/92124533/388294237-af362a85-9d05-40c6-86b1-1d1974cc9656.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzIxNDQ4MDYsIm5iZiI6MTczMjE0NDUwNiwicGF0aCI6Ii85MjEyNDUzMy8zODgyOTQyMzctYWYzNjJhODUtOWQwNS00MGM2LTg2YjEtMWQxOTc0Y2M5NjU2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTIwVDIzMTUwNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTQ2MjI4MWZmMTFkNmI3ZTMwN2QzOTJkNGZlOGU3NWVjZTU3N2JlYTk3ODQxMTJkNjFiMmU3MDBjM2U5YTQ5NWImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.-vJcgXpeY-XxXeQiQOuSjO8qAWkQh-Pa0jq-UlDqziE) |![Home](https://private-user-images.githubusercontent.com/92124533/388295063-dfc0e890-02e6-4236-8015-34961f5da134.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzIxNDQ5NjUsIm5iZiI6MTczMjE0NDY2NSwicGF0aCI6Ii85MjEyNDUzMy8zODgyOTUwNjMtZGZjMGU4OTAtMDJlNi00MjM2LTgwMTUtMzQ5NjFmNWRhMTM0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTIwVDIzMTc0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWI5MTQ2NGFjMjAyNGJkZWZlMWMwZWU5MDk1MWU0ZGE4YTcyMTcyNjMzNWI3NzI3ZjhhM2ZlZjFlMjA2MWZmYzQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.dpq-JMbbndChh3IdndeLySPZ6u4uSv_5ZTXKLtycBHo) |
| Loginを実施 | Signupを実施 | 株価グラフ表示 | 会社情報,財務情報表示 |

## Architecture
![Architecture](https://private-user-images.githubusercontent.com/92124533/388294120-07c9f7b0-73d8-420b-aadc-96192cb634b9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzIxNDQ5NjYsIm5iZiI6MTczMjE0NDY2NiwicGF0aCI6Ii85MjEyNDUzMy8zODgyOTQxMjAtMDdjOWY3YjAtNzNkOC00MjBiLWFhZGMtOTYxOTJjYjYzNGI5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTIwVDIzMTc0NlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTJkYzk1ZmI3ZTE1NWE0NTBmZDg0MDgxZGViZTdjM2ZlODlhNTdmMWE5MGZjYzJjNGRiNGU4ODBkNTAwNWZhNjcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.bNKJc1J3y7OlFtnX3Ot-HorgOSgfC43WfbQeTZshGd4)

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
