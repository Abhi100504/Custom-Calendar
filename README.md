# Learning Management Assignment Collector (LeMAC)

LeMAC eliminates the need to manually check both Canvas and PrairieLearn for homework deadlines by automatically importing assignment data and displaying it in an integrated interface.

## Features

**Tailored to UIUC Students**: Focuses on including assignments from Canvas and PrairieLearn, specifically designed for University of Illinois Urbana-Champaign students.

## Group Members and Responsibilities

- **Abhi Ramakrishnan**: Flask App Requests, React Registration, Login, and Calendar
- **Aarul Dhawan**: Flask App Requests, Canvas WebScraping, and MySQL
- **Joseph Chen**: PrairieLearn WebScraping

## Technical Architecture

1. **Registration**:
   - Validates login by calling the Flask App and running a Selenium-based function on the UIUC Microsoft login page.
   - If the login is valid, adds it to the MySQL database.

2. **Login**:
   - Retrieves login information from the SQL Database.
   - Calls the Flask App to run Selenium on Canvas and PrairieLearn systems, scraping all required information based on their HTML ID tags.
   - Displays the scraped data on the frontend.

## Installation and Setup

### Prerequisites

Ensure you have the following libraries and tools installed:

- Selenium
- Beautiful Soup
- lxml
- Flask
- React
- MySQL

### Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/LeMAC.git
    cd LeMAC
    ```

2. **Setup MySQL Database**:
    - Create a MySQL database.
    - Update the `canvas_scraper.py` file with your MySQL root password.

3. **Install Python Dependencies**:
    ```sh
    pip install selenium beautifulsoup4 lxml Flask
    ```

4. **Run the Canvas Scraper**:
    ```sh
    cd canvas_data
    python3 canvas_scraper.py
    ```

5. **Run the React Frontend**:
    - Open a separate terminal.
    ```sh
    cd login-signup
    npm install
    npm start
    ```

## Example Use Case

Imagine you are a UIUC student juggling multiple assignments from different platforms. LeMAC simplifies your life by integrating Canvas and PrairieLearn assignments into one seamless interface, ensuring you never miss a deadline again.

## Technical Implementation

### Data Sources

- **Canvas and PrairieLearn**: Web scraping performed using Selenium.

### Steps

1. **Extract Assignment Data**:
    - Use Selenium to scrape assignment data from Canvas and PrairieLearn.
    - Process this data using Python and store it in a MySQL database.

2. **Display Assignments**:
    - Retrieve assignment data from MySQL.
    - Use Flask to serve the data to the React frontend.
    - Display the assignments in an integrated calendar view.
