# 1. Directory Structure

```
custom_auth
├── README.md                                      
├── __init__.py                                    
├── __pycache__                                    
├── admin.py                                       # Django管理画面での設定
├── apps.py                                        # 認証アプリケーションの設定
├── authentication.py                              # JWT認証ロジックを含むカスタム認証クラス
├── migrations                                     
│   ├── 0001_initial.py                            
│   └── __init__.py                                
├── models.py                                      # メール認証用のトークンモデル
├── serializers.py                                 # 認証用シリアライザー（ログイン・ユーザー登録）
├── tests.py                                       
├── urls.py                                        # URLルーティング設定
└── views.py                                       # 認証に関するビューロジック
```