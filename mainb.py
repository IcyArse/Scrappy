from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from random import randint

# Prompt user for email and password
email = 'amran@um.edu.my'  # input("Enter your email: ")

# Securely ask for the password
password = 'Superman@1000'  # getpass("Enter your password: ")

# Prompt user for class ID
class_id = 43513647  # input("Enter the class ID: ")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
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

# Set user-agent to mimic a real browser
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
)

# Initialize Chrome WebDriver with options
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
email_field.send_keys(email)
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
            view_element = driver.find_element(By.XPATH, f"//td[@class='assgn-inbox']/a")

            if view_element:
                href_value = view_element.get_attribute('href')

                # Find the <a> tag within the <td> with class_name class
                print(f"The href value associated with ID View is: {href_value}")
                driver.get(href_value)

                driver.implicitly_wait(20)
                # sim_element = driver.find_element(By.XPATH, f"//td[@class='or-score-column' and @data-title='Similarity Score']/a")
                # print(sim_element)
                # if sim_element:
                #    href_value = sim_element.get_attribute('href')
                # Find the <a> tag within the <td> with class_name class
                #    print(f"The href value associated with sim ID is: {href_value}")
                # driver.get(href_value)

                link = driver.find_element(By.XPATH, f"//a[@class='similarity-open']")

                link.click()
                print(driver.current_url)

                driver.implicitly_wait(20)
                '''
                button_link = driver.find_element(By.XPATH, f"//div[@id='sc4694']")
                driver.implicitly_wait(20)
                if button_link:
                    button_link.click()'''

                download_class_id = "sc-view sc-segment-view sc-large sc-static-layout tii-theme carta square segment vertical sc-regular-size tii-icon-download sidebar-download-button sc-first-segment sc-segment-0"
                link = driver.find_element(By.XPATH, f"//div[@title='Download']")
                print(link)

                link.click()

            time.sleep(1000)
        else:
            print(f"No <a> tag found for class ID {class_id}")
    else:
        print(f"Class ID {class_id} not found in the HTML content.")
else:
    print('Login failed')

# Function to mimic human-like behavior by introducing random delays
def random_delay():
    time.sleep(randint(3, 5))  # Random delay between 3 to 5 seconds

# Mimic human-like behavior before closing the browser
random_delay()

# Close the browser
driver.quit()