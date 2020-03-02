.. BPPR documentation master file, created by
   sphinx-quickstart on Wed Dec 18 10:35:08 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BPPRC's documentation!
================================

.. image:: /image/image.png

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index
   BPPRC
   database
   bestmatchfinder
   clustalanalysis
   cry_package
   namingalgorithm
   MigrateToPostgreSQL.rst

Here is some text explaining some very complicated stuff.::

  print('hello')
  >> hello

|
Installation Instructions
^^^^^

If you have git and pip installed, use this:

pip install virtualenv
virtualenv env
source env/bin/activate

git clone https://github.com/Amrithasuresh/BPPRC.git
cd bpprc
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

|
Admin Functionalities
^^^^^

|
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
