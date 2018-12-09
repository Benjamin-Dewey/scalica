First installation:

Install required packages.
$ sudo apt-get update; sudo apt-get install mysql-server libmysqlclient-dev python-dev python-virtualenv git
(Set a mysql root password)

$ git clone https://github.com/Benjamin-Dewey/scalica.git && cd scalica

$ ./first_install.sh

Install the proper databases
$ cd db
$ ./install_db.sh
(Will ask for the mysql root password configured above).
$ cd ..

Sync the database
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py makemigrations micro
$ python manage.py migrate


After the first installation, from the project's directory
run the django app server and the suggestions rpc server
$ source ./env/bin/activate
$ cd suggestions
$ python server.py &
$ cd ../web/scalica
$ python manage.py runserver 0.0.0.0:8000 &

Access the site at http://[external_ip]:8000/micro

TODO: Explain how to schedule up.py and down.py
