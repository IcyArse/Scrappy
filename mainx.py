import requests
from bs4 import BeautifulSoup

# User credentials
email = 'amran@um.edu.my'
password = 'Superman@1000'

# Website login URL
login_url = 'https://www.turnitin.com/login_page.asp'

# Data URL (after login)
data_url = 'https://www.turnitin.com/data_page'  # Replace with the actual URL to download data

# Create a session to persist cookies and session information
session = requests.Session()

# Get the login page to extract necessary form data
login_page_response = session.get(login_url)
login_soup = BeautifulSoup(login_page_response.text, 'html.parser')

# Find the login form in the HTML
login_form = login_soup.find('form', {'name': 'login_form'})

# Construct login payload
login_payload = {
    'email': email,
    'password': password,
    # Include other form fields as needed based on the form
}

# The form action URL for posting login credentials
login_form_action_url = login_url  # Typically the same as the login page URL

# Submit the login form
login_response = session.post(login_form_action_url, data=login_payload)

# Check if login was successful
if login_response.ok:
    print('Login successful')
    
    # Get the redirected URL after login
    redirected_url = login_response.url
    
    print('Redirected URL after login:', redirected_url)
    
    # Prompt user to enter a class ID
    user_class_id = input('Enter the class ID: ')
    
    # Access the redirected page
    redirected_page_response = session.get(redirected_url)
    
    # Check if access to redirected page was successful
    if redirected_page_response.ok:
        # Parse the HTML of the redirected page
        redirected_soup = BeautifulSoup(redirected_page_response.text, 'html.parser')
        
        # Find the <td> element with the given class ID
        td_element = redirected_soup.find('td', class_='class_id', text=user_class_id)
        
        if td_element:
            # Get the parent <tr> element
            tr_element = td_element.parent
            
            # Find the <a> tag within the <td> with class_name class
            a_tag = tr_element.find('td', class_='class_name').find('a')
            
            if a_tag:
                href_value = a_tag['href']
                print(f"The href value associated with class ID {user_class_id} is: {href_value}")
            else:
                print(f"No <a> tag found for class ID {user_class_id}")
        else:
            print(f"Class ID {user_class_id} not found in the HTML content.")
    else:
        print('Failed to access the redirected page')
else:
    print('Login failed')
