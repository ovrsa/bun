from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        logger.exception(f'No valid token was found in the request: {str(exc)}')
        custom_response_data = {
            'message': 'No valid token was found in the request'
        }
        return Response(custom_response_data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, ValidationError):
        logger.exception(f'Invalid request data: {str(exc)}')
        custom_response_data = {
            'message': 'Invalid request data'
        }
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, TimeoutError):
        logger.exception(f'Request to external service timed out: {str(exc)}')
        custom_response_data = {
            'message': 'Request to external service timed out'
        }
        return Response(custom_response_data, status=status.HTTP_504_GATEWAY_TIMEOUT)

    elif response is not None:
        return response
    else:
        logger.exception(f'Unhandled exception: {str(exc)}')
        custom_response_data = {
            'message': f'Internal server error: {str(exc)}'
        }
        return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
