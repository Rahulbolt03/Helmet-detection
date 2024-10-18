import mysql.connector
import os
import pytesseract
from PIL import Image
from tabulate import tabulate


def extract_text_from_image(image_path):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Use Tesseract OCR to extract text from the image
            extracted_text = pytesseract.image_to_string(img)

            # Remove dots, commas, spaces, and '-' from the extracted text
            extracted_text = extracted_text.replace('.', '').replace(',', '').replace(' ', '').replace('-', '')

            # Ensure the first two characters are 'TN', otherwise remove the first character
            if len(extracted_text) > 1 and extracted_text[:2] != 'TN':
                extracted_text = extracted_text[1:]

            return extracted_text.strip()
    except Exception as e:
        print(f"Error processing image '{image_path}': {e}")
        return ''


def check_bike_number_with_database(bike_number):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Why2change-_-",
            database="student")

        # Execute a SELECT query to check if the bike number exists in the database
        cursor = connection.cursor()
        query = "SELECT Name, RegisterNum, Department, Email FROM student_info WHERE Bikeno = %s"  # Modified query
        cursor.execute(query, (bike_number,))
        result = cursor.fetchone()

        if result:
            name, register_num, department, email = result  # Include email in result tuple
            data = [[name, register_num, department, email]]  # Include email in the data list
            headers = ["Name", "Register Number", "Department", "Email"]  # Include email in the headers list
            print(tabulate(data, headers=headers, tablefmt="pretty"))
        else:
            print("Bike number not found in the database")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("Database connection closed")


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
                print(f"Image name: {filename}, Number plate: {extracted_text}")
                # Check bike number with database
                check_bike_number_with_database(extracted_text)

print("License plate recognition complete.")
