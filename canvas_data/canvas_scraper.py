from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import json
from getpass import getpass
from datetime import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
from pl_scraper import pl_scrape
app = Flask(__name__)
CORS(app)
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database = "mydatabase"
)
# from unidecode import unidecode
from time import sleep
from traceback import print_exc
# username2 = input("Enter your username (e.g., adhaw2@illinois.edu): ")
# password = getpass("Enter your password: ")
def test_login(username2, password):
    if(len(username2) == 0):
       return False
    if(len(password) == 0):
        return False
    if(len(username2) < 14 or username2[-13:] != "@illinois.edu"):
        return False
    firefox_service = Service('./geckodriver.exe')
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options,service=firefox_service)
    #driver = webdriver.Firefox(service=firefox_service)
    driver.get("https://canvas.illinois.edu/courses")
    if "login.microsoftonline.com" in driver.current_url:
        sleep(2)
        print("\nLogging in to Canvas System\n")
        username = driver.find_element(By.CSS_SELECTOR, "input[name='loginfmt']")
        username.send_keys(username2)
        driver.find_element(By.CSS_SELECTOR, "#idSIButton9").click()
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, "input[name='passwd']").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "#idSIButton9").click()
    sleep(2)
    if "login.microsoftonline.com" in driver.current_url:
        return False
    else:
        print("LOGIN SUCCESS!!!")
        return True

def combine(username2, password):
    try:
        firefox_service = Service('./geckodriver.exe')
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options,service=firefox_service)
        #driver = webdriver.Firefox(service=firefox_service)
        driver.get("https://canvas.illinois.edu/courses")

        if "login.microsoftonline.com" in driver.current_url:
            sleep(2)
            print("\nLogging in to Canvas System\n")
            username = driver.find_element(By.CSS_SELECTOR, "input[name='loginfmt']")
            username.send_keys(username2)
            driver.find_element(By.CSS_SELECTOR, "#idSIButton9").click()
            sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[name='passwd']").send_keys(password)
            driver.find_element(By.CSS_SELECTOR, "#idSIButton9").click()
        sleep(2)
        if "login.microsoftonline.com" in driver.current_url:
            raise("\nFailed: Wrong email or password!\n")

        courses =  driver.find_elements(By.CSS_SELECTOR, "#my_courses_table a")
        names = [course.get_attribute("title") for course in courses]
        print("\nGathering Course Names\n")
        links = [course.get_attribute("href")+"/assignments" for course in courses]
        print("\nGathering Course Links\n")
        cassignments = {}
        for i in range(len(links)):
            print(f'\nGathering {names[i]} Assignments\n')
            driver.get(links[i])
            sleep(2)
            assignment_elements = driver.find_elements(By.CSS_SELECTOR, "#assignment_group_upcoming .ig-title")
            date_elements = driver.find_elements(By.CSS_SELECTOR, "#assignment_group_upcoming .ig-details [class = 'ig-details__item assignment-date-due'] [class = 'screenreader-only']")
            assignment_names = [assignment.text for assignment in assignment_elements]
            dates = [date.text.split() for date in date_elements]
            dates_removed = []
            for z in dates:
                del z[2]
                if(len(z[2]) == 3 or len(z[2]) == 4):
                    if(len(z[2]) == 3):
                        z[2] = z[2][:1] + ":00" + z[2][1:]
                    else:
                        z[2] = z[2][:2] + ":00" + z[2][2:]
                z += ["2023"]
                dates_removed += [f'Due {datetime.strptime("-".join(z), "%b-%d-%I:%M%p-%Y").strftime(r"%H:%M, %m/%d")}']    
            assignment_dict = []
            for a,b in zip(assignment_names, dates_removed):
                assignment_dict += [[a,b]]
            cassignments[names[i]] = assignment_dict
        # with open("correct.json") as f:
        #     correct = json.load(f)
        print("LOGGING INTO PRAIRIELEARN")
        driver.get("https://us.prairielearn.com/pl/auth/institution/3/saml/login")
        sleep(2)
        courses = driver.find_elements(By.CSS_SELECTOR, "td > [href]")
        course_links = []
        course_names = []
        for course in courses:
            course_links.append(course.get_attribute("href"))
            course_names.append(course.text)
        course_dict = {}
        for name, link in zip(course_names, course_links):
            lod = []
            driver.get(link)
            html_soup = BeautifulSoup(driver.page_source, parser = "lxml", features = "lxml")
            assignments = html_soup.find_all("td")
            i = 0
            while i < len(assignments):
                i += 1
                lod.append([assignments[i].text.strip(), assignments[i + 1].text.strip(), assignments[i + 2].text.strip()])
                i += 3
            course_dict[name] = lod
            print(f"{name} loaded")
            sleep(4)
        unfinished = {}
        for course in course_dict:
            course_assignments = []
            for assignment in course_dict[course]:
                if "until" in assignment[1]:
                    name = assignment[0]
                    available_credit, date_str = assignment[1].split(r"% until ")
                    current_credit = assignment[2]
                    if available_credit != "None":
                        if current_credit == "Not started" or current_credit == "New instance":
                            date = datetime.strptime(date_str, r"%H:%M, %a, %b %d")
                            course_assignments.append([name, date])
                        elif int(available_credit) > int(current_credit[:-1]):
                            date = datetime.strptime(date_str, r"%H:%M, %a, %b %d")
                            course_assignments.append([name, date])
            unfinished[course] = course_assignments

        for course in unfinished:
            unfinished[course] = sorted(unfinished[course], key=lambda x: x[1])
            for data in unfinished[course]:
                data[1] = f'Due {data[1].strftime(r"%H:%M, %m/%d")}'
        cassignments.update(unfinished)
        #print(cassignments)
        driver.quit()
        assign = []
        for x in cassignments.keys():
            assign += cassignments[x]
        return(assign)
    except:
        print_exc()
        driver.quit()

# test_login(username2,password)
# canvas(username2, password)
# pl_scrape(username2, password)

def add(username, email, password):
    print(username)
    mycursor = mydb.cursor()
    sql = "INSERT INTO logins (username, email, password) VALUES (%s,%s,%s)"
    val = (username, email, password)
    mycursor.execute(sql,val)
    mydb.commit()
def retrieve_login(username):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM logins WHERE username = %s"
    mycursor.execute(sql, (username,))
    myresult = mycursor.fetchall()
    return myresult
def delete(username):
    mycursor = mydb.cursor()
    sql = "DELETE FROM logins WHERE username = %s"
    mycursor.execute(sql, (username,))
    mydb.commit()
#add("testing1", "testing2", "testing3")
#print(retrieve_login("testing3"))
#delete("testing3")

@app.route('/register', methods=['POST'])
def register():
    print("hi")
    data = request.get_json()
    email = data['email']
    password = data['password']
    username = data["username"]
    print(email)
    # Call the `test_login` function to validate the credentials
    valid = test_login(email, password)
    if(valid):
        add(username, email, password)
    return jsonify({"valid": valid})

@app.route('/assignments', methods=['POST'])
def assignments():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(email)
    # Call the `test_login` function to validate the credentials
    assignments = combine(email, password)

    return jsonify(assignments)

@app.route('/retrieve_mylogin', methods=['POST'])
def retrieve_mylogin():
    print("hello dearest")
    data = request.get_json()
    username = data['username']
    login_info = retrieve_login(username)

    if login_info:
        email = login_info[0][1] 
        password = login_info[0][2] 

        response_data = {'email': email, 'password': password}

        return jsonify(response_data)
    else:
        return jsonify({'error': 'Login details not found for the provided username'}), 404

if __name__ == '__main__':
    app.run(debug=True)