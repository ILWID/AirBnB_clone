# AirBnB_clone
---------------
### This project is a clone of the AirBnb web application

## In this project
### Command interpreter
----------------------

The command interpreter is a command line interpreter used to manage the objects of this project
- Create a new object
- Retrieve an object from a file or database
- Do operations on objects (count, compute stats, etc…)
- Update attributes of an object
- Destroy an object

The interpreter works in interactive mode
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$

But also in non-interactive mode
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
EOF  help  quit
(hbnb) 
$

