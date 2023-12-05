import cv2
import os
import numpy as np

# Load the stylized image
image_path_drawn = 'V4/starry_night_drawn.png'
image_drawn = cv2.imread(image_path_drawn)

# Check if the image was loaded correctly
if image_drawn is None:
    raise ValueError("Could not load the image from the path provided.")

# Load the original image
image_path_original = 'V4/starry_night_original.png'
image_original = cv2.imread(image_path_original)

# Check if the image was loaded correctly
if image_original is None:
    raise ValueError("Could not load the image from the path provided.")

# Parameters
#patch_sizes = {64, 96, 128, 192, 256, 512, 1024}  # Size of the square
patch_sizes = {64}
padding = 16  # Padding around the square
corner_range = 8  # Range to check for non-black pixels

# Function to check if a corner (or the center) has a non-black pixel within a certain range
def corner_has_color(img, corner, range_size):
    y, x = corner
    corner_area = img[max(0, y-range_size):y+range_size+1, max(0, x-range_size):x+range_size+1]
    return np.any(corner_area != 0)

# Create the dataset folders if they don't exist
version = 7
dataset_folder_drawn = f'V4/data/dataset_drawn_{version}'
dataset_folder_original = f'V4/data/dataset_original_{version}'
dataset_folder_validation = f'V4/data/dataset_validation_{version}'
os.makedirs(dataset_folder_drawn, exist_ok=True)
os.makedirs(dataset_folder_original, exist_ok=True)
os.makedirs(dataset_folder_validation, exist_ok=True)

# Create patches
height, width, _ = image_drawn.shape
for patch_size in patch_sizes:
    for y in range(0, height - patch_size, patch_size - padding):
        for x in range(0, width - patch_size, patch_size - padding):
            # Define the patch corners
            corners = [
                (y, x),
                (y, x + patch_size - 1),
                (y + patch_size - 1, x),
                (y + patch_size - 1, x + patch_size - 1),
                (y + patch_size // 2, x + patch_size // 2) # check the center of the image
            ]

            # Check if all corners have a non-black pixel within the range
            if all(corner_has_color(image_drawn, corner, corner_range) for corner in corners):
                patch_drawn = image_drawn[y:y+patch_size, x:x+patch_size]
                patch_filename_drawn = os.path.join(dataset_folder_drawn, f'patch_drawn_{y}_{x}.png')
                cv2.imwrite(patch_filename_drawn, patch_drawn)
                
                patch_original = image_original[y:y+patch_size, x:x+patch_size]
                patch_filename_original = os.path.join(dataset_folder_original, f'patch_original_{y}_{x}.png')
                cv2.imwrite(patch_filename_original, patch_original)
            else:
                patch_original = image_original[y:y+patch_size, x:x+patch_size]
                patch_filename_validation = os.path.join(dataset_folder_validation, f'patch_validation_{y}_{x}.png')
                cv2.imwrite(patch_filename_validation, patch_original)               