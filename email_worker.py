import os
import shlex
import subprocess
import imaplib
import email

from config import config

# Check to see if a job is running
if not os.path.exists(f"{config['job_dir']}/job.txt"):

    # Check for new messages
    mailbox = imaplib.IMAP4_SSL(config["imap_server"])
    mailbox.login(config["email"], config["password"])
    mailbox.select()
    result, data = mailbox.uid("search", None, "UNSEEN")

    if result == "OK":
        # Only read one of these at a time
        message_count = len(data[0].split())
        # TODO: Find a way to let new submissions know the queue length
        if message_count > 0:
        #for message_num in data[0].split():
            message_num = data[0].split()[0]
            typ, message_data = mailbox.uid("fetch", message_num, "(RFC822)")
            raw_message = message_data[0][1]
            email_message = email.message_from_bytes(raw_message)
            email_from = email.utils.parseaddr(email_message["From"])
            email_address = email_from[1]
            email_subject = email_message["Subject"]

            # Create a directory for the job
            # TODO: Make sure we have what we need before creating this
            # TODO: Make sure this doesn't exist before we try
            # TODO: Exit gracefully if any of this goes south
            job_dir = f"{config['job_dir']}/{message_num.decode('utf-8')}"
            os.makedirs(job_dir)

            # Here we walk the message and write-out the attached files
            filenames = []
            for part in email_message.walk():
                filename = part.get_filename()
                if filename:
                    if filename.lower().find(".jpeg") > 0 or filename.lower().find(".jpg") > 0 or filename.lower().find(".png") > 0:
                        if filename:
                            filenames.append(filename)
                            f = open(os.path.join(job_dir, filename), "wb")
                            f.write(part.get_payload(decode=True))
                            f.close()

            # Create the job file
            f = open(os.path.join(config["job_dir"], "job.txt"), "w")
            f.write(f"email:{email_address}\n")
            f.write(f"style:{job_dir}/{filenames[0]}\n")
            f.write(f"content:{job_dir}/{filenames[1]}\n")
            f.write(f"output:{job_dir}/out.png\n")
            f.close()

            # Launch the job
            command_line = "python ./job_worker.py"
            args = shlex.split(command_line)
            subprocess.Popen(args)

            # TODO: Send job begins notification email
