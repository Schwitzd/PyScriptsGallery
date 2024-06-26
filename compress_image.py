"""
version: 1.4 | Author: Daniel Schwitzgebel | Created: 24.06.2022 | Updated: 20.04.2024
Description: This script compresses JPEG and PNG images located in a specified directory.
"""

import argparse
import os
from typing import List
from PIL import Image


def get_args()-> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='image path')
    return parser.parse_args()


def compress_jpg(filepath: str) -> None:
    """Compress jpg images"""
    pathname, filename = os.path.split(filepath)
    compressed_path = f'{pathname}\\compressed_{filename}'
    picture = Image.open(filepath)
    picture.save(compressed_path, optimize=True, quality=70)


def compress_png(filepath: str) -> None:
    """Compress png images"""
    pathname, filename = os.path.split(filepath)
    compressed_path = f'{pathname}\\compressed_{filename}'
    picture = Image.open(filepath)
    picture = picture.convert('P', palette=Image.ADAPTIVE, colors=256)
    picture.save(compressed_path, optimize=True)


def get_images(path: str) -> List[str]:
    """Get all images"""
    formats = ('.png', '.jpg', '.jpeg')
    images = []
    for file in os.listdir(path):
        if file.endswith(formats):
            images.append(os.path.join(path, file))
    return images


def main():
    """Script main function"""
    args = get_args()
    images = get_images(args.path)

    for image in images:
        if image.endswith('.png'):
            compress_png(image)
        elif image.endswith(('.jpg', '.jpeg')):
            compress_jpg(image)


if __name__ == '__main__':
    main()
