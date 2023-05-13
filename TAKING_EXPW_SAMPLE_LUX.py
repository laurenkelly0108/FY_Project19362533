import os
import random
import shutil
from tqdm import tqdm

# Source and destination directories
source_dir = "C://Users/Lauren/Downloads/FY Project Datasets/ExpwSubset/SADNESS_subsetExpw"
destination_dir = "C://Users/Lauren/Downloads/FY Project Datasets/ExpwLUXSubset/sad"

# Number of images to select
sample_size = 3500

# Get a list of all image files in the source directory
image_files = [file for file in os.listdir(source_dir) if file.endswith(('.jpg', '.jpeg', '.png'))]

# Randomly select the required number of images
selected_images = random.sample(image_files, sample_size)

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Copy the selected images to the destination directory and display a progress bar
for image_file in tqdm(selected_images, desc="Copying Images"):
    source_path = os.path.join(source_dir, image_file)
    destination_path = os.path.join(destination_dir, image_file)
    shutil.copy2(source_path, destination_path)
