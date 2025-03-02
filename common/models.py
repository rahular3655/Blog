from django.db import models
from PIL import Image
import os
from io import BytesIO

class BaseImageModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        image_fields = [field.name for field in self._meta.get_fields() if isinstance(field, models.ImageField)]
        for field_name in image_fields:
            image_field = getattr(self, field_name)
            if image_field:
                # Open the original image
                img = Image.open(image_field)

                # Convert image to WebP format
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Create a BytesIO buffer to hold the WebP image data
                buffer = BytesIO()

                # Save the image to the buffer in WebP format
                img.save(buffer, format='WEBP')

                # Set the buffer's file pointer to the beginning
                buffer.seek(0)

                # Update the instance with the WebP image
                webp_filename = os.path.splitext(os.path.basename(image_field.name))[0] + '.webp'
                getattr(self, field_name).save(webp_filename, BytesIO(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

