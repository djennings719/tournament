# Welcome to the Tournament Project
##Full Stack Web Dev Project 2
###Files Included
####tournament.sql
This file contains the sql commands to create the database, tables, and views required to run the tournament application.

####tournament.py
This file contains the python methods which query the database and process the tournament rounds.

####tournament_test.py
This file contains the test procedures to ensure basic functionality.

###Launching the vagrant instance
1) Assuming your Vagrant instance is configured properly with necessary tools download the files to a folder under your Vagrant config - this is used as a dropbox in between Windows and the Linux VM 
2) Launch Git Bash and traverse your file system to get to where you have downloaded the files.
3) Type vagrant up 
4) After the start up process completes type vagrant ssh to login to the VM
5) type cd /vagrant to get to the shared vagrant folder
6) traverse the remainder of your file structure to find the files

###Configuring the database
1) Type psql
2) Type \i tournament.sql
3) Type \q to exit

###Running tournament.py file
1) Type python tournament_test.py
