import os
import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Use Tesseract OCR to extract text from the image
            extracted_text = pytesseract.image_to_string(img)

            # Remove dots, commas, spaces, and '-' from the extracted text
            extracted_text = extracted_text.replace('.', '').replace(',', '').replace(' ', '').replace('-', '')

            if len(extracted_text) > 1 and extracted_text[:2] != 'TN':
                extracted_text = extracted_text[1:]

            return extracted_text.strip()
    except Exception as e:
        print(f"Error processing image '{image_path}': {e}")
        return ''

# Folder containing the images of number plates
folder_path = 'number_plates'

# Verify folder path exists
if not os.path.exists(folder_path):
    print(f"Folder '{folder_path}' not found.")
else:
    # Iterate through each image file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust based on your image file types
            # Build the full path to the image
            image_path = os.path.join(folder_path, filename)

            # Extract text from the image
            extracted_text = extract_text_from_image(image_path)

            # Check if extracted text is not empty and starts with 'TN'
            if extracted_text and extracted_text.startswith('TN'):
                # Print the image name and extracted text
                print(f"Image name: {filename}, Number plate: {extracted_text}")

print("License plate recognition complete.")
