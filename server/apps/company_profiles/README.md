# 1. Directory Structure

```company_profiles
├── README.md                                      
├── __init__.py                                    
├── __pycache__                                    
├── admin.py                                       
├── apps.py                                        
├── migrations                                     
│   ├── 0001_initial.py                            
│   └── __init__.py                                
├── models.py                                      # データベースのモデル定義
├── services/                                      # ドメインロジックや外部APIの処理を行うサービス
│   ├── client_initializer.py                      # クライアント初期化に関するロジック
│   ├── company_profile_repository.py              # 企業情報に関するリポジトリ
│   ├── company_profile_validator.py               # Responseデータの適正を確認するバリデーションロジック
│   ├── finnhub_api_service.py                     # Finnhub APIとの通信を行うサービス
│   └── finnhub_service.py                         # Finnhubに関するビジネスロジック
├── tests/                                         
│   ├── test_company_profile.py                    # 会社プロフィールに関するユニットテスト
│   └── test_finnhub_service.py                    # Finnhubサービスに関するユニットテスト
├── urls.py                                        # URLのルーティング
└── views.py                                       # リクエストに対するレスポンスの処理（ビュー）
```