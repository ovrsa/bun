# ディレクトリ構造の概要

```plaintext
src/
├── application/          # ビジネスロジック層
│   ├── services/         # API 呼び出しやサーバーとの通信処理
│   │   ├── apiAxios.ts
│   │   ├── authService.ts
│   │   └── stockPricesService.ts
│   └── useCases/         # ユースケース層 (アプリケーションの機能の流れを定義)
│       └── fetchStockPrices.ts
├── assets/               # 静的アセット (CSSや画像など)
│   └── global.css
├── components/           # UIコンポーネント
│   ├── atoms/            # 基本要素 (ボタン、入力フィールドなど)
│   ├── molecules/        # 複数のAtomを組み合わせたもの (フォームなど)
│   ├── organisms/        # 複雑なUI要素 (ナビゲーションバーなど)
│   ├── templates/        # ページのテンプレート
│   └── ui/               # 汎用的なUIコンポーネント
├── store/                # 状態管理層 (Vuex)
│   ├── auth/             # 認証関連の状態管理
│   │   └── index.ts
│   ├── companyFinancials/ # 企業財務データの管理
│   │   └── index.ts
│   └── stockPrices/      # 株価データの管理
│       └── index.ts
├── router/               # ルーティング設定
│   └── index.ts
├── views/                # ページビュー
│   ├── 404.vue
│   ├── Home.vue
│   ├── Login.vue
│   └── Signup.vue
└── main.ts               # エントリーポイント
```

## ディレクトリ構造の詳細
1. application/ – ビジネスロジック層<br>
API通信やユースケース（アプリケーションの具体的な機能）を実装<br>
services/: API 呼び出しや認証など、再利用可能なロジックを定義<br>
useCases/: アプリケーションのユースケース（例: 株価データの取得）を実装。ビジネスロジックのフローをまとめることで、可読性と再利用性が向上させる。

2. assets/ – 静的アセット<br>
CSSや画像ファイルなど、変更されない静的なファイルを格納。

3. components/ – UIコンポーネント (Atomic Design)<br>
UIコンポーネントは Atomic Design に基づいて構成。

4. store/ – 状態管理層<br>
Vuexで状態を管理。
auth/: 認証の状態を管理。<br>
companyFinancials/: 企業の財務データを管理。
stockPrices/: 株価データの状態を管理。

5. router/ – ルーティング設定<br>
Vue Routerを使ったルート定義。

6. views/ – ページビュー<br>
各ページのビューコンポーネントが含まれる。
ルートごとに対応するページ全体を構築。

7. main.ts – エントリーポイント<br>
アプリケーションのエントリーポイント。