import os
import subprocess
import shlex
import smtplib
import imghdr
from email.message import EmailMessage

from config import config

# Read job file
f = open(f"{config['job_dir']}/job.txt", "r")
email = f.readline().split(":")[1].rstrip()
style = f.readline().split(":")[1].rstrip()
content = f.readline().split(":")[1].rstrip()
output = f.readline().split(":")[1].rstrip()
f.close()

# Launch neural-style 
# TODO: Externalize or otherwise make this less hard-codey
command_line = f"/home/jason/torch/install/bin/th /home/jason/neural-style/neural_style.lua -style_image {style} -content_image {content} -output_image {output} -gpu -1"
args = shlex.split(command_line)
subprocess.run(args, cwd=config.neural_style_dir)

# Email output
message = EmailMessage()
message['Subject'] = "Done"
message['From'] = config["email"] 
message['To'] = email

with open(output, "rb") as fp:
    output_data = fp.read()
message.add_attachment(output_data, maintype="image", subtype=imghdr.what(None, output_data))

s = smtplib.SMTP(f"{config['smtp_server']}:{config['smtp_port']}")
s.ehlo()
s.starttls()
s.login(config["email"], config["password"])
s.send_message(message)
s.quit()

# Delete job file
os.remove(f"{config['job_dir']}/job.txt")
