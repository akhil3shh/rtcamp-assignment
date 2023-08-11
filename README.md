# LEMP Stack Wordpress Website Deploy on Docker

### Pre-requisites:    
Make sure python3 is installed on your machine as this script is written in python.

### To install this script:  
1.) Download the script.py to your local machine (preferably Linux system)   
2.) Open a terminal and navigate to the directory containing the script.   
3.) Make the script executable using the command `sudo chmod +x script.py`   

### Commands:
1.) Docker and Docker-compose installation: `python3 script.py install`  
2.) Wordpress website creation: `python3 script.py create <site_name>`  
3.) Manage the website: `python3 script.py manage <site_name> start` or `python3 script.py manage <site_name> stop`  
4.) Delete the website: `python3 script.py delete <site_name>`

### Note:
Be sure to replace 'site_name' with your preferred website name.   
Use sudo privileges as and when needed.



