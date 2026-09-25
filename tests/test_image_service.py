from PIL import Image

from app.services.image_service import crop_image

def test_crop_image():
    image = Image.new("RGB", (800, 600), "white")

    cropped = crop_image(image, left=100, top=100, right=500, bottom=400)

    assert cropped.size == (400, 300)