The source for this e-commerce project is code for the Apress book "Beginning Django E-Commerce" by Jim McGaw ( jim@django-ecommerce.com )

Add the project to your system's PYTHONPATH
-------------------------------------------
Make sure that the ecomstore directory where you put your project on your machine is on your system's PYTHONPATH. 


Prepare the MySQL database
--------------------------
First, create a new database login with password, the database, and give the new login permissions to manipulate the site by running the following using the 'root' MySQL user on your local machine:

mysql> CREATE USER 'login'@'localhost' IDENTIFIED BY 'password';
mysql> CREATE DATABASE ecomstore CHARACTER SET utf8;
mysql> GRANT ALL ON ecomstore.* TO 'login'@'localhost';

Once you have done this, update the database settings in your settings.py file to match the values you used above. Then, run the following from inside the root of your project:

$ python manage.py validate

If no errors are found, then run:

$ python manage.py syncdb

If you're interested in loading test data (Modern Musician product catalog featured in the book), run the following to load the sample data:

$ python manage.py loaddata catalog


Other Requirements
------------------

Installation of the Django E-Commerce store requires the following additional applications to be installed:

Django-Tagging
URL: http://code.google.com/p/django-tagging/
Instructions: After downloading the project files above, put the 'tagging' directory onto your system's PYTHONPATH

Django DB Log
URL: http://github.com/dcramer/django-db-log
Instructions: Put the 'djangodblog' directory onto your system's PYTHONPATH

Google Keyczar
URL: http://code.google.com/p/keyczar/
Instructions: Make sure to download the Python version of the keyczar library.
Put the 'src/keyczar' directory onto your system's PYTHONPATH

In order to use the CACHE_BACKEND in settings.py, you need to also install a Memcached server on your local development machine.
URL: http://www.danga.com/memcached/
Instructions: Install per the documentation for your operating system. After doing so, uncomment and (if necessary) update the 
CACHE_BACKEND value in settings.py.

Before using, be sure to generate a long random string of characters for the SECRET_KEY value in settings.py.

For questions or comments about this project contact Jim at: jim@django-ecommerce.com.
