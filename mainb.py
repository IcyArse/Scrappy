from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from random import randint
from dotenv import load_dotenv
import os
import json

# Load environment variables from credentials.env file
dotenv_path = os.path.join(os.path.dirname(__file__), 'credentials.env')
load_dotenv(dotenv_path)

# Get credentials from environment variables or prompt user
email_login = os.getenv("EMAIL") #or input("Enter your email: ")
password = os.getenv("PASSWORD") #or getpass("Enter your password: ")

# Prompt user for class ID
class_id = 43513647  # input("Enter the class ID: ")

file = open("tunitfrnt\server\data.json")
data = json.load(file)

#Submission ID & paper email
submission_id = data["submissionId"]
print("submission_id = ", submission_id)
paper_email = data["email"]
print("paper email = ", paper_email)

## Set Chrome options
chrome_options = Options()
#chrome_options.add_argument("--disable-infobars")
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
# Disable Chrome's automated testing detection
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_experimental_option('useAutomationExtension', False)

# Initialize Chrome WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)


# Website login URL
login_url = 'https://www.turnitin.com/login_page.asp'

# Open the login page
driver.get(login_url)

# Find email and password fields and submit button
email_field = driver.find_element(By.NAME, 'email')
password_field = driver.find_element(By.NAME, 'user_password')
submit_button = driver.find_element(By.NAME, 'submit')

# Enter user credentials
email_field.send_keys(email_login)
password_field.send_keys(password)

# Click the submit button
submit_button.click()

# Wait for the login process to complete
driver.implicitly_wait(10)

# Check if login was successful
if 't_home.asp' in driver.current_url:
    print('Login successful')

    # Find the <td> element with the given class ID
    td_element = driver.find_element(By.XPATH, f"//td[@class='class_id' and text()='{class_id}']")

    if td_element:
        # Get the parent <tr> element
        tr_element = td_element.find_element(By.XPATH, './..')
        
        # Find the <a> tag within the <td> with class_name class
        a_tag = tr_element.find_element(By.XPATH, ".//td[@class='class_name']/a")

        if a_tag:
            href_value = a_tag.get_attribute('href')
            print(f"The href value associated with class ID {class_id} is: {href_value}")

            driver.get(href_value)

            student_element = driver.find_element(By.XPATH, "//a[@tabindex='2' and text()='Students']")

            if student_element:
                href_value = student_element.get_attribute('href')
                driver.get(href_value)

                print("Student url: ", driver.current_url)

                driver.implicitly_wait(20)

                # Find all the elements with class "ibox_long student-email"
                email_elements = driver.find_elements(By.CSS_SELECTOR, ".ibox_long.student-email")

                # Iterate through each email element
                for email_element in email_elements:
                    # Get the email ID from the <a> element's text
                    email_id = email_element.find_element(By.TAG_NAME, "a").text
                    print("email id iterated through: ", email_id)
                    
                    # Check if the email ID matches the given email ID
                    if email_id == paper_email:
                        # Find the sibling "ibox_long student-name" element
                        name_element = email_element.find_element(By.XPATH, "./ancestor::tr/td[@class='ibox_long student-name']")
                        
                        # Get the link from the sibling element
                        href_value = name_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                        # Takes the driver to href value
                        driver.get(href_value)

                        # Print the link
                        print("Link for matching email ID:", href_value)
                        break

                # Find all the <tr> elements with <td> class "ibox_long"
                tr_elements = driver.find_elements(By.XPATH, "//tr[td[@class='ibox_long']]")

                # Iterate through each <tr> element
                for tr_element in tr_elements:
                    # Find the <a> tag within the <td> with class "ibox_long"
                    a_tag = tr_element.find_element(By.XPATH, ".//td[@class='ibox_long']/a")
                    
                    # Get the href attribute value of the <a> tag
                    href_value = a_tag.get_attribute("href")
                    
                    # Open the extracted link in a new tab
                    driver.execute_script("window.open(arguments[0], '_blank')", href_value)

                    # Switch to the newly opened window
                    new_window_handle = driver.window_handles[-1]
                    driver.switch_to.window(new_window_handle)

                    print("BEFORE INFO CLASS:", driver.current_url)
                    info_class_id = "sc-view sc-segment-view sc-large sc-static-layout tii-theme carta square segment vertical sc-regular-size tii-icon-info-outline sidebar-paper-info-button sc-last-segment sc-segment-1"
                    link = driver.find_element(By.XPATH, f"//div[@class='{info_class_id}']")

                    link.click()
                    time.sleep(5)

                    # Find the element containing the submission ID value
                    submission_id_element = driver.find_element(By.XPATH, "//div[@class='sc-view sc-collection-item sc-item sc-large submission-id allow-select tii-theme carta']/div[@class='value']")

                    # Extract the text from the element
                    submission_id_value = submission_id_element.text

                    # Compare the extracted submission ID value with the given submission ID
                    if submission_id_value == submission_id:
                        print("Submission ID matches the given submission ID:", submission_id_value)

                        driver.refresh()

                        download_class_id = "sc-view sc-segment-view sc-large sc-static-layout tii-theme carta square segment vertical sc-regular-size tii-icon-download sidebar-download-button sc-first-segment sc-segment-0"
                        link = driver.find_element(By.XPATH, f"//div[@class='{download_class_id}']")

                        link.click()

                        time.sleep(2)

                        download_class_id = "sc-view sc-list-item-view sc-collection-item sc-item sc-large tii-theme carta btn-link print-download-btn sc-regular-size"
                        link = driver.find_element(By.XPATH, f"//div[@class='{download_class_id}']")

                        print('current file : ',link)
                        link.click()


                    else:
                        print("Submission ID does not match the given submission ID")

                        driver.close()

                        # Switch to the newly opened window
                        new_window_handle = driver.window_handles[-1]
                        driver.switch_to.window(new_window_handle)

            time.sleep(60)
        else:
            print(f"No <a> tag found for class ID {class_id}")
    else:
        print(f"Class ID {class_id} not found in the HTML content.")
else:
    print('Login failed')