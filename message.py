from email.message import EmailMessage
import ssl
import smtplib

email_sender = 'vinhnguyensj01@gmail.com'
email_password = 'pogeyfrqdvqxzoex'

email_receiver = 'vinhnguyensj01@gmail.com'

subject = "Hello world"
body = """
This is a test message
"""
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())