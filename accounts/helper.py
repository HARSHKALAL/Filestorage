from wand.image import Image
from PIL import Image as PILImage

def make_pdf_thumbnail(file_path, thumbnail_size):
   
    with Image(filename=file_path, resolution=300) as img:
        img.compression_quality = 99
        img.format = 'jpeg'
        img.crop(0, 0, img.width, img.height)
        img.transform(resize=f"{thumbnail_size[0]}x{thumbnail_size[1]}")
        thumbnail_path = f"{file_path}_thumbnail.jpg"
        img.save(filename=thumbnail_path)

    with PILImage.open(thumbnail_path) as pil_img:
        pil_img.thumbnail(thumbnail_size)
        pil_img.save(thumbnail_path)

    return thumbnail_path