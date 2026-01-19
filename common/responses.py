from rest_framework.response import Response
from rest_framework import status

class APIResponse(Response):
    def __init__(self, success=True, message=None, data=None, status_code=None, **kwargs):
        payload = {
            'success': success,
            'message': message or ('Success' if success else 'Error'),
            'data': data,
            **kwargs
        }
        super().__init__(data=payload, status=status_code or (status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)) 