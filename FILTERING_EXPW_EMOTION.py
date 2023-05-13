import os
import shutil
import pandas as pd
from tqdm import tqdm

# Set the source directory where the original images are located
source_dir = 'C://Users/Lauren/Downloads/FY Project Datasets/ExpwCleaned/'

# Set the target directory where the subset folders will be created
target_dir = 'C://Users/Lauren/Downloads/FY Project Datasets/ExpwSubset/'

# Set the subset name and CSV file containing the list of image names for the subset
subset_name = 'ANGER'
csv_file = 'C://Users/Lauren/Downloads/ExpWtest/Output/ANGER_domemot.csv'

# Create the subset directory if it doesn't already exist
subset_dir = os.path.join(target_dir, subset_name + '_subsetExpw')
if not os.path.exists(subset_dir):
    os.makedirs(subset_dir)

# Read the CSV file into a pandas dataframe
df = pd.read_csv(csv_file, header=None)

# Loop through each row in the dataframe
for index, row in tqdm(df.iterrows(), total=len(df)):
    # Get the image name from the dataframe
    image_name = row[0]

    # Skip over the .DS_Store file if it exists
    if image_name == '.DS_Store':
        continue

    # Set the source and target file paths for the current image
    source_file = os.path.join(source_dir, image_name)
    target_file = os.path.join(subset_dir, image_name)

    # Copy the image to the subset directory
    shutil.copyfile(source_file, target_file)

# Print completion message
print(f"All {subset_name} subset images have been successfully copied to {subset_dir}.")
