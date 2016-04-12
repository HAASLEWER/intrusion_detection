def send_email(user, pwd, recipient, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    gmail_user = user
    gmail_pwd = pwd

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = user
    msg['Reply-to'] = user
    msg['To'] = recipient
    msg.preamble = 'Multipart massage.\n'

    # This is the textual part:
    part = MIMEText(body)
    msg.attach(part)

    # This is the binary part(The Attachment):
    part = MIMEApplication(open("intrusion.png","rb").read())
    part.add_header('Content-Disposition', 'attachment', filename="intrusion.png")
    msg.attach(part)    

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.close()
