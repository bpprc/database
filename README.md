# BPPRC 2021

[![Django CI](https://github.com/Amrithasuresh/database_test/actions/workflows/testing.yml/badge.svg?branch=database_test)](https://github.com/Amrithasuresh/database_test/actions/workflows/testing.yml)

BPPRC database repository for GitHub actions

The pesticidal protein database is part of the Bacterial Pesticidal Protein Resource Center (BPPRC), which is under development. This database is intended to replace and extend the current [Bacillus thuringiensis nomenclature site](http://www.btnomenclature.info).

The database currently contains proteins listed in the Bt nomenclature site but with new mnemonics to reflect assignment of proteins to different homology groups. New bacteria-derived proteins with pesticidal properties are to be added.

In addition to the database, the BPPRC will contain links to additional information about these proteins, as well as applications to allow for analysis and comparison between proteins.

The development team is composed of:

Suresh Pannerselvam<sup>1</sup> ,  Neil Crickmore <sup>2</sup> ,  Colin Berry <sup>3</sup>,  Thomas Connor<sup>3</sup>, Ruchir Mishra<sup>1</sup>  and  Bryony C. Bonning<sup>1</sup>
&nbsp;
<sup>1</sup> Department of Entomology and Nematology, University of Florida, USA
<sup>2</sup> School of Life Sciences, University of Sussex, UK
<sup>3</sup> School of Biosciences, Cardiff University, UK


This is the source code of BBPRC 2019 website developed in Python/Django. To run the website locally, you need to install Django and a list of other Python packages which are listed in the requirements.txt file.


Get the development version from `Github`
--------------------------------------------

If you have `git` and `pip` installed, use this:

   pip install virtualenv
   virtualenv env
   source env/bin/activate

   git clone https://github.com/Amrithasuresh/BPPRC.git <br />
   cd bpprc <br />
   pip install -r requirements.txt <br />
   python manage.py migrate <br />
   python manage.py runserver <br />

Then copy the following URL in your browser.

http://127.0.0.1:8000/


Production installation instruction without Docker
--------------------------------------------

1.	[Celery](https://docs.celeryproject.org/en/stable/index.html) is an open-source task queue or job queue which is based on the distributed message passing. It supports scheduling too. Here we use [redis](https://redis.io/) the message-broker for celery.

*	How to install [Celery?](https://pypi.org/project/celery/)  <br />
   `pip install celery`  <br />

*  How to run Celery from the base project directory? Here, it will be ~/database/  Django base directory. <br />
   `celery worker -A BPPRC –loglevel=info` <br />

* 	How to install the Redis server? <br />
   `wget http://download.redis.io/redis-stable.tar.gz` <br />
   `tar xvzf redis-stable.tar.gz` <br />
   `cd redis-stable` <br />
   `make` <br />

* 	How to start Redis server?  <br />
   `sudo service redis start`  <br />

*	How to check the status of Redis server?  <br />
   `sudo service redis status`  <br />

2.	[PostgreSQL](https://www.postgresql.org/) is a powerful, open-source object-relational database system.

* How to install PostgreSQL? <br />
  `sudo apt-get install python-dev` <br />
  `sudo apt-get install postgresql-server-dev-9.1` <br />
  `sudo apt-get install python-psycopg2 - Or sudo pip install psycopg2` <br />
  `sudo apt-get install postgresql pgadmin3` <br />

* Change the default password <br />
  `sudo su` <br />
  `su postgres -c psql postgres` <br />
  `ALTER USER postgres WITH PASSWORD 'YourPassWordHere';` <br />
  `\q` <br />

 *	Create the database <br />
   `sudo su` <br />
   `su postgres -c psql postgres` <br />
   `CREATE DATABASE dbname;` <br />
   `CREATE USER djangouser WITH ENCRYPTED PASSWORD 'myPasswordHere';` <br />
   `GRANT ALL PRIVILEGES ON DATABASE dbname TO djangouser;` <br />


 *	Settings.py file <br />
  ` DATABASES = {` <br />
  `  'default': {` <br />
   ` 'ENGINE': 'django.db.backends.postgresql_psycopg2',` <br />
   ` 'NAME': 'dbname',` <br />
    `'USER': 'postgres',` <br />
    `'PASSWORD': 'postgres',` <br />
   ` 'HOST': '',` <br />
   ` 'PORT': '',` <br />
   ` }` <br />
  ` }` <br />


3.	Create virtual environment  <br />
   `pip install virtualenv` <br />
   `virtualenv venv` <br />
   `source venv/bin/activate` <br />

   * Dependencies (requirements.txt file is inside the Django base directory) <br />
   `pip install -r requirements.txt` <br />

4. Nginx is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache. Nginx can be deployed to server dynamic HTTP content on the network using WSGI application servers (an example) and it can serve as a software load balancer. Nginx will face the outside world. It will serve media files (images, CSS, etc) directly from the file system. However, it can't talk directly to Django applications; it needs something (uWSGI) that will run the application, feed it requests from the web, and return responses. [Source](https://serverfault.com/a/887845)

The outside world (HTTP client) <-> Nginx <-> The socket <-> uWSGI <-> Python app <br />


   * Install Nginx <br />
   `sudo apt-get install nginx ` <br />

   * Nginx configuration file Location <br />
   `/etc/nginx/conf.d/virtual.conf` <br />

   * Nginx virtual.conf file contents <br />

      `server {` <br />
        `  listen       80;` <br />
         ` server_name  {your domain_name};` <br />
         `  error_log /srv/www/database/logs/error.log;` <br />
         `  access_log /srv/www/database/logs/access.log;` <br />
          ` charset utf-8;` <br />

       `location /static/ {` <br />
         ` alias /srv/www/database/static/;` <br />
       `}` <br />

       `location /media/ {` <br />
         `  alias /srv/www/database/media/;` <br />
       `}` <br />

       `location / {` <br />
      	 ` add_header 'Cache-Control' 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';` <br />
    	    ` expires off;` <br />
          ` #uwsgi_pass unix:/opt/uwsgi/sock/database.sock;` <br />
          ` proxy_connect_timeout 300s;` <br />
          ` proxy_read_timeout 300s;` <br />
          ` proxy_pass http://127.0.0.1:8000;` <br />
           `include uwsgi_params;` <br />
       `}` <br />

       ` #root /srv/www/database_test/database/templates/extra;` <br />
       ` #index site-down.html; ` <br />

      ` }` <br />


  * Nginx log file location <br />
    `/var/log/nginx/error.log` <br />


 5. uWSGI is a popular web server that implements the WSGI  (pronounced wiz-gee) standard. WSGI  (Web Server Gateway Interface) is a software specification, uWSGI is a web server. It’s pretty common to pair Django and uWSGI since they both talk WSGI. The uWSGI server is a full featured HTTP server that is quite capable of running production web apps. However, it’s not as performant as nginx at serving static content, so it’s pretty common to see nginx sitting in front a uWSGI server. Here’s where some poor naming choices make things even more confusing. So we know WSGI is a software spec, uWSGI is a server, so what the hell is uwsgi? When it’s spelled using all lowercase letters, it refers to a binary protocol for connecting the uWSGI server to other applications. [Source](https://www.ultravioletsoftware.com/single-post/2017/03/23/An-introduction-into-the-WSGI-ecosystem) <br />


  *  Installation <br />
     `sudo apt-get install build-essential python` <br />
     `sudo apt-get install python-dev ` <br />
     `pip install uwsgi (in the virtual environment)` <br />

  *  uwsgi emperor configuration location and contents <br />
     `/etc/uwsgi/emperor.ini <br />

     `[uwsgi]` <br />
     `emperor = /etc/uwsgi/vassals ` <br />
     `uid = uwsgi ` <br />
     `gid = uwsgi ` <br />
     `logto = /etc/uwsgi/log/uwsgilog` <br />


  *	uwsgi vassals configuration location and contents <br />
      `/etc/uwsgi/vassals/demo.ini` <br />


      `[uwsgi] ` <br />
      `http = :8000 ` <br />
      `workers = 1  ` <br />
      `processes = 1` <br />
      `socket = /opt/uwsgi/sock/database.sock`  <br />
      `chdir = /srv/www/database/` <br />
      `pythonpath = /srv/www/database/database/` <br />
      `home = /opt/python-virtual-env/` <br />
      `logto = /srv/www/database/logs/uwsgi.log` <br />
      `module = BPPRC.wsgi` <br />
      `uid = uwsgi `  <br />
      `chmod-socket = 666` <br />
      `chown-socket = uwsgi` <br />
      `harakiri = 300 ` <br />

  *	uwsgi log file location <br />
   `/etc/uwsgi/log/uwsgilog` <br />



  6. Install bioinformatics software’s <br />

  * How to install Needle?. It should be able to run in the terminal. Provide a full path in both production as well as local. Otherwise, in production it will be     headache. This applies to all the binary external softwares.  <br />
   ` Download EMBOSS-6.x.x.tar.gz` <br />
    `Gunzip EMBOSS-6.x.x.tar.gz` <br />
   `tar xvf EMBOSS-6.x.x.tar.gz` <br />

     Compile <br />
     `cd EMBOSS-6.x.x` <br />
     `./configure` <br />
     `make` <br />

  *	Clustal Omega. [Download and Install](http://clustal.org/omega/). <br />
      [Installation Instructions](http://clustal.org/omega/INSTALL) <br />



  7. How do I manage the production and local settings? <br />

    We have separate .env files both in the production and local settings <br />

  *	Production .env file location and contents <br />
      `/srv/www/database/.env` <br />

     `SECRET_KEY='………'` <br />
     `EMAIL_BACKEND='django_ses.SESBackend'` <br />

     `#Amazon key` <br />
    `AWS_ACCESS_KEY_ID='……..'` <br />
    `AWS_SECRET_ACCESS_KEY='…’` <br />
    `AWS_SES_REGION_NAME='us-east-1'` <br />
    `AWS_SES_REGION_ENDPOINT='email-smtp.us-east-1.amazonaws.com'` <br />

    `CRISPY_TEMPLATE_PACK='bootstrap4'` <br />
    `CSRF_COOKIE_SECURE=True` <br />

    `# google recaptcha` <br />
     `RECAPTCHA_PUBLIC_KEY="6Lc-HfMUAAAAALHi0-vkno4ntkJvLW3rAF-d5UXT"` <br />

    `# used betweeen server and reCAPTCHA` <br />
    `RECAPTCHA_PRIVATE_KEY="6Lc-HfMUAAAAAI2H-DuGJKPETsB_ep3EQNKkdesC"` <br />


    `NEEDLE_PATH='/opt/EMBOSS-6.6.0/emboss/'` <br />
    `BLAST_PATH='/usr/local/bin/'` <br />
    `CLUSTAL_PATH='/usr/local/bin/'` <br />
    `DATABASE_TYPE='production'` <br />


  *	Local .env file location and contents <br />
     ` ~/database_test/` <br />

     ` SECRET_KEY=’’` <br />
     ` DEVELOPMENT=True` <br />

      `AWS_ACCESS_KEY_ID=''` <br />
      `AWS_SECRET_ACCESS_KEY=''` <br />

      `CRISPY_TEMPLATE_PACK='bootstrap4'` <br />
      `CSRF_COOKIE_SECURE=True` <br />

     `# used betweeen server and reCAPTCHA` <br />
       `RECAPTCHA_PRIVATE_KEY="6Lc-HfMUAAAAAI2H-DuGJKPETsB_ep3EQNKkdesC"` <br />

       `NEEDLE_PATH='/usr/local/bin/'` <br />
       `BLAST_PATH=''` <br />
       `CLUSTAL_PATH='/sw/bin/'` <br />

       ` DATABASE_TYPE='sqlite3'` <br />

 *	We add/change these lines to access the path in the settings.py file  <br />

    `SECRET_KEY = os.environ.get("SECRET_KEY")`  <br />

    `if os.environ.get('DEVELOPMENT'):`  <br />
        `DEBUG = True`  <br />
    `else:`  <br />
        `DEBUG = False`  <br />


    `if os.environ.get('DATABASE_TYPE') == 'sqlite3':`  <br />
        `DATABASES = {`  <br />
            `'default': {`  <br />
            `'ENGINE': 'django.db.backends.sqlite3',`  <br />
            `'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),`  <br />
         `}`  <br />
     `}`  <br />
    `else:`  <br />
         `DATABASES = {`  <br />
          ` 'default': {`  <br />
            `'ENGINE': 'django.db.backends.postgresql_psycopg2',`  <br />
            `'NAME': 'YOURDATABASENAME',`  <br />
            `'USER': 'YOURNAME',`  <br />
            `'PASSWORD': 'YOURPASSWORD',`  <br />
            `'HOST': 'localhost',` <br />
            `'PORT': '5432',` <br />
        ` }`  <br />
      `}`  <br />

      `NEEDLE_PATH = os.environ.get('NEEDLE_PATH', '')`  <br />
      `BLAST_PATH = os.environ.get('BLAST_PATH', '')`  <br />
      `CLUSTAL_PATH = os.environ.get('CLUSTAL_PATH', '')`  <br />
      `CRISPY_TEMPLATE_PACK = os.environ.get('CRISPY_TEMPLATE_PACK')`  <br />

     `# AWS`  <br />
      `EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')`  <br />
      `AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')`  <br />
      `AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')`  <br />
      `AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME')`  <br />
      `AWS_SES_REGION_ENDPOINT = os.environ.get('AWS_SES_REGION_ENDPOINT')`  <br />

      `# google reCAPTCHA`  <br />
      `RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')`  <br />
      `RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')`  <br />



 8. How do you manage the local repository and the server repository? <br />

   I have setup a private repository for [GitHub](https://github.com/). Push the changes from Atom editor to the GitHub. And, pull the changes from the hosted        server. <br />
    `git pull origin database `


 9. Tmux usage – Terminal multiplexer. It lets you switch easily between several programs in one terminal, detach them (they keep running in the background) and      reattach them to a different terminal. <br />

     `sudo apt-get install tmux` <br />

   ### [Tutorial](https://help.sourcelair.com/terminal/working-with-multiple-tabs/) <br />

    To start a tmux session <br />
    tmux in terminal <br />

    Opening a multiple tab <br />
    ` Ctrl + B and then C` <br />

    To move among these tables hit the following keys <br />
    `Ctrl + B and then n to go the next tab on the right` <br />
    ` Ctrl + B and then p to go to the previous tab on the left` <br />
    ` Ctrl + B and then {number} to go the tab with number equal to 0, 1` <br />

    To detach the tmux session <br />
    `Ctrl + B and then d` <br />

    To close a tab <br />
   `Ctrl + B and then x and then hit y and Enter to confirm closing of this tab` <br />


 10. Remove temporary files through cron jobs <br />
   ` cat /opt/script/tmp-cleanup.sh` <br />
   ` #!/bin/bash` <br />
    `Find /tmp -type f -mmin +14440 -exec rm -f {} \;` <br />
