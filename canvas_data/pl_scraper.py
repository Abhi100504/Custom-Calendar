from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from getpass import getpass
import json

from datetime import datetime
from time import sleep
from traceback import print_exc
#username2 = input("Enter your username (e.g., adhaw2@illinois.edu): ")
#password = getpass("Enter your password: ")
def pl_scrape(username2, password):
    try:
        firefox_service = Service('./geckodriver')
        firefox_options = Options()
        #firefox_options.add_argument("--headless")
        #driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        driver = webdriver.Firefox(service=firefox_service)
        driver.get("https://us.prairielearn.com/pl/auth/institution/3/saml/login")
        # with open("plcookies.json", 'r') as cookiesfile: #cookies
        #     cookies = json.load(cookiesfile)
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
        # driver.get("https://us.prairielearn.com")
        if "login.microsoftonline.com" in driver.current_url:
                sleep(2)
                print("\nLogging in to PrairieLearn System\n")
                username = driver.find_element(By.CSS_SELECTOR, "input[name='loginfmt']")
                username.send_keys(username2)
                driver.find_element(By.CSS_SELECTOR, "#idSIButton9").click()
                sleep(1)
                driver.find_element(By.CSS_SELECTOR, "input[name='passwd']").send_keys(password)
                driver.find_element(By.CSS_SELECTOR, "#idSIButton9").click()
        sleep(2)
        if "login.microsoftonline.com" in driver.current_url:
            raise("\nFailed: Wrong email or password!\n")
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
        print(unfinished)
        return unfinished
        # with open('correct.json', "w") as fp:
        #     json.dump(unfinished, fp)

        # with open('correct.json') as fp:
        #     correct = json.load(fp)

        # if correct == unfinished:
        #     print("Test Case Passed")
        #     print(correct)
        # else:
        #     raise Exception("Incorrect output")

    except:
        print_exc()
    driver.quit()
