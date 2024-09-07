import pytest
from company_profiles.services.finnhub_service import FinnhubService
from rest_framework.exceptions import NotFound, AuthenticationFailed, APIException


@pytest.mark.django_db
class TestFinnhubService:

    @pytest.fixture
    def service(self):
        return FinnhubService()

    def test_invalid_symbol_raises_not_found(self, mocker, service):
        mock_finnhub_client = mocker.patch.object(service, 'client')
        mock_finnhub_client.company_profile2.return_value = None

        with pytest.raises(NotFound, match="ティッカーから企業が見つかりませんでした"):
            service.get_company_profile("INVALID")

    def test_authentication_failure(self, mocker, service):
        mock_finnhub_client = mocker.patch.object(service, 'client')
        mock_finnhub_client.company_profile2.side_effect = AuthenticationFailed(
            "認証に失敗しました")

        with pytest.raises(AuthenticationFailed, match="認証に失敗しました"):
            service.get_company_profile("AAPL")

    def test_server_unavailable(self, mocker, service):
        mock_finnhub_client = mocker.patch.object(service, 'client')
        mock_finnhub_client.company_profile2.side_effect = APIException(
            "サーバーが一時的に利用できません。しばらくしてから再試行してください")

        with pytest.raises(APIException, match="サーバーが一時的に利用できません。しばらくしてから再試行してください"):
            service.get_company_profile("SOME_OTHER_SYMBOL")
