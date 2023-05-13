import os
import random
import shutil

# Set the path to the original folder containing the images
folder_path = "C://Users/Lauren/Downloads/FY Project Datasets/FERtest/fear"

# Get a list of all the image filenames in the folder
image_filenames = [filename for filename in os.listdir(folder_path) if filename.endswith(".jpg")]

# Shuffle the list of image filenames randomly
random.shuffle(image_filenames)

# Select a random sample of 700 image filenames
sample_filenames = random.sample(image_filenames, 700)

# Create a new folder to store the sample images
sample_folder_path = "C://Users/Lauren/Downloads/FY Project Datasets/FERsubsets/test/fear"
os.makedirs(sample_folder_path, exist_ok=True)

# Copy the sample images to the new folder
num_copied = 0
for i, filename in enumerate(sample_filenames, 1):
    src_path = os.path.join(folder_path, filename)
    dst_path = os.path.join(sample_folder_path, filename)
    shutil.copy(src_path, dst_path)
    num_copied += 1
    if num_copied % 10 == 0:
        print(f"Copied {num_copied} images, {len(sample_filenames) - num_copied} left to copy.")
print("Finished copying images.")
