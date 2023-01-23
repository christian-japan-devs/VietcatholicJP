
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def compressImage(input_image):
    imageTemproary = Image.open(input_image)
    outputIoStream = BytesIO()
    imageTemproary.save(outputIoStream , format='JPEG', quality=60)
    outputIoStream.seek(0)
    input_image = InMemoryUploadedFile(outputIoStream,'ImageField', '%s.jpg' % input_image.name.split('.')[0], 'image/jpg', sys.getsizeof(outputIoStream), None)
    return input_image