import smtplib, ssl
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "my@gmail.com"
#password = input("Type your password and press enter: ")

# Send an OpsGenie Alert email
# See https://realpython.com/python-send-email/#sending-a-plain-text-email
def lambda_handler(event, context):

        # Create a secure SSL context
    #context = ssl.create_default_context()

    # Try to log in to server and send email
    #try:
    #    server = smtplib.SMTP(smtp_server,port)
    #    server.ehlo() # Can be omitted
    #    server.starttls(context=context) # Secure the connection
    #    server.ehlo() # Can be omitted
    #    server.login(sender_email, password)
    #    # TODO: Send email here
    #except Exception as e:
        # Print any error messages to stdout
    #    print(e)
    #finally:
    #    server.quit() 

    subject = 'Testing'
    body = 'Testing Trace3 Integration with Opsgenie'
    fromaddr = ['damien.gallagher@gmail.com']
    toaddr =  ['trace3_testops@csx.opsgenie.net']
    message = MIMEMultipart('mixed')
    message['Subject'] = subject
    message['From'] = ", ".join(fromaddr)
    message['To'] = ", ".join(toaddr)
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()
    server = smtplib.SMTP('smtp.csx.com', 25)
    server.ehlo()
    server.starttls()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return "Email Sent"


