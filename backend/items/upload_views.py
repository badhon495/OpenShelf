from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.cloudinary_service import CloudinaryService
import os


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_images(request):
    """
    Upload multiple images to Cloudinary and return their URLs
    """
    if 'images' not in request.FILES:
        return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    uploaded_data = []
    successful_uploads = []
    errors = []
    
    for image in request.FILES.getlist('images'):
        # Validate file type
        if not image.content_type.startswith('image/'):
            errors.append(f'File {image.name} is not an image')
            continue
        
        # Validate file size (max 10MB)
        if image.size > 10 * 1024 * 1024:
            errors.append(f'File {image.name} is too large (max 10MB)')
            continue
        
        # Upload to Cloudinary
        result = CloudinaryService.upload_image(image, folder="openshelf/items")
        
        if result['success']:
            successful_uploads.append({
                'url': result['url'],
                'public_id': result['public_id'],
                'width': result.get('width'),
                'height': result.get('height'),
                'format': result.get('format'),
                'bytes': result.get('bytes'),
            })
        else:
            errors.append(f'Failed to upload {image.name}: {result["error"]}')
    
    # Return response with successful uploads and any errors
    response_data = {
        'uploaded_images': successful_uploads,
        'image_urls': [img['url'] for img in successful_uploads],
        'public_ids': [img['public_id'] for img in successful_uploads]
    }
    
    if errors:
        response_data['errors'] = errors
        return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request):
    """
    Delete an image from Cloudinary
    """
    public_id = request.data.get('public_id')
    
    if not public_id:
        return Response({'error': 'No public_id provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    result = CloudinaryService.delete_image(public_id)
    
    if result['success']:
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_optimized_url(request):
    """
    Get optimized URL for an image with specific dimensions
    """
    public_id = request.data.get('public_id')
    width = request.data.get('width')
    height = request.data.get('height')
    crop = request.data.get('crop', 'fill')
    
    if not public_id:
        return Response({'error': 'No public_id provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    optimized_url = CloudinaryService.get_optimized_url(
        public_id, width=width, height=height, crop=crop
    )
    
    if optimized_url:
        return Response({'optimized_url': optimized_url}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Failed to generate optimized URL'}, status=status.HTTP_400_BAD_REQUEST)
