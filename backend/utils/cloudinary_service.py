import cloudinary.uploader
import cloudinary.api
from django.conf import settings
import uuid
import os

class CloudinaryService:
    """
    Service class for handling Cloudinary uploads and deletions
    """
    
    @staticmethod
    def upload_image(image_file, folder="openshelf"):
        """
        Upload an image to Cloudinary
        
        Args:
            image_file: The image file to upload
            folder: The folder name in Cloudinary (default: "openshelf")
            
        Returns:
            dict: Response from Cloudinary with URL and public_id
        """
        try:
            # Generate a unique filename
            unique_filename = f"{folder}_{uuid.uuid4().hex}"
            
            # Upload to Cloudinary
            response = cloudinary.uploader.upload(
                image_file,
                folder=folder,
                public_id=unique_filename,
                overwrite=True,
                resource_type="image",
                transformation=[
                    {'quality': 'auto'},
                    {'fetch_format': 'auto'}
                ]
            )
            
            return {
                'success': True,
                'url': response.get('secure_url'),
                'public_id': response.get('public_id'),
                'width': response.get('width'),
                'height': response.get('height'),
                'format': response.get('format'),
                'bytes': response.get('bytes'),
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def delete_image(public_id):
        """
        Delete an image from Cloudinary
        
        Args:
            public_id: The public ID of the image to delete
            
        Returns:
            dict: Response from Cloudinary
        """
        try:
            response = cloudinary.uploader.destroy(public_id)
            return {
                'success': True,
                'result': response.get('result')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def upload_multiple_images(image_files, folder="openshelf"):
        """
        Upload multiple images to Cloudinary
        
        Args:
            image_files: List of image files to upload
            folder: The folder name in Cloudinary
            
        Returns:
            list: List of upload responses
        """
        results = []
        for image_file in image_files:
            result = CloudinaryService.upload_image(image_file, folder)
            results.append(result)
        return results
    
    @staticmethod
    def get_optimized_url(public_id, width=None, height=None, crop="fill"):
        """
        Get an optimized URL for an image
        
        Args:
            public_id: The public ID of the image
            width: Desired width
            height: Desired height
            crop: Crop mode
            
        Returns:
            str: Optimized image URL
        """
        try:
            transformations = [
                {'quality': 'auto'},
                {'fetch_format': 'auto'}
            ]
            
            if width and height:
                transformations.append({
                    'width': width,
                    'height': height,
                    'crop': crop
                })
            elif width:
                transformations.append({'width': width})
            elif height:
                transformations.append({'height': height})
            
            url, options = cloudinary.utils.cloudinary_url(
                public_id,
                transformation=transformations,
                secure=True
            )
            
            return url
            
        except Exception as e:
            print(f"Error generating optimized URL: {e}")
            return None
