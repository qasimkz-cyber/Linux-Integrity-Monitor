Project Diary: Linux Integrity Monitor

Here's my log of thoughts and new things I learned during this project.

Phase 1: Environment Setup & Project Initialization

mkdir creates a new folder; I don't want to keep forgetting this stuff. 

cd x will go into the folder x. I then wanted to create my virtual environment within that folder so all my tools and functionality are specific to that folder and don't spill outwards.

Luckily, I don't need to install any external libraries to connect my Python program to the OS; it seems Python already has a built-in library to do so.  But it is best practice to create a 

venv anyway.

To work with Linux systems and the Linux environment for this project, I will be using WSL, which lets me run a Linux terminal on my Windows computer. 

I used Git Bash for my security header project, and since I didn't need direct interaction with the Linux system for that project's functionalities, it was fine. Different story here! We're moving up, so cool! 

I had trust issues with WSL. I have to enable virtualization through my BIOS to use it and I don't want my gaming performance affected. But, it should not be an issue if closed properly. Remember: 

wsl --shutdown in Command Prompt to close it immediately. 

It seemed like WSL's list of available software was out of date, so I had to remind it what the available software was by using sudo apt update. Now I will try to install the package used for creating a venv. My first attempt to create a venv failed, so there are incomplete folders. I want to remove them using rm -r venv. I can activate my 

venv by using source venv/bin/activate. 

Phase 2: Figuring Out the Hashing Logic

After I activate my venv, I should create my Python file. After that, I should think of what files I will make this secure baseline for.  Then I need to understand why I'm using SHA-256 and not other hashing algorithms, and what SHA-256 even is. After that, before the actual implementation, I should connect my GitHub repository. 


touch is how you create a new file, it seems, within a folder.

I clearly want to pick the most important files. Firstly, there are system binaries. These are the essential files that the system runs, so if an attacker gets a hold of these files, then they can pretty much control the system's core behavior. From my research, such files include: 

/bin/bash (the command shell itself), /bin/ls (the command to list files), and /usr/bin/ssh (the SSH client for secure remote connections). 

There are also the configuration files, which control user access and system settings. Again from research, I know a couple: /etc/passwd (the list of all user accounts) and /etc/shadow (the encrypted passwords for those users).

The modern secure encryption hashing algorithms are a part of the SHA family.  From what I gathered, it seems it's between SHA-256 and SHA-512. Apparently, SHA-512 is more secure since it produces a longer hash, with less chance of collision and brute-force attacks. I will use SHA-256. Even though I'm on a 64-bit system and SHA-512 should be faster, I don't think it matters for what we are doing. SHA-256 is apparently an industry standard, so I'll go with it. 


I learned some things about the SHA-256 object:

.update(): This function will essentially be the function that feeds our data (in bytes only) to our hashing algorithm. You can call it multiple times; that's how we process data chunk by chunk. 

.hexdigest(): After you've fed all your data into the object, you call this function and it will return the hash value as a 64-character hexadecimal string. Cool. 

To create a new hash value for a new file, I will be forced to create a brand new hash object. So there's no way to reuse the same object. I thought there would be a way to "clean" the current pipeline, if that makes sense. 

The standard procedure to hash the contents of a file is by feeding the hashing algorithm the contents chunk by chunk instead of giving it all the data at once. Apparently, going byte by byte is very inefficient and will take a very long time to process. We have enough memory to go chunk by chunk. We want to process 4096 bytes at a time because it aligns with the architecture of most modern systems, hence it's most efficient and will give good performance. 

What if the data cannot be divided by 4096? Apparently, in Python, the next time you call the 

read method with 4096 as an argument, if there are less than 4096 bytes remaining, it will return them all. If there are no bytes, it will return 

b"". 

Phase 3: Storing the Baseline (JSON & try...except)

We need to store our secure baselines of the files that we create somewhere. We know that if we store it somewhere like a dictionary in Python, every time the script is re-ran the dictionary will be rendered empty.  Hence, our secure baselines would be erased, which is an issue since it would keep creating new secure baselines every time the script ran. Big issue. Hence we need to store that dictionary somewhere safe and secure. 


Apparently, we can use a JSON file to store our dictionary. There are alternative files like CSV and Pickle. JSON provides a direct mapping and is a perfect fit for dictionaries, while CSV will have issues with the formatting and we would have to add and modify things ourselves, and Pickle has security risks. 

Now the issue with JSON is that if our script adds any whitespace to the file accidentally, JSON might indicate it isn't empty when it really conceptually is. To make our code as robust as possible, we should handle this. 

Some learning about methods: 

json.dump() will store and save our data, while json.load() will retrieve and return our data. Also, JSON preserves the data type, so when I call 

json.load() it will return the specified data in the correct and accurate format as it was before being stored in the JSON file. 

The first issue is, as we noted earlier, if the JSON file is empty or contains whitespace and we try to load anything, it will cause an error. So a safe and secure practice would be to try to load the contents of the file. If nothing exists or there's only whitespace, we get an error, and I can gracefully catch that error using the 

try-catch block. 

I want to catch two specific errors: 

json.JSONDecodeError (occurs when we attempt json.load() if the file is empty or contains whitespace) and FileNotFoundError (occurs if the file doesn't even exist).  I'll add a 

try-catch for this. Clearly, if we don't get any errors caught, we compare the secure baseline. Else, we create a new secure baseline if errors occur.

Phase 4: Testing, Debugging, & Permissions

Done with the main script, now I should probably test it. rm is for deleting a file within the Linux terminal! Remember! 

lol, accidentally used different syntax for Python lol. 

Tried running the script, and it seems like I'm getting a permission issue. It says something along the lines of access to a certain file being denied. I learned we use the sudo command in Linux to initiate something as the administrator. Cool.

A key thing to know is that when you dump a dictionary into a JSON file using 

json.dump(), the key values are automatically converted into strings, so watch out for that. 

So it works! Let's modify one of the hash values within the baseline file, rerun the script, and see what happens. I'm excited, I won't lie! 

I opened the file through VS Code but can't edit it since I don't have the permissions. The baseline file itself was created when I ran the program using 

sudo, which made the owner the superuser, "root". Now VS Code is running as me, the normal user qasim, so that's an issue. I need to change the owner of the baseline file back to me lolz. 


The  chown command will be used to change the owner of a file, and sudo will be used to authorize the change. In Linux, a file has 2 owners: an individual owner and a group owner (like a collection of users). So when resetting the owner, I had to do 


qasim:qasim; the first part set the individual user, the second the collection of users. 

Phase 5: Automating with cron

Essentially, there is a program called 

cron that is constantly running within our Linux system; these types of programs are called daemons.  The main job of this program is to wake up every minute or so and scan for any scheduled tasks. If it's time to run any that exist, it runs them. 


The list of tasks that the 

cron program checks is the crontab, which stands for "cron table". Each user on the system has their own 

crontab where they can list the specific jobs/tasks they want to be run and scheduled. 


crontab -e will open my user-specific crontab, allowing me to edit and add any tasks/jobs. The most beginner-friendly text editor is 

nano. 

I learned that a cron job has two parts: the schedule and the command. For my testing, I'll set it up for every minute. To do that, I'll use 

*/1 * * * *. 


My venv has a specific version of Python. My system could have many different versions installed, so I need to specify which Python my project's venv uses to avoid compatibility issues. After that, I need to specify the path of my Python script. 

I had an issue where my venv was created wrong and was pointing to the system-wide Python binaries. Luckily, it wasn't an issue since I didn't use any special Python version or libraries, but I need to keep this in mind. I deleted the 

venv with rm -rf venv and recreated it. The new one now points to the 

venv specific Python binaries. 

Nothing was being printed to the terminal. I learned I need to redirect the output. >> will create a new file if one does not exist and append any output from my script into that file, so it keeps a running log. So I created a log file to store the output. 

Errors weren't being sent to the log, so troubleshooting would be hell. 

2>&1 states that it will send anything from the error stream to the same place where the normal standard output stream is sent. 

On WSL, 

cron is disabled automatically once you close it, hence I have to manually run it with sudo service cron start. 

After all that, I was getting the wrong output in the log. Annoying. Apparently, it was because cron by default runs in the home directory and wasn't given any instruction on where baseline.json was. In my command, I had to add cd and then the location of my project folder. Once I fixed that, everything worked. Good. We are done. 

Phase 6: Finalizing on GitHub

Okay, so now to just push everything onto GitHub. I need to ignore the 

venv files since there are thousands of files specific to my machine and I clearly don't want that pushed