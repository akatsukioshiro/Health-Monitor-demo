Installation Steps:

1. Setup Commands (Auto sets flask ipaddress) and port to 5001

py/python.exe/python3/python SETUP_flask.py -port 5001

2. Setup Commands (Manually sets flask ipaddress) and port to 5001

py/python.exe/python3/python SETUP_flask.py -ip 192.168.1.10 -port 5001

3. CONFIG_configuration.json sets up arduino ipaddress,identity_email,access point email and pass,wifi email and pass.

4. Post filling CONFIG_configuration.json, run:

py/python.exe/python3/python SETUP_arduino_setup.py

5. Email connection to Gmail needs following setup:

  a. Enable Less Secure apps as shown here "python_gmail_app_access.png".
  b. Configure CONFIG_email_admin.json for sender details.
  c. Configure CONFIG_email_user.json for receiver details.
  d. Configure CONFIG_email_message.txt for message body.

6. View LOG_runtime.log for errors.

7. Show current ipaddress:

py/python.exe/python3/python SETUP_flask.py -get ip

8. Libraries Used:

argparse
datetime
email.mime.multipart
email.mime.text
flask
jinja2
json
logging
smtplib
socket
subprocess
time
urllib.request

Thank You
