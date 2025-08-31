import requests
import hashlib
import hmac
import time
import base64
from django.conf import settings
import uuid
import os

class CloudinaryService:
    """
    Service class for handling Cloudinary uploads and deletions using REST API
    """
    
    @staticmethod
    def _get_cloudinary_config():
        """Get Cloudinary configuration from settings"""
        return {
            'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
            'api_key': os.environ.get('CLOUDINARY_API_KEY'),
            'api_secret': os.environ.get('CLOUDINARY_API_SECRET'),
        }
    
    @staticmethod
    def _generate_signature(params, api_secret):
        """Generate signature for Cloudinary API"""
        # Sort parameters and create string
        sorted_params = sorted(params.items())
        param_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
        
        # Create signature
        signature = hmac.new(
            api_secret.encode('utf-8'),
            param_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    @staticmethod
    def upload_image(image_file, folder="openshelf"):
        """
        Upload an image to Cloudinary using REST API
        """
        try:
            config = CloudinaryService._get_cloudinary_config()
            
            # Generate unique filename
            unique_filename = f"{folder}_{uuid.uuid4().hex}"
            timestamp = str(int(time.time()))
            
            # Prepare upload parameters
            params = {
                'folder': folder,
                'public_id': unique_filename,
                'timestamp': timestamp,
                'transformation': 'q_auto,f_auto'
            }
            
            # Generate signature
            signature = CloudinaryService._generate_signature(params, config['api_secret'])
            
            # Prepare form data
            files = {'file': image_file}
            data = {
                **params,
                'api_key': config['api_key'],
                'signature': signature
            }
            
            # Upload to Cloudinary
            upload_url = f"https://api.cloudinary.com/v1_1/{config['cloud_name']}/image/upload"
            response = requests.post(upload_url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'url': result.get('secure_url'),
                    'public_id': result.get('public_id'),
                    'width': result.get('width'),
                    'height': result.get('height'),
                    'format': result.get('format'),
                    'bytes': result.get('bytes'),
                }
            else:
                return {
                    'success': False,
                    'error': f'Upload failed: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def delete_image(public_id):
        """
        Delete an image from Cloudinary using REST API
        """
        try:
            config = CloudinaryService._get_cloudinary_config()
            timestamp = str(int(time.time()))
            
            # Prepare delete parameters
            params = {
                'public_id': public_id,
                'timestamp': timestamp
            }
            
            # Generate signature
            signature = CloudinaryService._generate_signature(params, config['api_secret'])
            
            # Prepare data
            data = {
                **params,
                'api_key': config['api_key'],
                'signature': signature
            }
            
            # Delete from Cloudinary
            delete_url = f"https://api.cloudinary.com/v1_1/{config['cloud_name']}/image/destroy"
            response = requests.post(delete_url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'result': result.get('result')
                }
            else:
                return {
                    'success': False,
                    'error': f'Delete failed: {response.text}'
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
        """
        try:
            config = CloudinaryService._get_cloudinary_config()
            base_url = f"https://res.cloudinary.com/{config['cloud_name']}/image/upload"
            
            # Build transformation string
            transformations = ["q_auto", "f_auto"]
            
            if width and height:
                transformations.append(f"w_{width},h_{height},c_{crop}")
            elif width:
                transformations.append(f"w_{width}")
            elif height:
                transformations.append(f"h_{height}")
            
            transformation_string = ",".join(transformations)
            
            # Build final URL
            url = f"{base_url}/{transformation_string}/{public_id}"
            return url
            
        except Exception as e:
            print(f"Error generating optimized URL: {e}")
            return None
