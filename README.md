# Resize-image-template

This is a Python script for processing images. The script can process a single image or multiple images in a directory. The images can be resized and converted to a different format, and their file size can be reduced.

These dependencies can be installed via pip:

```bash
pip install -r requirements.txt
```

# Usage

The script can be used from the command line with the following arguments:

```scss
usage: image_processing.py [-h] --mode {single,multiple} --input_path INPUT_PATH --output_path OUTPUT_PATH [--target_format TARGET_FORMAT] [--target_size TARGET_SIZE] [--target_file_size TARGET_FILE_SIZE] [--zip_filename ZIP_FILENAME]

Image Processing Script

optional arguments:
  -h, --help            show this help message and exit
  --mode {single,multiple}
                        Choose 'single' for processing a single image or 'multiple' for processing multiple images
  --input_path INPUT_PATH
                        Path to the input images
  --output_path OUTPUT_PATH
                        Path to the output images
  --target_format TARGET_FORMAT
                        Target format for the images (default: JPG)
  --target_size TARGET_SIZE
                        Target size for the images (default: 1000x1000)
  --target_file_size TARGET_FILE_SIZE
                        Target file size for the images in KB (default: 50)
  --zip_filename ZIP_FILENAME
                        Filename for the ZIP file containing processed images (default: processed_images.zip)

```

# Examples

Process a single image:

```css
python image_processing.py --mode single --input_path "input/download.jpeg" --output_path "output" --target_format "jpeg" --target_size "1000x1000" --target_file_size 50
```

```css
python image_processing.py --mode multiple --input_path "input" --output_path "output" --target_format "jpeg" --target_size "1000x1000" --target_file_size 50 --zip_filename "processed_images.zip"
```
