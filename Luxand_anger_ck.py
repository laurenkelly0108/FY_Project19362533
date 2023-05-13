import os
import requests
import json
import csv

API_TOKEN = "0f359a5a9fae4f14bc3dee9074551505"

# Set image directory path
image_directory = "C://Users/Lauren/Downloads/FY Project Datasets/CK+48/anger"

# Set output directory paths
csv_directory = "C://Users/Lauren/Downloads/RESULTS/CK/LUXAND/CSV"
json_directory = "C://Users/Lauren/Downloads/RESULTS/CK/LUXAND/JSON"

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

# Loop through the images in the folder
for filename in os.listdir(image_directory):
    # Skip any non-image files
    if not filename.endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Set the image file path and name
    image_file = os.path.join(image_directory, filename)
    image_name = os.path.splitext(filename)[0]

    # Detect emotions in the image using Luxand
    result = emotions(image_file)

    if result is not None:
        # Write the result to the CSV file
        with open(os.path.join(csv_directory, 'ANGER_LUXresults.csv'), mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([image_name, result])
        
        # Write the result to a JSON file
        with open(os.path.join(json_directory, f'{image_name}.json'), mode='w') as json_file:
            json.dump(result, json_file)
            
        print(f"Results for {image_name} written to CSV and JSON.")
    else:
        # Write "no result" to the CSV file
        with open(os.path.join(csv_directory, 'ANGER_LUXresults.csv'), mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([image_name, "no result"])
        
        print(f"No results for {image_name}.")

print("done")
