import boto3
import csv
import json
import os

# Specify the AWS region
region = 'us-east-1'

# Set the AWS profile name
profile_name = '19362533'

# Create a Boto3 session using the AWS profile
session = boto3.Session(profile_name=profile_name)

# Initialize the AWS Rekognition client using the Boto3 session
client = session.client('rekognition', region_name=region)

# Initialize S3 resource using the Boto3 session
s3 = session.resource('s3', region_name=region)

# Specify the S3 bucket name
bucket_name = '19362533project'

# Specify the folder path for the images to analyze
folder_path = 'C://Users/Lauren/Downloads/FY Project Datasets/FERtest/angry'

# Specify the output folder paths for the CSV and JSON files
csv_output_folder = 'C://Users/Lauren/Downloads/RESULTS/FER/test/AWS/CSV'
json_output_folder = 'C://Users/Lauren/Downloads/RESULTS/FER/test/AWS/JSON'

print("START")

# Create the output folder paths if they don't exist
os.makedirs(csv_output_folder, exist_ok=True)
os.makedirs(json_output_folder, exist_ok=True)

# Initialize the emotions dictionary
emotions = {}

# Loop through the images in the folder
for filename in os.listdir(folder_path):
    # Skip any non-image files
    if not filename.endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Set the image file path and name
    image_file = os.path.join(folder_path, filename)
    image_name = os.path.splitext(filename)[0]

    # Upload the image to S3
    s3.Bucket(bucket_name).upload_file(image_file, f'FERtest/angry/{filename}')

    # Detect faces and emotions in the image using AWS Rekognition
    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket_name, 'Name': f'FERtest/angry/{filename}'}}, Attributes=['ALL'])

    # Extract the emotions detected and their confidence levels
    emotions[image_name] = {}
    for face in response['FaceDetails']:
        for emotion in face['Emotions']:
            emotions[image_name][emotion['Type']] = emotion['Confidence']

    # Write the response to a JSON file
    with open(os.path.join(json_output_folder, f'AWS - {filename}.json'), 'w') as json_file:
        json.dump(response, json_file)

# Write the emotions and confidence levels to a CSV file
with open(os.path.join(csv_output_folder, 'ANGER_AWS_FERresults.csv'), mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Image Name', 'HAPPY', 'SURPRISED', 'FEAR', 'SAD', 'ANGRY', 'DISGUSTED', 'CONFUSED', 'CALM'])
    for image_name, emotion_values in emotions.items():
        writer.writerow([image_name, emotion_values.get('HAPPY', ''), emotion_values.get('SURPRISED', ''), emotion_values.get('FEAR', ''), emotion_values.get('SAD', ''), emotion_values.get('ANGRY', ''), emotion_values.get('DISGUSTED', ''), emotion_values.get('CONFUSED', ''), emotion_values.get('CALM', '')])

print("DONE")