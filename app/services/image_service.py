from PIL import Image

def crop_image(image: Image.Image, left: int, top: int, right: int, bottom: int) -> Image.Image:
    return image.crop((left, top, right, bottom))

def resize_image(image: Image.Image, width:int, height:int) -> Image.Image:
    return image.resize((width, height), Image.Resampling.LANCZOS) 