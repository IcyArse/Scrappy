import time
from dotenv import load_dotenv
import os
import json

error_file_path = "error.json"
error_data = None

# Write data to the JSON file
with open(error_file_path, "w") as json_file:
    json.dump(error_data, json_file)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Load environment variables from credentials.env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get credentials from environment variables or prompt user
email_login = os.getenv("EMAIL") #or input("Enter your email: ")
password = os.getenv("PASSWORD") #or getpass("Enter your password: ")

# Opens the json file
file = open("data.json")
data = json.load(file)

#Submission ID & paper email
submission_id = data["submissionId"]
paper_email = data["email"]

## Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
headless = True
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

# Sets current directory path and relative path
current_dir = os.getcwd()
relative_download_dir = 'downloads'

# Combine the current directory with the relative path to get the absolute path
download_dir = os.path.join(current_dir, relative_download_dir)
print(download_dir)

# Sets the custom download directory
prefs = {'download.default_directory' : download_dir}
chrome_options.add_experimental_option('prefs', prefs)

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

    # initial value to test for faliure
    thesis_href_value = None

    # Find all <tr> elements
    tr_elements = driver.find_elements(By.TAG_NAME, "tr")
    
    # Loop over each <tr> element
    for tr_element in tr_elements:

        # Find the <td> element with the given class ID
        td_element = driver.find_element(By.XPATH, f"//td[@class='class_name']/a")

        if td_element and td_element.text == "Thesis":
            thesis_href_value = td_element.get_attribute('href')

            driver.get(thesis_href_value)

            student_element = driver.find_element(By.XPATH, "//a[@tabindex='2' and text()='Students']")

            if student_element:
                href_value = student_element.get_attribute('href')
                driver.get(href_value)

                driver.implicitly_wait(20)

                # Find all the elements with class "ibox_long student-email"
                email_elements = driver.find_elements(By.CSS_SELECTOR, ".ibox_long.student-email")

                # Iterate through each email element
                for email_element in email_elements:
                    # Get the email ID from the <a> element's text
                    email_id = email_element.find_element(By.TAG_NAME, "a").text
                    
                    # Check if the email ID matches the given email ID
                    if email_id == paper_email:
                        # Find the sibling "ibox_long student-name" element
                        name_element = email_element.find_element(By.XPATH, "./ancestor::tr/td[@class='ibox_long student-name']")
                        
                        # Get the link from the sibling element
                        href_value = name_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                        # Takes the driver to href value
                        driver.get(href_value)
                        break
                print(email_id)
                print(paper_email)
                if email_id != paper_email:
                    print("Email ID not present, please enter a valid email.")

                    error_file_path = "error.json"
                    error_data = {'download_error': 'Email ID not present, please enter a valid email.'}

                    # Write data to the JSON file
                    with open(error_file_path, "w") as json_file:
                        json.dump(error_data, json_file)
                    
                    driver.quit()
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

                    driver.maximize_window

                    if headless:
                        setting_button_link = "sc-view sc-button-view popup-button-view sc-medium tii-icon-settings misc-popup-button-view tii-theme carta square button sc-regular-size"
                        button_link = driver.find_element(By.XPATH, f"//div[@class='{setting_button_link}']")

                        button_link.click()
                        time.sleep(1)
                        info_class_id = "sc-view sc-segment-view tii-icon-info-outline sidebar-paper-info-button sc-static-layout tii-theme carta square segment sc-last-segment sc-segment-1 sc-regular-size sc-medium"
                        link = driver.find_element(By.XPATH, f"//div[@class='{info_class_id}']")

                        link.click()

                        # Find the element containing the submission ID value
                        submission_id_path = "sc-view sc-collection-item sc-item sc-medium submission-id allow-select tii-theme carta"
                        submission_id_element = driver.find_element(By.XPATH, f"//div[@class='{submission_id_path}']/div[@class='value']")

                        filename_id_path = "sc-view sc-collection-item sc-item sc-medium file-name allow-select tii-theme carta"
                        filename_element = driver.find_element(By.XPATH, f"//div[@class='{filename_id_path}']/div[@class='value']")
                        filename_file = (filename_element.text).split('.')[0] + '.pdf'

                        # Extract the text from the element
                        submission_id_value = submission_id_element.text

                    # Only used for testing purposes   
                    else:
                        info_class_id = "sc-view sc-segment-view sc-large sc-static-layout tii-theme carta square segment vertical sc-regular-size tii-icon-info-outline sidebar-paper-info-button sc-last-segment sc-segment-1"
                        link = driver.find_element(By.XPATH, f"//div[@class='{info_class_id}']")

                        link.click()
                        time.sleep(5)

                        # Find the element containing the submission ID value
                        submission_id_path = "sc-view sc-collection-item sc-item sc-large submission-id allow-select tii-theme carta"
                        submission_id_element = driver.find_element(By.XPATH, f"//div[@class='{submission_id_path}']/div[@class='value']")

                        filename_element = driver.find_element(By.XPATH, "//div[@class='sc-view sc-collection-item sc-item sc-large file-name allow-select tii-theme carta']/div[@class='value']")
                        filename_file = (filename_element.text).split('.')[0] + '.pdf'

                        # Extract the text from the element
                        submission_id_value = submission_id_element.text
 
                    # Compare the extracted submission ID value with the given submission ID
                    if submission_id_value == submission_id:
                        driver.refresh()
                        
                        time.sleep(10)
                        link = driver.find_element(By.XPATH, "//div[@id='sc4727']//tii-aiw-button")
                            
                        link.click()
                        link.click()

                        time.sleep(5)    

                        # Switch to the newly opened window
                        new_window_handle = driver.window_handles[-1]
                        driver.switch_to.window(new_window_handle)

                        # Find the top-level shadow root element
                        tii_ai_writing_app = driver.find_element(By.CSS_SELECTOR, 'tii-ai-writing-app.hydrated')

                        # Access the shadow root
                        shadow_root = driver.execute_script('return arguments[0].shadowRoot', tii_ai_writing_app)

                        # Find the next level shadow root elements recursively
                        tii_router = shadow_root.find_element(By.CSS_SELECTOR, 'tii-router.hydrated')
                        shadow_root_1 = driver.execute_script('return arguments[0].shadowRoot', tii_router)

                        aiwa_home = shadow_root_1.find_element(By.CSS_SELECTOR, 'aiwa-home.hydrated')
                        shadow_root_2 = driver.execute_script('return arguments[0].shadowRoot', aiwa_home)

                        download_button = shadow_root_2.find_element(By.CSS_SELECTOR, 'tii-sws-download-btn-mfe.hydrated')
                        shadow_root_3 = driver.execute_script('return arguments[0].shadowRoot', download_button)

                        report_download_button = shadow_root_3.find_element(By.CSS_SELECTOR, 'button')
                
                        # Click on the button element
                        download_button.click()
                        report_download_button.click()
                            
                        timeout = 120  # seconds
                        start_time = time.time()
                        while True:
                             # Check if timeout exceeded
                            if time.time() - start_time > timeout:
                                print("Download timed out.")
                                break

                            # Check if the file is still being downloaded
                            if any(filename == filename_file for filename in os.listdir(download_dir)):
                                print("Download completed.")

                                # Check if the download directory is empty
                                if os.listdir(download_dir):
                                    # Get the list of files in the directory
                                    files = os.listdir(download_dir)
                                    # Assuming only one file is present, get its name
                                    file_name = filename_file
                                    # Get the full file path by joining the download directory with the file name
                                    file_path = os.path.join(download_dir, file_name)

                                    filedata = {submission_id:{"filename":file_name,"filepath":file_path}}
                                    file_path = "filedata.json"

                                    # Read the existing JSON data from the file
                                    with open(file_path, 'r') as file:
                                        existing_data = json.load(file)

                                    existing_data.update(filedata)

                                    # Write data to the JSON file
                                    with open(file_path, "w") as json_file:
                                        json.dump(existing_data, json_file)
                                break
                        break


                    else:
                        driver.close()

                        # Switch to the newly opened window
                        new_window_handle = driver.window_handles[-1]
                        driver.switch_to.window(new_window_handle)

                if submission_id_value == submission_id:
                    pass
                else:
                    print("Submission ID does not match, please enter a valid ID")

                    error_file_path = "error.json"
                    error_data = {'download_error': 'Submission ID does not match, please enter a valid ID'}

                    # Write data to the JSON file
                    with open(error_file_path, "w") as json_file:
                        json.dump(error_data, json_file)
                    driver.quit()
                    break
            break
            
else:
    print('Login failed')

try:
    if not thesis_href_value:
        print("Your thesis is not present on the platform.")
except:
    pass
driver.quit()
