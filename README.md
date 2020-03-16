## Email Queue Worker

1. Check for new message
2. Read message
3. Check for two attached images
4. Create a directories for the job
5. Create a job file for the job
6. Download attached images to job directory


## Job Queue Worker

1. Check to see if a job is running
2. Start the new job
3. Check to see if job is complete
4. Create email response and attach output images
5. Update job file


## Job File

```
email: someone@somewhere.com
status: new
```
