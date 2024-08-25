import os
import json
from PIL import Image, PngImagePlugin, ImageEnhance
from widgets.path_helpers.path_helpers import get_images_and_data_path

def resize_image(image_path: str, scale_factor: float) -> None:
    try:
        # Open the image and extract metadata
        with Image.open(image_path) as img:
            metadata = img.info.get("metadata")

            # Resize image to a percentage of its original size with LANCZOS filter
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            resized_img = img.resize(new_size, Image.LANCZOS)

            # Optional: Apply sharpening to improve clarity
            enhancer = ImageEnhance.Sharpness(resized_img)
            resized_img = enhancer.enhance(1.5)  # 1.0 is original sharpness; >1.0 increases sharpness

            # Create the PngInfo object and reapply metadata
            if metadata:
                png_info = PngImagePlugin.PngInfo()
                png_info.add_text("metadata", metadata)

                # Save the resized image with metadata
                resized_img.save(image_path, "PNG", pnginfo=png_info)
            else:
                # Save without metadata if none exists
                resized_img.save(image_path, "PNG")

            print(f"Resized and saved: {image_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_dictionary_images(dictionary_dir: str, scale_factor: float) -> None:
    for root, dirs, files in os.walk(dictionary_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                image_path = os.path.join(root, file)
                resize_image(image_path, scale_factor)

if __name__ == "__main__":
    # Directory containing the images to be processed
    dictionary_directory = get_images_and_data_path("dictionary")
    scale_factor = 0.5  # Resize images to 65% of their original size
    process_dictionary_images(dictionary_directory, scale_factor)
    print("Processing complete.")
