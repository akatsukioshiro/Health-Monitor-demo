import logging
try:
    logging.basicConfig(filename='LOG_runtime.log', filemode='a', format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
except FileNotFoundError:
    with open("runtime.log","w+") as f:
        f.write("")
    logging.basicConfig(filename='LOG_runtime.log', filemode='a', format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
except Exception as e:
    print(e)

try:
    import smtplib 
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import json
except Exception as e:
    print(e)
    logging.critical(str(e))

try:
    with open("CONFIG_email_user.json","r") as f:
        userD=json.loads(f.read().replace("'","\""))
    with open("CONFIG_email_admin.json","r") as f:
        serverD=json.loads(f.read().replace("'","\""))
    with open("CONFIG_email_message.txt","r") as f:
        messageD=f.read()
except FileNotFoundError as e:
    print(e)
    logging.critical(str(e))
    print("Exiting ...")
    exit()

  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
try:
    s.login(serverD["email"], serverD["pass"]) 
except smtplib.SMTPAuthenticationError as e:
    print(e)
    logging.error(str(e))
except KeyError as e:
    print(e)
    logging.error(str(e))
    

msg = MIMEMultipart()
msg['From'] = userD["title"]
msg['To'] = ",".join(userD["receiver_email"])
msg['Subject'] = userD["subject"]

body = messageD
msg.attach(MIMEText(body,'plain'))

# message to be sent 
message = msg.as_string()
logging.info(str(message))
  
# sending the mail 
s.sendmail(serverD["email"], userD["receiver_email"], message) 
  
# terminating the session 
s.quit() 
