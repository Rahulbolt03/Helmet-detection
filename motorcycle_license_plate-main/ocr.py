import cv2
import easyocr
import numpy as np
import pyttsx3

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

def process_image(image_path, threshold=0.5):
    # Read image using OpenCV
    img = cv2.imread(image_path)

    # Detect text on image
    text_results = reader.readtext(image_path)

    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # Adjust speech properties for clarity
    engine.setProperty('rate', 150)  # Set speech rate (words per minute)
    engine.setProperty('volume', 1.0)  # Set volume level (0.0 to 1.0)

    # Select a female voice for clearer pronunciation
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    # Speak out the detected text using text-to-speech
    for bbox, text, score in text_results:
        if score >= threshold:
            engine.say(text)

    # Wait for speech to complete
    engine.runAndWait()

if __name__ == "__main__":
    # Specify the image path (use raw string or escape backslashes)
    image_path = r'C:\Users\rahul\Downloads\home surveillance\demopic2.jpg'

    # Process the image and initiate text-to-speech with adjusted settings for clarity
    process_image(image_path)
