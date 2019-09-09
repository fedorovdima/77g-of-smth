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

# Implementation
## Automated deployment
<details>
  <summary>Automated task implementation is performed by means of using Ansible</summary>
as shown below:
```$ ansible-playbook -v playbook.yml
Using /home/ubuntu/.ansible.cfg as config file
PLAY [target_group] ********************************************************************************
TASK [make sure APT DB is up-to-date] **************************************************************
...
changed: [1.2.3.4] => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3"}, "cache_update_time": 1568045341, "cache_updated": true, "changed": true}
TASK [install nginx] *******************************************************************************
ok: [1.2.3.4] => {"changed": false, "enabled": true, "name": "nginx", "state": "started", ...
TASK [upload nginx config] *************************************************************************
changed: [1.2.3.4] => {"changed": true, "checksum": "23fc2dfb5f9bd61d1782a5e528d8bf162dd5ea36", "dest": "/etc/nginx/sites-available/default", "gid": 0, "group": "root", "md5sum": "c97266038ac920f43212e5284a0b5152", "mode": "0644", "owner": "root", "size": 481, "src": "/home/ubuntu/.ansible/tmp/ansible-tmp-1568045356.14-82845152666069/source", "state": "file", "uid": 0}
TASK [upload hello-world app code] *****************************************************************
changed: [1.2.3.4] => {"changed": true, "checksum": "8470b848120d476f56a39a22d2eae7839dd8233c", "dest": "/var/www/html/hello.py", "gid": 0, "group": "root", "md5sum": "4353284cba16776d79af7e3a69867fe0", "mode": "0755", "owner": "root", "size": 421, "src": "/home/ubuntu/.ansible/tmp/ansible-tmp-1568045357.42-54131129288573/source", "state": "file", "uid": 0}
TASK [install python3-pip to install required Python module(s)] ************************************
changed: [1.2.3.4] => {"cache_update_time": 1568045341, "cache_updated": false, "changed": true, "stderr": "", "stderr_lines": [], "stdout": "Reading package lists...
TASK [install Python flup module for hello-world app] **********************************************
changed: [1.2.3.4] => {"changed": true, "cmd": ["pip3", "install", "flup"], "delta": "0:00:01.504129", "end": "2019-09-09 16:09:56.878618", "rc": 0, "start": "2019-09-09 16:09:55.374489", "stderr": "", "stderr_lines": [], "stdout": "Collecting flup\n  Downloading https://files.pythonhosted.org/packages/88/e5/17bcf4431e811ffaec213feea7609a6f003084006d2e210f53cee09095d9/flup-1.0.3-py3-none-any.whl (74kB)\nInstalling collected packages: flup\nSuccessfully installed flup-1.0.3", "stdout_lines": ["Collecting flup", "  Downloading https://files.pythonhosted.org/packages/88/e5/17bcf4431e811ffaec213feea7609a6f003084006d2e210f53cee09095d9/flup-1.0.3-py3-none-any.whl (74kB)", "Installing collected packages: flup", "Successfully installed flup-1.0.3"]}
TASK [install supervisor to manage FastCGI socket between nginx and hello-world app] ***************
changed: [1.2.3.4] => {"cache_update_time": 1568045341, "cache_updated": false, "changed": true, "stderr": "", "stderr_lines": [], "stdout": "Reading package lists...
TASK [enable and start supervisor] *****************************************************************
ok: [1.2.3.4] => {"changed": false, "enabled": true, "name": "supervisor", "state": "started", ...
TASK [upload supervisor config file for managing FastCGI socket] ***********************************
changed: [1.2.3.4] => {"changed": true, "checksum": "6c692a9be45e99d8468e7061022deca54b1dfad2", "dest": "/etc/supervisor/conf.d/hello-fcgi.conf", "gid": 0, "group": "root", "md5sum": "a1cd419c052da3561c905bae6e543d68", "mode": "0644", "owner": "root", "size": 134, "src": "/home/ubuntu/.ansible/tmp/ansible-tmp-1568045668.61-142918330755432/source", "state": "file", "uid": 0}
TASK [reload supervisor for it to handle the new config] *******************************************
changed: [1.2.3.4] => {"changed": true, "name": "supervisor", "state": "started", ...
TASK [install postgres_* modules dependencies] *****************************************************
changed: [1.2.3.4] => {"cache_update_time": 1568045341, "cache_updated": false, "changed": true, "stderr": "", "stderr_lines": [], "stdout": "Reading package lists...
TASK [install Postgres SQL RDBMS] ******************************************************************
changed: [1.2.3.4] => {"cache_update_time": 1568045341, "cache_updated": false, "changed": true, "stderr": "", "stderr_lines": [], "stdout": "Reading package lists...
TASK [create a sample Postgres DB] *****************************************************************
changed: [1.2.3.4] => {"changed": true, "db": "noctaskdb"}
TASK [сreate a sample Postgres user] ***************************************************************
changed: [1.2.3.4] => {"changed": true, "queries": ["CREATE USER \"noc\" WITH ENCRYPTED PASSWORD %(password)s "], "user": "noc"}
TASK [GRANT ALL PRIVILEGES ON DATABASE noctaskdb TO noc] *******************************************
changed: [1.2.3.4] => {"changed": true, "queries": ["GRANT ALL ON database \"noctaskdb\" TO \"noc\";\nREVOKE GRANT OPTION FOR ALL ON database \"noctaskdb\" FROM \"noc\";"]}
PLAY RECAP *************************************************************************************************************
1.2.3.4              : ok=16   changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
</details>

## Manual task implementation steps
* configure networking:
The IP configuration is stored in `/etc/netplan/50-cloud-init.yaml`.
* apply network configuration:
```
$ sudo netplan --debug try
$ sudo netplan --debug apply
```
* install nginx and configure:
```
$ sudo apt-get update
$ sudo apt-get install -y nginx
$ sudo systemctl enable nginx.service
$ sudo systemctl start nginx.service
$ sudo nano /etc/nginx/sites-available/default
```
* deploy hello-world app and its dependencies:
```
$ sudo nano /var/www/html/hello.py
$ sudo apt install -y python3-pip
# pip3 install flup
$ sudo chmod +x /var/www/html/hello.py
```
* install supervisor to manage FastCGI socket: 
```
$ sudo apt install -y supervisor
$ sudo systemctl enable supervisor.service
$ sudo systemctl start supervisor.service
$ sudo nano /etc/supervisor/conf.d/hello-fcgi.conf
$ sudo systemctl reload supervisor.service
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
```
* test access to Postgres DB under the new user
```
$ psql -h 127.0.0.1 -p 5432 -U noc -W noctaskdb
```