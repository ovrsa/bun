# accounts アプリケーション

このアプリケーションは、認証とユーザー管理を担当します。

## 主な構成
- `domain`: ユーザーモデルや認証関連のビジネスロジックを定義します。
- `application`: ユーザー登録、ログインなどのユースケースを管理します。
- `infrastructure`: データベースアクセスや外部サービス（例: メール送信）との連携を行います。
- `presentation`: シリアライザーやビュー、エンドポイントを提供します。

## 主な機能
- JWT認証
- ユーザー登録とログイン
- パスワードリセットやメール検証