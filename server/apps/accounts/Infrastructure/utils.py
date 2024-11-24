from django.conf import settings
from rest_framework.response import Response


def set_jwt_cookies(
    response: Response, access_token: str, refresh_token: str
) -> Response:
    """
    JWTクッキーを設定する関数
    レスポンスオブジェクトにアクセストークンとリフレッシュトークンのクッキーを設定する。
    付与されたリフレッシュトークンは、アクセストークンの有効期限が切れた場合に使用される。

    Args:
        response (Response): レスポンスオブジェクト
        access_token (str): アクセストークン
        refresh_token (str): リフレッシュトークン

    Returns:
        Response: クッキーが設定されたレスポンスオブジェクト
    """
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=settings.SIMPLE_JWT.get('TOKEN_COOKIE_SECURE', False),
        samesite=settings.SIMPLE_JWT.get('TOKEN_COOKIE_SAMESITE', 'Lax'),
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        path='/',
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=settings.SIMPLE_JWT.get('TOKEN_COOKIE_SECURE', False),
        samesite=settings.SIMPLE_JWT.get('TOKEN_COOKIE_SAMESITE', 'Lax'),
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        path='/',
    )
    return response


def clear_jwt_cookies(response: Response) -> Response:
    """
    JWTクッキーをクリアする関数
    logout時に再度アクセストークンを取得できないようにするため

    Args:
        response (Response): レスポンスオブジェクト

    Returns:
        Response: クッキーがクリアされたレスポンスオブジェクト
    """
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')
    return response
