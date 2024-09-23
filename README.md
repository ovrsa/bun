- [EN:](#en)
  - [Application Overview](#application-overview)
  - [Tech Stack](#tech-stack)
    - [Docker](#docker)
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
- [JA:](#ja)
  - [概要](#概要)
  - [技術スタック](#技術スタック)
    - [Docker](#docker-1)
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
- 

### Libraries:
- 

### Testing:
- 

## Setup

### Prerequisites
- Docker and Docker Compose are installed

### Local Setup

1. Clone the repository

2. Start the environment with Docker Compose
   ```bash
   docker-compose up --build
   ```

# JA:
## 概要


## 技術スタック

### Docker

#### サービス

## フロントエンド

### 技術スタック:

### ライブラリ:

### テスト:

## バックエンド

### 技術スタック

### ライブラリ:

### テスト:

## 環境構築

### 前提条件
- DockerおよびDocker Composeがインストールされていること

### ローカルでの立ち上げ

1. リポジトリをクローン

2. Docker Composeで環境を立ち上げる
   ```bash
   docker-compose up --build
   ```