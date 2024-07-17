# group-project-readme
Learning Management Assignment Collector (LeMAC)

Description: Our project eliminates the need of manually checking both Canvas and PrairieLearn for homework deadlines by automatically importing assignment data and displaying them in an integrated interface. Selenium webdrivers in Python are used in the backend.
Differences In Our Software Compared To Others: Our software is tailored to UIUC students, because we focused on including assignments from Canvas and PrairieLearn.

Group Members/Responsibilities:
Joseph Chen: PrairieLearn WebScraping
Aarul Dhawan: Canvas WebScraping and MySQL
Brian Beers: React Registration and Login 
Abhi Ramakrishnan:  Flask App Requests, React Big Calendar

Technical Architecture: Upon registration, it would check if its a valid login by calling the Flask App, and then running a selenium based function on the UIUC microsoft login page. If its a valid login, then it would add it to the MySQL database.  
When logging in, it would retrieve the login information from the SQL Database, and then call the Flask APP run selenium on the Canvas and PrairieLearn Management systems and scrape all the required information based on their HTML ID tags. Then we would display it on the frontend

Instructions:
Install the following libraries:
Selenium, Beautiful Soup, lxml, Flask, and React
Setup a MySQL Database, and change the password of the root database in canvas_scraper.py
cd into canvas_data and run python3 canvas_scraper.py
In a separate terminal, cd into login-signup and run npm start
