import os
import argparse
from typing import                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Optional, Tuple
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class GPSExtractor:
    def __init__(self, image_path: Optional[str] = None, folder_path: Optional[str] = None):
        """Initialize with the path to a single image or a folder."""
        self.image_path = image_path
        self.folder_path = folder_path

    @staticmethod
    def convert_to_decimal(degrees: Tuple[float, float, float], ref: str) -> float:
        """Convert GPS coordinates to decimal format."""
        decimal = degrees[0] + degrees[1] / 60.0 + degrees[2] / 3600.0
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal

    def extract_gps_data(self, image_path: str) -> Optional[str]:
        """Extract GPS data from an image and return in decimal format."""
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if not exif_data:
                return None

            gps_info = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'GPSInfo':
                    for gps_tag, gps_value in value.items():
                        gps_name = GPSTAGS.get(gps_tag, gps_tag)
                        gps_info[gps_name] = gps_value

            if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
                lat = self.convert_to_decimal(
                    gps_info['GPSLatitude'], gps_info['GPSLatitudeRef']
                )
                lon = self.convert_to_decimal(
                    gps_info['GPSLongitude'], gps_info['GPSLongitudeRef']
                )
                return f'{lat}/{lon}'
            return None
        except Exception as e:
            print(f'Error processing {image_path}: {e}')
            return None

    def process_images(self) -> None:
        """Process images to extract GPS data."""
        if self.image_path:
            if not os.path.isfile(self.image_path):
                print(f'Error: {self.image_path} is not a valid file.')
                return
            gps_data = self.extract_gps_data(self.image_path)
            print(
                f'\033]8;;file://{self.image_path}\033\\{os.path.basename(self.image_path)}\033]8;;\033\\: '
                f'{gps_data if gps_data else 'No GPS data'}'
            )

        elif self.folder_path:
            if not os.path.isdir(self.folder_path):
                print(f'Error: {self.folder_path} is not a valid directory.')
                return
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        file_path = os.path.join(root, file)
                        gps_data = self.extract_gps_data(file_path)
                        print(
                            f'\033]8;;file://{file_path}\033\\{os.path.basename(file_path)}\033]8;;\033\\: '
                            f'{gps_data if gps_data else 'No GPS data'}'
                        )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Extract GPS data from images.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--image', type=str, help='Path to a single image file.')
    group.add_argument(
        '-f', '--folder', type=str, help='Path to a folder containing images.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    gps_extractor = GPSExtractor(image_path=args.image, folder_path=args.folder)
    gps_extractor.process_images()
