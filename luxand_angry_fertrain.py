import os
import requests
import json
import csv
from tqdm import tqdm

API_TOKEN = "0f359a5a9fae4f14bc3dee9074551505"

# Set image directory path
image_directory = "C://Users/Lauren/Downloads/FY Project Datasets/FERsubsets/train/angry"

# Set output directory paths
csv_directory = "C://Users/Lauren/Downloads/RESULTS/FER/train/LUXAND/CSV"
json_directory = "C://Users/Lauren/Downloads/RESULTS/FER/train/LUXAND/JSON"

print("START")

# Create the output folder paths if they don't exist
os.makedirs(csv_directory, exist_ok=True)
os.makedirs(json_directory, exist_ok=True)

def emotions(image_path):
    url = "https://api.luxand.cloud/photo/emotions"
    headers = {"token": API_TOKEN}

    if image_path.startswith("https://"):
        files = {"photo": image_path}
    else:
        files = {"photo": open(image_path, "rb")}

    response = requests.post(url, headers=headers, files=files)
    result = json.loads(response.text)

    if response.status_code == 200:
        return result
    else:
        print("Can't recognize people:", response.text)
        return None

print("START")

# Get the list of image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Create a progress bar
pbar = tqdm(total=len(image_files))

# Define the header for the CSV file
csv_header = ["Image Name", "Status", "Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"]

# Write the header to the CSV file
with open(os.path.join(csv_directory, 'ANGER_LUX_FER_train_results.csv'), mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_header)

# Loop through the images in the folder
for filename in image_files:
    # Set the image file path and name
    image_file = os.path.join(image_directory, filename)
    image_name = os.path.splitext(filename)[0]

    # Detect emotions in the image using Luxand
    result = emotions(image_file)

    if result is not None:
        # Check if there are faces in the photo
        if result["status"] == "failure":
            # Write the result to the CSV file with "no result" for the emotions
            with open(os.path.join(csv_directory, 'ANGER_LUX_FER_train_results.csv'), mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([image_name, result["status"], 0, 0, 0, 0, 0, 0, 0, 0])
            
        else:
            # Check if there are emotions in the result
            if result["faces"]:
                # Write the result to the CSV file
                with open(os.path.join(csv_directory, 'ANGER_LUX_FER_train_results.csv'), mode='a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([image_name, result["status"], result["faces"][0]["emotions"].get("anger", 0), result["faces"][0]["emotions"].get("contempt", 0), result["faces"][0]["emotions"].get("disgust", 0), result["faces"][0]["emotions"].get("fear", 0), result["faces"][0]["emotions"].get("happiness", 0), result["faces"][0]["emotions"].get("neutral", 0), result["faces"][0]["emotions"].get("sadness", 0), result["faces"][0]["emotions"].get("surprise", 0)])

            else:
                # Write the result to the CSV file with "no result" for the emotions
                with open(os.path.join(csv_directory, 'ANGER_LUX_FER_train_results.csv'), mode='a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([image_name, result["status"], 0, 0, 0, 0, 0, 0, 0, 0])
                

    else:
        # Write "no result" to the CSV file with "0" for the emotions
        with open(os.path.join(csv_directory, 'ANGER_LUX_FER_train_results.csv'), mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([image_name, "no result", 0, 0, 0, 0, 0, 0, 0, 0])
        

    # Update the progress bar
    pbar.update(1)

# Close the progress bar
pbar.close()

print("done")
