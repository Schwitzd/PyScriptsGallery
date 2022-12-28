import os
import argparse
import pathlib
from glob import glob
from PIL import Image


def get_args():
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images', required=True, type=pathlib.Path,
                        dest='images', help='image path')
    parser.add_argument('-o', '--output', required=True, type=pathlib.Path,
                        dest='output', help='image output path')
    args = parser.parse_args()

    return args


def check_same_size(images_filename: list[str]) -> bool:
    """Check that all images have the same size"""
    reference_size = None

    for img in images_filename:
        with Image.open(img) as oi:
            if reference_size is None:
                reference_size = oi.size
            elif reference_size != oi.size:
                raise ValueError('All images must be with the same size')

    return True


def get_image_size(image: str) -> list[int]:
    """Get the size of the first image"""
    with Image.open(image) as oi:
        return oi.size


def get_images(path: str):
    """Get all images"""
    extensions = ('*.jpg', '*.jpeg', '*.png')
    images = []
    for ext in extensions:
        images.extend(glob(os.path.join(path, ext)))

    return images


def calc_canvas_size(
    images: list[str],
    image_size: list[int]
) -> list[int]:
    """Calculate the size of the final image"""
    num_images = len(images)
    num_rows = num_images // 2

    if num_images % 2 == 1:
        num_rows += 1 # if there is an odd number of images, add an extra row

    canvas_width = 2 * image_size[0]
    canvas_height = num_rows * image_size[1]

    return (canvas_width, canvas_height)


def generate_canvas(
    images: list[str],
    image_size: list[int],
    width: int,
    height: int,
    destination: str
) -> None:
    """Generate the canvas of the collage image"""
    canvas = Image.new('RGB', (width, height))

    for i, image in enumerate(images):
        x = (i % 2) * image_size[0]
        y = (i // 2) * image_size[1]
        image_paste = Image.open(image)
        canvas.paste(image_paste, (x, y))

    canvas.save(destination)


def main():
    args = get_args()
    images = get_images(args.images)

    if check_same_size(images):
        # Get size of first image only
        image_size = get_image_size(images[0])
        # Calculate the size of the canvas
        width, height = calc_canvas_size(images, image_size)
        # Generate the final image
        generate_canvas(images, image_size, width, height, args.output)


if __name__ == "__main__":
    main()
