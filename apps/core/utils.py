import cloudinary.uploader
import cloudinary
from django.conf import settings

def upload_image_to_cloudinary(file, folder="ecommerce"):
    """Uploads an image file to Cloudinary and returns a dict with
    {url, public_id}. Raises exceptions if upload fails."""
    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        resource_type="image",
        overwrite=True
    )
    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id")
    }


def delete_from_cloudinary(public_id):
    """Deletes an asset by its public_id. Safe to call even if missing."""
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass
