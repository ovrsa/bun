import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context) -> Response:
    """
    例外ハンドラー
    例外をキャッチしてログを出力し、レスポンスを返す

    Args:
        exc (Exception): 例外
        context (dict): コンテキスト

    Returns:
        Response: レスポンス
    """
    logger.error(f"Exception occurred: {exc}", exc_info=True)

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        response = Response(
            {
                "detail": "Internal server error occurred.",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
