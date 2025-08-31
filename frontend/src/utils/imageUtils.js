export function getImageUrl(imagePath) {
  if (!imagePath)
    return ''
  
  // If it's already a full URL (Cloudinary or other CDN), return as-is
  if (imagePath.startsWith('http'))
    return imagePath

  // For legacy local images, construct the full URL
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return imagePath.startsWith('/') ? `${baseUrl}${imagePath}` : `${baseUrl}/${imagePath}`
}

export function getImageUrls(imagePaths) {
  if (!Array.isArray(imagePaths))
    return []
  return imagePaths.map(getImageUrl)
}
