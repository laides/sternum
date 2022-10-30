# sternum
parking registration exercise

This is the readme file for the parking registration system.

It creates a database with each car that tries to enter the parking, including its license number, the parking status (allowed or denied), the timestamp of the parking entry and the car type (fuel operated/hybrid/public transportation)
The car number is detected from image file using an api, that detects text from image.
The system supports jpg and pdf files.  

It contains the python file sternum.py and the database class.

Before running sternum.py please verify that you have python version 2.7 installed .
In addition, please install python packages sed by the application :
- requests
- json
- time
- os
- sqlite3
For the package installation, please use "pip install <package name>" from cmd window.

In order to run the application , please run command "python sternum.py"
from sternum folder.
Plase contact me for any questions or issues.
