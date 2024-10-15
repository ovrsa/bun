sequenceDiagram
    participant Client as クライアント
    participant ViewSet as CompanyProfileViewSet
    participant TickerRef as TickerReferenceモデル
    participant Repository as CompanyProfileリポジトリ
    participant UseCase as GetCompanyProfileUseCase
    participant Fetcher as YFinanceCompanyProfileFetcher
    participant DB as データベース
    participant ExternalAPI as 外部API

    Client->>ViewSet: GET /api/company-profiles/?symbol=AAPL
    ViewSet->>TickerRef: get_or_create(ticker=AAPL)
    TickerRef-->>ViewSet: Returns TickerReferenceオブジェクト

    ViewSet->>UseCase: execute(ticker_ref)
    
    UseCase->>Repository: get_by_ticker(ticker_ref)
    Repository->>DB: TickerReferenceで企業プロファイルをクエリ
    DB-->>Repository: 結果なし
    Repository-->>UseCase: None
    
    UseCase->>Fetcher: fetch(AAPL)
    Fetcher->>ExternalAPI: Yahoo Finance APIにリクエスト
    ExternalAPI-->>Fetcher: 企業情報を返却
    Fetcher-->>UseCase: 企業プロファイルデータを返却
    
    UseCase->>Repository: save(company_profile_data, ticker_ref)
    Repository->>DB: 企業情報を保存
    DB-->>Repository: 保存成功
    Repository-->>UseCase: CompanyProfileオブジェクトを返却

    UseCase-->>ViewSet: CompanyProfileオブジェクトを返却
    ViewSet->>Client: 200 OK + 企業情報JSON
