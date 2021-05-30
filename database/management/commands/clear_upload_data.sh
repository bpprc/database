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
