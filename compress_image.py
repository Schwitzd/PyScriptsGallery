import argparse
import os
from PIL import Image

def get_args():
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='image path')
    args = parser.parse_args()
    return args


def compress_jpg(filepath):
    """Compress jpg images"""
    pathname, filename = os.path.split(filepath)
    compressed_path = pathname + '\compressed_' + filename
    picture = Image.open(filepath)
    picture.save(compressed_path, optimize = True, quality = 70)

    return

def compress_png(filepath):
    """Compress png images"""
    pathname, filename = os.path.split(filepath)
    compressed_path = pathname + '\\compressed_' + filename
    picture = Image.open(filepath)
    picture = picture.convert('P', palette=Image.ADAPTIVE, colors=256)
    picture.save(compressed_path, optimize=True)

    return


def get_images(path):
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


if __name__ == "__main__":
    main()
