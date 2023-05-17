import os
import shutil

from image_processing import process_image_file, process_images
from PIL import Image

# Replace these with the path to your test images
TEST_IMAGE_SINGLE = "/path/to/single/test/image.jpg"
TEST_IMAGE_MULTIPLE = "/path/to/directory/with/multiple/images"


def test_process_image_file():
    output_path = "test_output_single"
    target_format = "JPG"
    target_size = "1000x1000"
    target_file_size = 50

    # Ensure the output directory is clean
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    output_filename = process_image_file(
        TEST_IMAGE_SINGLE, output_path, target_format, target_size, target_file_size
    )

    # Check if the output file exists
    assert os.path.exists(os.path.join(output_path, output_filename))

    # Check if the output file format is correct
    assert output_filename.endswith("." + target_format.lower())

    # Check if the output file size is less than or equal to the target file size
    assert (
        os.path.getsize(os.path.join(output_path, output_filename))
        <= target_file_size * 1024
    )

    # Check if the output file dimensions are less than or equal to the target size
    with Image.open(os.path.join(output_path, output_filename)) as img:
        width, height = img.size
        max_width, max_height = map(int, target_size.split("x"))
        assert width <= max_width and height <= max_height


def test_process_images():
    output_path = "test_output_multiple"
    target_format = "JPG"
    target_size = "1000x1000"
    target_file_size = 50
    zip_filename = "test_images.zip"

    # Ensure the output directory is clean
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    result = process_images(
        TEST_IMAGE_MULTIPLE,
        output_path,
        target_format,
        target_size,
        target_file_size,
        zip_filename,
    )

    # Check if the zip file exists
    assert os.path.exists(os.path.join(output_path, zip_filename))

    # Check if the processed files list is not empty
    assert len(result["processed_files"]) > 0
