from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

@api_view(['GET'])
def test_cloudinary_config(request):
    """Test endpoint to check if Cloudinary is configured properly"""
    return Response({
        'cloudinary_configured': bool(os.getenv('CLOUDINARY_CLOUD_NAME')),
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', 'NOT_SET'),
        'api_key_set': bool(os.getenv('CLOUDINARY_API_KEY')),
        'api_secret_set': bool(os.getenv('CLOUDINARY_API_SECRET')),
    })
