#!/bin/bash
python manage.py delete_all_models
python manage.py upload_association_database
python manage.py upload_hidden_sequence_database
#python manage.py upload_private_database needs csv input file
python manage.py upload_public_database
python manage.py upload_structure_database
python manage.py upload_description_database
python manage.py upload_newname_database
python manage.py upload_oldname_database
python manage.py upload_threedomain_data

# https://pythoneatstail.com/en/overview-all-articles/backup-and-restore-django-site/
python3 manage.py dbbackup
python3 manage.py mediabackup

# if you remove a feild and want to load data use --ignorenonexistent
python manage.py loaddata /Users/suresh/Desktop/May_21.json -ignorenonexistent


# Automatically change the .env file in git
https://stackoverflow.com/questions/62841470/how-to-have-branch-specific-variables-in-git-and-python

# how to add admin user name in the status page
