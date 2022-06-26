import os
from dotenv import load_dotenv

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

    time_entry(0, "Client", "2022-06-13", "Configuration", "1", "Desc")
    add_another_response(0)


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
    client_selection = driver.find_element(By.XPATH, '//div[contains(@class, "tt-dataset")]')
    wait = WebDriverWait(driver, 20);
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tt-dataset")));
    client_selection.click()

def enter_date(index, date):
    date_field = driver.find_element(By.ID, date_field_id(index))
    date_field.click()
    day_icon = driver.find_element(By.XPATH, '//span[@data-date="' + date + '"]')
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