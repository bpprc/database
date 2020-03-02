# BPPRC 2019

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

   git clone https://github.com/Amrithasuresh/BPPRC.git
   cd bpprc
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

Then copy the following URL in your browser.

http://127.0.0.1:8000/
