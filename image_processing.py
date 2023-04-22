import argparse
import os
import shutil
import sys
import tempfile
import zipfile

from loguru import logger
from PIL import Image

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": "DEBUG",
            "colorize": True,
        }
    ]
)


def compress_image(
    image, image_file, output_filepath, target_file_size_kb, image_format
):
    original_file_size = os.path.getsize(image_file)
    target_file_size_bytes = target_file_size_kb * 1024

    # 確保輸出目錄存在
    output_directory = os.path.dirname(output_filepath)
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
            logger.info(f"Created directory: {output_directory}")
        except Exception as e:
            logger.error(f"Error creating directory: {output_directory}: {e}")
            return

    if original_file_size <= target_file_size_bytes:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                image.save(temp_file.name, format=image_format)
                shutil.move(temp_file.name, output_filepath)
        except Exception as e:
            logger.error(f"Error saving file: {output_filepath}: {e}")
            raise
    else:
        compression_ratio = target_file_size_bytes / original_file_size
        quality = int(100 * compression_ratio)
        quality = max(1, min(100, quality))

        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                image.save(temp_file.name, format=image_format, quality=quality)
                shutil.move(temp_file.name, output_filepath)
        except Exception as e:
            logger.error(f"Error saving file: {output_filepath}: {e}")
            raise


def process_image_file(
    image_file, output_path, target_format, target_size, target_file_size
):

    width, height = map(int, target_size.split("x"))
    target_format = target_format.upper()

    try:
        with Image.open(image_file) as img:

            img = img.convert("RGB")
            img = img.resize((width, height), Image.ANTIALIAS)

            output_filename = (
                os.path.splitext(os.path.basename(image_file))[0]
                + "."
                + target_format.lower()
            )

            output_filepath = os.path.join(output_path, output_filename)
            compress_image(
                img, image_file, output_filepath, target_file_size, target_format
            )

            return output_filename
    except Exception as e:
        logger.error(f"Error Processed file: {image_file}: {e}")


def process_images(
    input_path, output_path, target_format, target_size, target_file_size, zip_filename
):

    if not os.path.exists(input_path):
        raise FileNotFoundError("Input path does not exist.")

    supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]

    image_files = [
        os.path.join(input_path, f)
        for f in os.listdir(input_path)
        if os.path.splitext(f)[1].lower() in supported_formats
    ]
    processed_files = []

    with zipfile.ZipFile(os.path.join(output_path, zip_filename), mode="w") as zip_file:
        for image_file in image_files:
            output_filename = process_image_file(
                image_file, output_path, target_format, target_size, target_file_size
            )

            if output_filename:
                processed_files.append(output_filename)

                output_filepath = os.path.join(output_path, output_filename)
                if os.path.exists(output_filepath):
                    zip_file.write(output_filepath, arcname=output_filename)
                    os.remove(output_filepath)
                else:
                    logger.error(f"File not found: {output_filepath}")

    return {
        "processed_files": processed_files,
    }


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Image Processing Script")
    parser.add_argument(
        "--mode",
        choices=["single", "multiple"],
        required=True,
        help="Choose 'single' for processing a single image or 'multiple' for processing multiple images",
    )
    parser.add_argument("--input_path", required=True, help="Path to the input images")
    parser.add_argument(
        "--output_path", required=True, help="Path to the output images"
    )
    parser.add_argument(
        "--target_format", default="JPG", help="Target format for the images"
    )
    parser.add_argument(
        "--target_size", default="1000x1000", help="Target size for the images"
    )
    parser.add_argument(
        "--target_file_size",
        type=int,
        default=50,
        help="Target file size for the images in KB",
    )
    parser.add_argument(
        "--zip_filename",
        default="processed_images.zip",
        help="Filename for the ZIP file containing processed images",
    )

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    target_format = args.target_format
    target_size = args.target_size
    target_file_size = args.target_file_size
    zip_filename = args.zip_filename

    if args.mode == "single":
        output_filename = process_image_file(
            input_path, output_path, target_format, target_size, target_file_size
        )
        print(f"Processed file: {os.path.join(output_path, output_filename)}")
    else:
        # Call process_images function and print the processed files list
        result = process_images(
            input_path,
            output_path,
            target_format,
            target_size,
            target_file_size,
            zip_filename,
        )
        print(f"Processed files: {result['processed_files']}")
