Migrate from sqlite to PostgreSQL
=================================

Follow the steps to migrate :

1. Dumb database contents to json

  .. code:: bash

      python manage.py dumpdata > dump.json

2. Switch the backend database in settings.py

  .. code::

      DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
          }
      }

  To

  .. code::

      DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'proteindatabase',
      'USER': 'YOUR USERNAME',
      'PASSWORD': 'YOUR PASSWORD',
      'HOST': 'localhost',
      'PORT': '5432',
        }
      }

3. Sync and migrate the updated database

  .. code::

      python manage.py syncdb
      python manage.py migrate


4. Load the dumped json data to the new database

  .. code::

      python loaddata dump.json


Possible errors.:
===============

1. No module psycopg2

.. code:: bash

    django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 module: No module named 'psycopg2'

Solution:

.. code::

    pip install psycopg2


2. IntegrityError

.. code:: bash

    IntegrityError: duplicate key value violates unique constraint "django_content_type_app_label_key"

Solution:

  As mentioned by Daniel Roseman in the stackoverflow

  `
  The problem is simply that you're getting the content types defined twice - once when you do syncdb, and
  once from the exported data you're trying to import. Since you may well have other items in your database
  that depend on the original content type definitions, I would recommend keeping those.

  So, after running syncdb, do manage.py dbshell and in your database do TRUNCATE django_content_type;
  to remove all the newly-defined content types. Then you shouldn't get any conflicts - on that part of the process, in any case.
  `
