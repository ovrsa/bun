# ディレクトリ構造の概要

```plaintext
├── index.html                # アプリのエントリポイント
├── package-lock.json         # 依存関係のロックファイル
├── package.json              # プロジェクトの依存関係とスクリプト
├── src
│   ├── App.vue
│   ├── main.ts               # アプリのエントリポイント
│   ├── assets                # 静的アセット (CSSや画像)
│   ├── components            # UIコンポーネント
│   │   ├── ui                # UIライブラリ
│   │   ├── atoms             # 基本要素 (ボタン、入力フィールドなど)
│   │   ├── molecules         # Atomとuiを組み合わせたもの (フォームなど)
│   │   ├── organisms         # セクション
│   │   └── templates         # ページのテンプレート
│   ├── pages                 # ページビュー
│   ├── hooks                 # カスタムフック
│   ├── services              # サービス層
│   ├── router                # ルーティング設定
│   ├── store                 # 状態管理層 (Vuex)
│   ├── types                 # 型定義
│   ├── utils                 # ユーティリティ関数
│   └── vite-env.d.ts         # Viteの環境変数定義
├── Dockerfile
├── test                      # テスト関連
├── mocks                     # モックデータ
├── public                    # 公開用ファイル
├── config                    # 設定ファイル
│   ├── components.json       # コンポーネント設定
│   ├── eslint.config.cjs     # ESLintの設定
│   ├── postcss.config.js     # PostCSSの設定
│   └── tsconfig.json         # TypeScriptの設定
├── tailwind.config.js        # Tailwind CSSの設定
├── tsconfig.node.json        # Node用のTypeScript設定
└── vite.config.ts            # Viteの設定
```
# テストの実行
1. UTの実行
``````
npx vitest