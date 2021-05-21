#!/bin/bash
python manage.py clear_models
python manage.py upload_association
python manage.py upload_data_hidden_sequence_database
#python manage.py upload_data_private_database needs csv input file
python manage.py upload_data_public_database
python manage.py upload_data_structure_database
python manage.py upload_description
python manage.py upload_newname
python manage.py upload_oldname
python manage.py upload_threedomain_data
