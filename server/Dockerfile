# syntax=docker/dockerfile:1

# ベースイメージを設定
ARG RUBY_VERSION=3.1.5
FROM ruby:$RUBY_VERSION-slim

# 作業ディレクトリを設定
WORKDIR /rails

# 必要なパッケージをインストールする
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y \
    build-essential \
    git \
    libpq-dev \
    libvips \
    pkg-config \
    libssl-dev \
    zlib1g-dev \
    libsqlite3-dev \
    libreadline-dev \
    curl \
    postgresql-client \
    libxml2-dev \
    libxslt1-dev && \
    rm -rf /var/lib/apt/lists/*

# GemfileとGemfile.lockをコピー
COPY Gemfile Gemfile.lock ./

# Bundlerを使用してGemをインストール
RUN bundle install --jobs=4 --retry=3

# アプリケーションコードをコピー
COPY . .

# Bootsnapを事前コンパイル
RUN bundle exec bootsnap precompile --jobs 4 app/ lib/

# セキュリティのためにランタイムファイルのみを非rootユーザーで実行
RUN useradd -ms /bin/bash rails && echo "rails ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER rails

# デフォルトでサーバーを起動する（ランタイムで上書き可能）
EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]