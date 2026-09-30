from io import BytesIO
from PIL import Image

def crop_image(image: Image.Image, left: int, top: int, right: int, bottom: int) -> Image.Image:
    return image.crop((left, top, right, bottom))

def resize_image(image: Image.Image, width:int, height:int) -> Image.Image:
    return image.resize((width, height), Image.Resampling.LANCZOS) 

def compress_image(image: Image.Image, quality: int = 70) -> Image.Image:
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    compressed = Image.open(buffer).copy()
    compressed.format = "JPEG"
    return compressed