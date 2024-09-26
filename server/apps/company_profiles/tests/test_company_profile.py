import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed, NotFound


@pytest.mark.django_db
def test_company_profile_view_with_valid_symbol(mocker):
    """
    正しいシンボルでAPIが正常に企業情報を返すかをテストする。
    """
    mock_finnhub_service = mocker.patch(
        'company_profiles.services.finnhub_service.FinnhubService.get_company_profile')
    mock_finnhub_service.return_value = {
        "ticker": "AAPL",
        "name": "Apple Inc",
        "country": "US",
        "currency": "USD",
        "exchange": "NASDAQ",
        "ipo_date": "1980-12-12",
        "marketCapitalization": 2000000,
        "phone": "14089961010",
        "shareOutstanding": 1000.0,
        "website_url": "https://www.apple.com/",
        "logo_url": "https://example.com/logo.png",
        "finnhubIndustry": "Technology"
    }

    client = APIClient()
    url = reverse('company-profile')
    response = client.get(url, {'symbol': 'AAPL'})

    # レスポンス検証
    assert response.status_code == 200
    assert response.data['ticker'] == 'AAPL'
    assert response.data['name'] == "Apple Inc"

    mock_finnhub_service.assert_called_once_with('AAPL')


@pytest.mark.django_db
def test_company_profile_view_with_invalid_symbol(mocker):
    """
    不正なシンボルでAPIが適切なエラーメッセージを返すかをテストする。
    """
    mock_finnhub_service = mocker.patch(
        'company_profiles.services.finnhub_service.FinnhubService.get_company_profile')
    mock_finnhub_service.side_effect = NotFound(
        "ティッカーから企業が見つかりませんでした")

    client = APIClient()
    url = reverse('company-profile')
    response = client.get(url, {'symbol': 'INVALID'})

    # レスポンス検証
    assert response.status_code == 404
    assert 'message' in response.data
    assert response.data['message'] == "ティッカーから企業が見つかりませんでした"


@pytest.mark.django_db
def test_company_profile_view_unauthorized(mocker):
    """
    認証に失敗した場合に適切なエラーメッセージを返すかをテストする。
    """
    mock_finnhub_service = mocker.patch(
        'company_profiles.services.finnhub_service.FinnhubService.get_company_profile')
    mock_finnhub_service.side_effect = AuthenticationFailed(
        "認証に失敗しました")  # Unauthorized エラーをシミュレート

    client = APIClient()
    url = reverse('company-profile')
    response = client.get(url, {'symbol': 'AAPL'})

    assert response.status_code == 401
    assert 'message' in response.data
    assert response.data['message'] == "認証に失敗しました"
