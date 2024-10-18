import cv2
import os
import pytesseract
from PIL import Image
from tabulate import tabulate
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            extracted_text = pytesseract.image_to_string(img)

            # Clean up extracted text
            extracted_text = extracted_text.replace('.', '').replace(',', '').replace(' ', '').replace('-', '')
            if len(extracted_text) > 1 and extracted_text[:2] != 'TN':
                extracted_text = extracted_text[1:]

            return extracted_text.strip()
    except Exception as e:
        print(f"Error processing image '{image_path}': {e}")
        return ''

# Function to check bike number against database and send email if rider is detected without a helmet
def check_bike_number_with_database(bike_number):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Why2change-_-",
            database="student"
        )
        cursor = connection.cursor()
        query = "SELECT Name, RegisterNum, Department, Email FROM student_info WHERE Bikeno = %s"
        cursor.execute(query, (bike_number,))
        result = cursor.fetchone()

        if result:
            name, register_num, department, email = result
            data = [[name, register_num, department, email]]
            headers = ["Name", "Register Number", "Department", "Email"]
            print(tabulate(data, headers=headers, tablefmt="pretty"))

            # Send email if helmet is not detected
            send_email_if_helmet_not_detected(name, email, bike_number)

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

# Function to send email if helmet is not detected
def send_email_if_helmet_not_detected(name, email, bike_number):
    sender_email = "ragulrtr1902@gmail.com"  # Update with your email address
    receiver_email = email
    password = "jesus25&"  # Update with your email password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f"Helmet Alert: Rider {name} ({bike_number}) Detected Without Helmet"

    body = f"Dear {name},\n\nThis is to inform you that you have been detected riding without a helmet (Bike Number: {bike_number}). Please ensure safety measures while riding.\n\nBest regards,\nYour Name"
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Update with your SMTP server details
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Email notification sent to {email} regarding helmet violation")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main script
folder_path = 'number_plates'

if not os.path.exists(folder_path):
    print(f"Folder '{folder_path}' not found.")
else:
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            extracted_text = extract_text_from_image(image_path)

            if extracted_text and extracted_text.startswith('TN'):
                print(f"Image name: {filename}, Number plate: {extracted_text}")
                check_bike_number_with_database(extracted_text)

print("License plate recognition complete.")
