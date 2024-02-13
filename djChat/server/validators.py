import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The Max Size Allowd for Image Dimensions is 70x70, Size of Uploaded Image:{img.size}"
                )


def validate_image_file_extension(value):
    ext = os.path.split(value.name)[1]
    valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Un-Supported File extension")
