import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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