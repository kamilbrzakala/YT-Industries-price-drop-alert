import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from cryptography.fernet import Fernet
import os

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def load_key():
    return open("key.txt", "rb").read()
    
def decrypt_password(encrypted_password):
    key = load_key()
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password
    
# Function to send email
def send_email(price, pw):
    # Email configurations
    sender_email = "xxxxx@xxxx.com"  # Replace with your email
    receiver_email = "xxxxx@xxxx.com"  # Replace with recipient email

    # Create message object instance
    msg = MIMEMultipart()

    # Setup the parameters of the message
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Price Alert: The price of the product has changed!"

    # Create the body of the message
    body = f"The price of the product has changed from €7,499.00 to: {price}"

    # Attach the body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('serwer2365163.home.pl', 587)  # Use your email provider's SMTP server and port
    session.starttls()  # Enable security
    session.login(sender_email, pw)  # Login with your email and password
    text = msg.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()

    print("Email sent successfully!")

# Define the URL of the website
url = "https://www.yt-industries.com/products/bikes/decoy-29/core-4/680/decoy-29-core-4/"  # Replace with the actual URL of the website

with open("C:\\Users\\xxxx\\pw.txt", "rb") as password_file:
    encrypted_password = password_file.read()
decrypted_password = decrypt_password(encrypted_password)

while True:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div element with class "yind-bike-price-container"
        price_container = soup.find('div', class_='yind-bike-price-container')
        
        # Check if the price container is found
        if price_container:
            # Find the h3 element with class "ytind-bike-price" within the price container
            price_element = price_container.find('h3', class_='ytind-bike-price')
            
            # Check if the price element is found
            if price_element:
                # Get the price text
                price = price_element.text.strip()
             
                # Check if the price is different from €7,499.00
                if price != "€7,499.00":
                    # Send email notification
                    print(Color.BOLD + "Price DROPPPED!!: " + Color.ENDC, Color.OKGREEN + price + Color.ENDC)
                    send_email(price,decrypted_password)
                else:
                    print("Price:", price)
            else:
                print("Price element not found.")
        else:
            print("Price container not found.")
    else:
        print("Failed to retrieve website. Status code:", response.status_code)
    # Wait for 15 minutes before checking again
    time.sleep(900)  # 15 minutes = 900 seconds
