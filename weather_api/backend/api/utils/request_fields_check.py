from typing import Union
from rest_framework import status
from rest_framework.response import Response


def handle_errors(data: dict, allowed_fields: list) -> Union[Response, None]:
    """Check that all fields are in request"""
    for field in allowed_fields:
        if field not in data.keys():
            return Response({'error': f'Missing {field} field'}, status=status.HTTP_400_BAD_REQUEST)

    unexpected_fields = [field for field in data.keys() if field not in allowed_fields]
    if unexpected_fields:
        return Response({'error': f'Unexpected fields: {unexpected_fields}'}, status=status.HTTP_400_BAD_REQUEST)