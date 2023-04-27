import os
import argparse
import pathlib
from glob import glob
from dataclasses import dataclass
from PIL import Image


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images', required=True, type=pathlib.Path,
                        dest='images', help='image path')
    parser.add_argument('-o', '--output', required=True, type=pathlib.Path,
                        dest='output', help='image output path')
    args = parser.parse_args()

    return args


@dataclass
class ImageSize:
    """Hold the size of a single image"""
    width: int
    height: int

def check_size(images_filename: list[str]) -> ImageSize:
    """Check that all images have the same size"""
    reference_size = None

    for img in images_filename:
        with Image.open(img) as oi:
            if reference_size is None:
                reference_size = oi.size
            elif reference_size != oi.size:
                raise ValueError('All images must be with the same size')

    return ImageSize(oi.width, oi.height)


def get_images(path: str) -> list[str]:
    """Get all images"""
    extensions = ('*.jpg', '*.jpeg', '*.jfif', '*.png')
    images = []
    for ext in extensions:
        images.extend(glob(os.path.join(path, ext)))

    return images


@dataclass
class CanvasSize:
    """Hold the size of the final canvas"""
    width: int
    height: int

def calc_canvas_size(
    images: list[str],
    image_size: ImageSize
) -> CanvasSize:
    """Calculate the size of the final image"""
    num_images = len(images)
    num_rows = num_images // 2

    if num_images % 2 == 1:
        num_rows += 1 # if there is an odd number of images, add an extra row

    canvas_width = 2 * image_size.width
    canvas_height = num_rows * image_size.height

    return CanvasSize(canvas_width, canvas_height)


def generate_canvas(
    images: list[str],
    image_size: ImageSize,
    canvas_size: CanvasSize,
    destination: str
) -> None:
    """Generate the canvas of the collage image"""
    canvas = Image.new('RGB', (canvas_size.width, canvas_size.height))

    for i, image in enumerate(images):
        x = (i % 2) * image_size.width
        y = (i // 2) * image_size.height
        image_paste = Image.open(image)
        canvas.paste(image_paste, (x, y))

    canvas.save(destination)


def main() -> None:
    """Main function"""
    args = get_args()
    images = get_images(args.images)
    image_size = check_size(images)

    if image_size:
        # Calculate the size of the canvas
        canvas_size = calc_canvas_size(images, image_size)
        # Generate the final image
        generate_canvas(images, image_size, canvas_size, args.output)


if __name__ == "__main__":
    main()
