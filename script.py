#!/usr/bin/env python3

import subprocess
import sys
import os

# function to check docker and docker-compose installation
def installation_check():
    try:
        docker_version_output = subprocess.check_output(["docker", "--version"])
        docker_compose_version_output = subprocess.check_output(["docker-compose", "--version"])
        print('Docker: ', docker_version_output)
        print('Docker-Compose: ', docker_compose_version_output)
    except FileNotFoundError:
        print('Docker / Docker-Compose not found. Please wait while it is being installed.')
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "docker-compose"])
    
# function to create the wordpress website
def create_wordpress_site(site_name):
    # docker-compose file
    with open("docker-compose.yml", "w") as f:
        f.write('''\
version: '3'
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - php
  php:
    image: php:latest
    volumes:
      - ./wordpress:/var/www/html
  mysql:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: example
  wordpress:
    image: wordpress:latest
    volumes:
      - ./wordpress:/var/www/html
    environment:
      WORDPRESS_DB_HOST: mysql
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: example
    depends_on:
      - mysql
''')
    # nginx configuration file
    with open("nginx.conf", "w") as f:  
        f.write('''\
server {
    listen 80;
    server_name _;
    root /var/www/html;
    index index.php index.html index.htm;
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
    location ~ \.php$ {
        fastcgi_pass php:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
''')

    subprocess.run(["docker-compose", "up", "-d"])
    # site_name pointing to localhost
    with open("/etc/hosts", "a") as f:
        f.write(f"127.0.0.1 {site_name}\n")

    print(f"LEMP stack with WordPress site '{site_name}' created. Open http://{site_name} in your browser.")

# function to manage the state of website
def manage_site(site_name, action):
    if action not in ["start", "stop"]:
        print("Invalid action. Use 'start' or 'stop'.")
        sys.exit(1)

    subprocess.run(["docker-compose", "-f", "docker-compose.yml", action])

    print(f"Action for '{site_name}' has been taken.")

# function to delete the website
def delete_site(site_name):
    subprocess.run(["docker-compose", "-f", "docker-compose.yml", "down"])

    with open("/etc/hosts", "r") as f:
        lines = f.readlines()
    with open("/etc/hosts", "w") as f:
        for line in lines:
            if not line.startswith(f"127.0.0.1 {site_name}"):
                f.write(line)

    print(f"Site '{site_name}' has been deleted.")

# main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py {install | create | manage | delete}")
        sys.exit(1)

    command = sys.argv[1]

    if command == "install":
        installation_check()
    elif command == "create":
        if len(sys.argv) != 3:
            print("Usage: python3 script.py create <site_name>")
            sys.exit(1)
        create_wordpress_site(sys.argv[2])
    elif command == "manage":
        if len(sys.argv) != 4:
            print("Usage: python3 script.py manage <site_name> <start | stop>")
            sys.exit(1)
        manage_site(sys.argv[2], sys.argv[3])
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: python3 script.py delete <site_name>")
            sys.exit(1)
        delete_site(sys.argv[2])
    else:
        print("Usage: python3 script.py {install | create | manage | delete}")
        sys.exit(1)
