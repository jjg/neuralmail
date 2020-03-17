# Neuromail

An email-based job scheduler for processing images using neural-style.

## TODO:

* ~~There may be a bug when more than one email is in the queue...~~
* ~~Externalize email config~~
* ~~Make paths configurable~~
* ~~Create dedicated email account~~
* Delete emails from account when job completes to save room on server
* ~~Logging?~~
* Make sure email has two images to work with before processing
* Keep track of processing time, etc.
* Write a better email notification
* Genrify this whole thing so it can be used to schedule other programs
* Include all output images in the notification email
* Job submission feedback email (queue position???)

## Components

### Email Queue Worker
1. Check for running job (only one at a time for now)
2. Check for new message
3. Read message
4. Check for two attached images
5. Create a directories for the job
6. Download attached images to job directory
7. Create a job file for the job
8. Start the job

### Job Queue Worker
1. Parse job file
2. Start neural-style
3. Create email response and attach output images
4. Delete job file

### Job File
```
email:someone@somewhere.com
style:/path/to/style.jpg
content:/path/to/content.jpg
output:/path/to/out.png
```

# References

* https://stackoverflow.com/questions/1685157/how-can-i-specify-working-directory-for-popen
* https://github.com/jcjohnson/neural-style
* https://docs.python.org/3/library/email.examples.html
* https://docs.python.org/3.7/library/email.message.html
* https://stackoverflow.com/questions/275018/how-can-i-remove-a-trailing-newline
* https://docs.python.org/3.5/library/subprocess.html#using-the-subprocess-module
* https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
* https://docs.python.org/3.7/library/email.parser.html#module-email.parser
* https://docs.python.org/3.7/library/imaplib.html
* https://github.com/jjg/preposter.us/blob/master/preposter.us.py

