from PIL import Image

from app.services.image_service import crop_image, resize_image, compress_image

def test_crop_image():
    image = Image.new("RGB", (800, 600), "white")
    cropped = crop_image(image, left=100, top=100, right=500, bottom=400)
    assert cropped.size == (400, 300)

def test_resize_image():
    image = Image.new("RGB", (800, 600), "white")
    resized = resize_image(image, width=400, height=300)
    assert resized.size == (400, 300)

def test_compress_image():
    image = Image.new("RGB", (800, 600), "white")
    compressed = compress_image(image, quality=70)
    assert compressed.size == (800, 600)
    assert compressed.format == "JPEG"