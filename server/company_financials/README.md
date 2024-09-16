# 1.Directory Structure

```
company_financials
├── __init__.py
├── admin.py
├── apps.py
├── models.py                                         # database model
├── views.py                                          # view
├── core/
│   ├── domain/                                       # domain
│   │   ├── company_symbol_validator.py
│   │   ├── financial_data_extractor.py
│   │   └── company_financials_domain_service.py
│   ├── repository/                                   # interface
│   │   └── company_financials_repository.py
│   └── use_case/                                     # use case
│       └── get_company_financials_use_case.py
├── infra/
│   ├── external/                                     # Correct Factory, API by infra
│   │   ├── finnhub_client_factory.py
│   │   └── finnhub_financials_api.py
│   └── repository/                                   # repository
│       └── django_company_financials_repository.py
├── web/
│   └── serializers/
│       └── company_financials_serializer.py          # interface for serializer
└── migrations/                  
```

# 2.Domain Models
プロジェクトで使用されるドメインモデルについて。

## 1.1 Entity
CompanyFinancials モデルは、企業の財務データを表すエンティティ<br>
企業のシンボル、財務データの年度、財務データの種類、財務データの値を保持する<br>
models.py
```from django.db import models
class CompanyFinancials(models.Model):
    ticker = models.CharField(max_length=10)
    fiscal_year = models.IntegerField()
    total_revenue = models.FloatField(null=True, blank=True)
    normalized_ebitda = models.FloatField(null=True, blank=True)
    stockholders_equity = models.FloatField(null=True, blank=True)
    free_cash_flow = models.FloatField(null=True, blank=True)
    capital_expenditures = models.FloatField(null=True, blank=True)
    total_assets = models.FloatField(null=True, blank=True)
    total_liabilities = models.FloatField(null=True, blank=True)
    gross_profit = models.FloatField(null=True, blank=True)
    net_income_loss = models.FloatField(null=True, blank=True)
    operating_expenses = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```


## 1.2 Repository Interface
企業の財務データを保存・取得するためのインターフェースを定義<br>
core/repository/company_financials_repository.py

## 1.3 Domain Service
### 1.3.1. CompanySymbolValidator
企業のシンボルをバリデーション<br>
core/domain/company_symbol_validator.py

### 1.3.2. FinancialDataExtractor
外部APIの生データから財務データを抽出・変換<br>
domain/financial_data_extractor.py

### 1.3.3. CompanyFinancialsDomainService
財務データの処理を統括<br>
domain/company_financials_domain_service.py

# 3.Sequence Diagrams

## REST API

### company_financials
### GET


### Sequence Diagram
```mermaid
sequenceDiagram
    actor Clien
    participant Django as Django REST Framework
    participant Service as FinancialDataService
    participant Validator as FinancialDataValidator
    participant Repo as CompanyFinancialsRepository
    participant Extractor as FinancialDataExtractor
    participant FinnhubAPI as FinnhubAPIService
    participant DB as CompanyFinancials DB

    Client ->>+ Django: [GET] request
    Django ->>+ Service: get_company_financials
    
    Service ->>+ Validator: validate_symbol
    Validator -->>- Service: validate

    alt キャッシュの有効期限内（同日中のRequest）
        Service ->>+ Repo: fetch
        Repo ->>+ DB: fetch
        DB -->>- Repo: response
        
        Repo -->>- Service: cached_data
        Service -->> Django: Return cached_data
    else キャッシュが古いまたは存在しない
        alt 年数の指定がない場合（直近5年のデータ取得）
            Service ->>+ FinnhubAPI: get
            FinnhubAPI -->>- Service: response
            
            Service ->>+ Extractor: extract
            Extractor -->>- Service: extracted_data
            
            Service ->>+ Repo: save_company_financials(extracted_data)
            Repo ->>+ DB: Insert or Update Financial Data (only if not exists)
            DB -->>- Repo: success/failure
            Repo -->>- Service: confirm
            
            Service -->> Django: Return new_data
        else 年数の指定があり、指定年のデータがない場合
            Service ->>+ FinnhubAPI: fetch_company_financials(symbol)
            FinnhubAPI -->>- Service: financials_data
            
            Service ->>+ Extractor: extract_financial_info
            Extractor -->>- Service: extracted
            
            Service -->> Django: Return extracted_data
            
            par 非同期でデータを保存する処理
                Service ->>+ Repo: save_company_financials(extracted_data)
                Repo ->>+ DB: Insert or Update Financial Data (only if not exists)
                DB -->>- Repo: success/failure
            end
        end
    end

    Django -->>- Client: response (financials data)
```

### Dependency Injection Sequence
```mermaid
sequenceDiagram
    participant View as View
    participant UseCase as UseCase
    participant Repo as Repository
    participant APIService as API Service
    participant ClientFactory as ClientFactory

    View ->>+ Repo: DjangoCompanyFinancialsRepositoryをインスタンス化
    View ->>+ ClientFactory: FinnhubClientFactoryをインスタンス化
    View ->>+ APIService: FinnhubFinancialsAPIをインスタンス化（client=None）
    View ->>+ UseCase: 依存関係を注入してGetCompanyFinancialsUseCaseをインスタンス化
    UseCase ->> UseCase: execute(symbol, start_year, end_year)
    UseCase ->>+ ClientFactory: create_client()
    ClientFactory -->>- UseCase: client
    UseCase ->> APIService: clientを設定
    Note over UseCase,APIService: 以降はビジネスロジックの処理
```