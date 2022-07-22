import os
import csv
import math
import time
from dotenv import load_dotenv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

def main():
    TIMESHEET_URL = os.getenv("TIMESHEET_URL")
    timesheet_csv = "timesheet.csv"

    load_page(TIMESHEET_URL)
    driver.maximize_window()

    index = 0

    with open(timesheet_csv, newline='') as csvfile:
        count_reader = csv.DictReader(csvfile)
        total_rows = 0
        for row in count_reader:
            total_rows += 1

    with open(timesheet_csv, newline='') as csvfile:
        timesheet_reader = csv.DictReader(csvfile)
        for row in timesheet_reader:
            client = row['Project']
            date = row['Date']
            action = row['Task']
            time2 = row['Time (decimal)']
            desc = row['Description']

            time_entry(index, client, format_date(date), action, format_time(time2), desc)
            driver.execute_script("!!document.activeElement ? document.activeElement.blur() : 0");

            add_another_response(index)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            index += 1


### OTHER METHODS ###

def format_time(time_str):
    return math.ceil(float(time_str)*4)/4

def format_date(date_str):
    date = datetime.strptime(date_str, "%m/%d/%y").date()
    return date.strftime("%Y-%m-%d")


### DATA ENTRY METHODS ###

def time_entry(index, project, date, action, time, description):
    enter_project(index, project)
    enter_date(index, date)
    enter_action(index, action)
    enter_time(index, time)
    enter_description(index, description)

def enter_project(index, project):
    project_field = driver.find_element(By.ID, project_field_id(index))
    project_field.send_keys(project)
    dataset_number = str(index * 2)
    client_selection = project_field.find_element(By.XPATH, '//div[contains(@class, "tt-dataset-' + dataset_number + '")]')
    wait = WebDriverWait(driver, 20);
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tt-dataset-" + dataset_number)));
    client_selection.click()

def enter_date(index, date):
    date_field = driver.find_element(By.ID, date_field_id(index))
    date_field.click()
    day_icon = date_field.find_element(By.XPATH, '//span[@data-date="' + date + '" and not(ancestor::div[contains(@style, "display: none")]) and not(ancestor::div[contains(@style, "display: none")])]')
    day_icon.click()

def enter_action(index, action):
    action_field = driver.find_element(By.ID, action_field_id(index))
    action_select = Select(action_field)
    action_select.select_by_visible_text(action.title())

def enter_time(index, time):
    time_field = driver.find_element(By.ID, time_field_id(index))
    time_field.send_keys(time)

def enter_description(index, description):
    desc_field = driver.find_element(By.ID, desc_field_id(index))
    desc_field.send_keys(description)



### SUBMISSION METHODS ###

def add_another_response(index):
    add_another = driver.find_element(By.ID, another_response_id(index))
    add_another.click()

def submit():
    button_id = "submit_button"
    submit_button = driver.find_element(By.ID, button_id)
    submit_button.click()


### START/END METHODS ###

def load_page(url):
    driver.implicitly_wait(2)
    driver.get(url)


### FIELD HELPER METHODS ###

def another_response_id(index):
    return "tfa_6-wfDL" if index == 0 else "tfa_6[0]-wfDL"

def project_field_id(index):
    return "tfa_7" if index == 0 else "tfa_7[" + str(index) + "]"

def date_field_id(index):
    return "tfa_869" if index == 0 else "tfa_869[" + str(index) + "]"

def action_field_id(index):
    return "tfa_9" if index == 0 else "tfa_9[" + str(index) + "]"

def time_field_id(index):
    return "tfa_870" if index == 0 else "tfa_870[" + str(index) + "]"

def desc_field_id(index):
    return "tfa_8" if index == 0 else "tfa_8[" + str(index) + "]"

if __name__ == "__main__":
    main()