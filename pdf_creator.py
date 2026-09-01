# pdf_creator.py

from PIL import Image


def create_pdf(image_files, output_file):

    if not image_files:
        raise ValueError("No images found.")

    image_files = sorted(image_files)

    images = []

    for image_file in image_files:

        image = Image.open(image_file)

        image = image.convert("RGB")

        images.append(image)

    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:]
    )