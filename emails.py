import smtplib
from email.mime.text import MIMEText
from string import Template
import os
from dotenv import load_dotenv # type: ignore
import ollama # type: ignore

load_dotenv(dotenv_path="D:\cold mail\log\cr.env")

EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
#print("Email:", EMAIL_ADDRESS)
#print("Password:", repr(EMAIL_PASSWORD))
'''
def read_template(filename):
    with open(filename,'r') as file:
        return Template(file.read())
'''        
def send_email(to_email, subject, body):
    msg = MIMEText(body, 'plain')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)        

def generate_email_llm(name, product, discount, sender='ABC Company', contact='1234567890'):
    prompt = f"""
    You are the HR system for {sender}. Write a professional, polite, and clear application acknowledgment email to a student named {name}.
    The candidate have {discount} for the course {product}. Include the following

    Requirements:
    - starting with Add an engaging subject line (start with an emoji or symbol like 🎯, 💡, 🎁, or 🔥).
    - Greet the candidate by like Dear {name}.
    - Add a clear and compelling subject line
    - Include a greeting and a short intro about the offer
    - Explain the value/benefit of the product in 2-3 sentences
    - Encourage the user to contact Safeer at {contact} to learn more or sign up
    - No links or URLs
    - Use line breaks and paragraph spacing (not a single paragraph)
    - Do NOT include email headers or formatting like "To" or "From".

    Best regards,  
    {sender}  
    {contact}

    Format the response as:
    Subject: Exciting Offer on the course{product}

    <email body>
    """

    response = ollama.chat(model='mistral', messages=[
        {"role": "user", "content": prompt}
    ])

    return response['message']['content']