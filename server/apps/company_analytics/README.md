# company_analytics

株式情報（企業プロフィール、株価、財務データ）を管理します。

## ディレクトリ構成
```
server/apps/company_info/
├── Application
│   ├── __init__.py               # ユースケース層の初期化ファイル
│   ├── interfaces.py             # 外部サービスインターフェースの定義
│   └── use_cases.py              # ユースケースの実装
├── Domain
│   ├── __init__.py               # ドメイン層の初期化ファイル
│   ├── models.py                 # ドメインモデル
│   └── services.py               # ドメインサービス
├── Infrastructure
│   ├── __init__.py               # インフラ層の初期化ファイル
│   └── external_services.py      # 外部サービス実装（例: YFinance）
├── Presentation
│   ├── __init__.py               # プレゼンテーション層の初期化ファイル
│   ├── serializers.py            # シリアライザー
│   ├── urls.py                   # ルーティング
│   └── views.py                  # ビューセット
├── README.md                     # このドキュメント
├── __init__.py                   # アプリケーションの初期化ファイル
├── admin.py                      # Django 管理画面用設定
├── apps.py                       # Django アプリケーション設定
├── exception
│   ├── __init__.py               # 例外処理層の初期化ファイル
│   └── handlers.py               # カスタム例外ハンドラー
└── migrations/                   # データベースマイグレーションファイル
```

## アーキテクチャ構成

### **1. Domain**

- 責務: アプリケーションの中心的なビジネスルールやデータモデルを管理。

主な内容:
- ドメインモデル (models.py) - データ構造を定義。
- ドメインサービス (services.py) - ビジネスロジックを実装。

### **2. Application**

責務: ビジネスロジックを実行し、他の層とのやり取りを仲介。

主な内容:
- ユースケース (use_cases.py) - 各操作のフローを管理。
- インターフェース (interfaces.py) - 外部サービスと連携するための抽象定義。


### **3. Infrastructure**

責務: 外部サービスやデータベースアクセスに関する具体的な実装。

主な内容:
- 外部APIとの連携 (external_services.py) - 例: YFinance を使用。


### **4. Presentation**

責務: クライアントとのインターフェースを提供。

主な内容:
- ビューセット (views.py) - APIエンドポイント。
- シリアライザー (serializers.py) - 入出力データの整形。


## 主な機能

1. 企業情報の取得

- 外部APIから会社概要を取得し、データベースに保存。
- 必要に応じてキャッシュを使用。
- 株価情報の取得

2. 指定したティッカーの株価履歴を取得。
- 移動平均線やRSIの計算も含む。

3. 財務情報の取得
- バランスシート、キャッシュフロー、損益計算書から主要指標を抽出。

## 外部プロバイダーの追加
このモジュールは、複数の外部プロバイダーを利用可能です。

プロバイダーを追加するには、以下の手順を実施してください。

1. インターフェースの実装

- Application/interfaces.py 内の該当インターフェースを実装。
- 例: CompanyProfileFetcher, StockPriceFetcher, CompanyFinancialsFetcher。

2. 新しいプロバイダーを追加

- Infrastructure/external_services.py にクラスを追加。
- 必要に応じて、初期化処理やエラーハンドリングを実装。

3. ユースケースでの利用

- Application/use_cases.py に新しいプロバイダーを組み込む。
- ユースケースの切り替えが簡単にできるよう、プロバイダーを引数で渡す設計にする。

## 使用例
APIエンドポイント
- GET /api/company-profiles/?symbol=AAPL
  - 企業情報を取得

- GET /api/stock-prices/?symbol=GOOGL
  - 株価情報を取得。

- GET /api/company-financials/?symbol=MSFT
  - 財務情報を取得。

## 貢献

1. Issue を立て、変更内容を提案。
2. フォークして、修正を加えたブランチを作成。
3. プルリクエストを送信。
