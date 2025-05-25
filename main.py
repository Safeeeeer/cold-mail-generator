import csv
import os
from datetime import datetime
from emails import generate_email_llm
from emails import send_email #read_template --import this when you are not using the llm model for the customized template.

#TEMPLATE_PATH = 'template/dis.txt'
CSV_PATH = 'customer/customer.csv'
LOG_FILE = 'log/cr.env'

# Load template
#template = read_template(TEMPLATE_PATH) (uncomment this wheh you import the read_template)

# Open log file
os.makedirs('logs', exist_ok=True)
log = open(LOG_FILE, 'a', newline='')
log_writer = csv.writer(log)

# Read customer CSV
with open(CSV_PATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        personalized = generate_email_llm(
     name=row['FirstName'],
     product=row['Product'],
     discount=row['Discount']
)

        subject = personalized.splitlines()[0].replace("Subject: ", "")
        body = "\n".join(personalized.splitlines()[1:])

        try:
            send_email(row['Email'], subject, body)
            log_writer.writerow([datetime.now(), row['Email'], "Sent"])
            print(f"✅ Sent to {row['Email']}")
        except Exception as e:
            log_writer.writerow([datetime.now(), row['Email'], f"Failed: {str(e)}"])
            print(f"❌ Failed for {row['Email']}: {str(e)}")

log.close()