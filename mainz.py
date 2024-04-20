from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# User credentials
email = 'amran@um.edu.my'
password = 'Superman@1000'

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Website login URL
login_url = 'https://www.turnitin.com/login_page.asp'

# Data URL (after login)
data_url = 'https://www.turnitin.com/data_page'  # Replace with the actual URL to download data

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

    # Now navigate to the redirected page
    #driver.get(data_url)

    # Prompt user to enter a class ID
    user_class_id = 43513647#input('Enter the class ID: ')

    # Find the <td> element with the given class ID
    td_element = driver.find_element(By.XPATH, f"//td[@class='class_id' and text()='43513647']")

    if td_element:
        # Get the parent <tr> element
        tr_element = td_element.find_element(By.XPATH, './..')
        
        # Find the <a> tag within the <td> with class_name class
        a_tag = tr_element.find_element(By.XPATH, ".//td[@class='class_name']/a")

        if a_tag:
            href_value = a_tag.get_attribute('href')
            print(f"The href value associated with class ID {user_class_id} is: {href_value}")
        else:
            print(f"No <a> tag found for class ID {user_class_id}")
    else:
        print(f"Class ID {user_class_id} not found in the HTML content.")
else:
    print('Login failed')

# Close the browser
#driver.quit()
