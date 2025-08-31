export function getImageUrl(imagePath) {
  console.log('getImageUrl called with:', imagePath);
  
  if (!imagePath) {
    console.log('No imagePath provided, returning empty string');
    return ''
  }
  
  // If it's already a full URL (Cloudinary or other CDN), return as-is
  if (imagePath.startsWith('http')) {
    console.log('Image is already a full URL, returning as-is:', imagePath);
    return imagePath
  }

  // For legacy local images, construct the full URL
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const finalUrl = imagePath.startsWith('/') ? `${baseUrl}${imagePath}` : `${baseUrl}/${imagePath}`
  console.log('Constructed URL:', finalUrl);
  return finalUrl
}

export function getImageUrls(imagePaths) {
  if (!Array.isArray(imagePaths))
    return []
  return imagePaths.map(getImageUrl)
}
