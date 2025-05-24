import smtplib
from email.mime.text import MIMEText
from string import Template
import os
from dotenv import load_dotenv # type: ignore
import openai # type: ignore
import ollama # type: ignore

load_dotenv(dotenv_path="C:/Users/91956/Desktop/cold mail/log/cr.env")

EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
#print("Email:", EMAIL_ADDRESS)
#print("Password:", repr(EMAIL_PASSWORD))

def read_template(filename):
    with open(filename,'r') as file:
        return Template(file.read())
def send_email(to_email, subject, body):
    msg = MIMEText(body, 'plain')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)        

def generate_email_llm(name, product, discount,sender='ABC Company'):
    prompt = f"""
    Write a concise cold email to {name} offering a {discount}% discount on our product '{product}'.
    The tone and format should be friendly but professional.Include a compelling subject line and soft call to action.give my name as safeer and contact number as 1234567890.the mail must be in single paragraph.not give the link of the programme tell them only to contact the number
    - The sign-off must be next line: "Best regards,\n{sender}"
    Return output in this format:

    Subject: <subject line>
    <email body>
    """

    response = ollama.chat(model='mistral', messages=[
        {"role": "user", "content": prompt}
    ])

    return response['message']['content']   