# Task
Please implement deployment of 3 tier application, which would run on Ubuntu server 18.04 LTS, would use Nginx, Postgres and Python code in consitent and repeatable way. You would need to automate deployment of:
1. Setup use of 10.0.0.2/18 static IP address, Netmask 255.255.0.0, gateway 10.0.0.1/18
2. Install Nginx, configure it to serve static pages and dynamic pages via FCGI (python application)
3. Install PostgreSQL DBMS and create DB, user for DB, set users password.
4. Install simple Python application which would serve "Hello World!" via FCGI.
5. Make sure all your changes are persistent after reboot.

# Evaluation points
* correctness of implementation in scripts
* Bash scripts best practices
* Python code best practices
* use of git, appropriate commit messages
* documentation: README and inline code comments
# Bonus points
* Use Ansible for server setup.

# Notes on manual task implementation
* configure networking:
The IP configuration is stored in `/etc/netplan/50-cloud-init.yaml`.
```
$ sudo netplan --debug try
$ sudo netplan --debug apply
```
* install nginx:
```
$ sudo apt-get update
$ sudo apt-get install -y nginx
$ sudo systemctl enable nginx.service
$ sudo systemctl start nginx.service
$ sudo nano /etc/nginx/sites-available/default
$ sudo nano /var/www/html/hello.py
$ sudo apt install -y python3-pip
# pip3 install flup
$ sudo chmod +x /var/www/html/hello.py
$ sudo nano /etc/supervisor/conf.d/hello-fcgi.conf
$ sudo systemctl reload nginx.service
```
* install supervisor to manage FastCGI socket:
```
$ sudo apt install -y supervisor
$ sudo systemctl enable supervisor.service
$ sudo systemctl start supervisor.service
```
* install PostgreSQL:
```
$ sudo apt install -y postgresql
```
* create DB, user(s) and setup access:
```
$ sudo -u postgres psql

postgres=# CREATE DATABASE noctaskdb;
postgres=# CREATE USER noc WITH ENCRYPTED PASSWORD 'kQTVFqpFuqo';
postgres=# GRANT ALL PRIVILEGES ON DATABASE noctaskdb TO noc;

$ psql -h 127.0.0.1 -p 5432 -U noc -W noctaskdb
```