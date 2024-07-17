from canvas_scraper import test_login
from canvas_scraper import combine
from canvas_scraper import add, retrieve_login, delete

from getpass import getpass
password = getpass("Enter your password: ")

#Test Case 1 Empty Username Non-empty Password
if(test_login("", "1234")):
    print("Failed")
else:
    print("True")

#Test Case 2 Non Empty Username Empty Password
if(test_login("adhaw2@illinois.edu", "")):
    print("Failed")
else:
    print("True")

#Test Case 3 Empty Username Empty Password
if(test_login("", "")):
    print("Failed")
else:
    print("True")

#Test Case 4 Incorrect Password
if(test_login("adhaw2@illinois.edu", "hi")):
    print("Failed")
else:
    print("True")


#Test Case 5 Non-UIUC Domain
if(test_login("afd5749@psu.edu", "hi")):
    print("Failed")
else:
    print("True")

#Test Case 6 Correct Login
if(not (len(combine("arama9@illinois.edu", password)) > 0)):
    print("Failed")
else:
    print("True")


#Test Case 7 SQL Database
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database = "mydatabase"
)
add("nuhuh","arama9@illinois.edu", password )
if(len(retrieve_login("nuhuh")) == 0):
    print("Failed")
else:
    print("True")
    delete("nuhuh")







