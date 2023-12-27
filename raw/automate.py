from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Path to Tor Browser directory containing the profile
tor_browser_path = '/home/deepak/Downloads/tor-browser/'

# Initialize options for Firefox
options = Options()
options.profile = tor_browser_path + 'Browser/TorBrowser/Data/Browser/profile.default'
options.binary_location = '/usr/bin/firefox115'  # Path to your Firefox binary

# Set geckodriver path using Service object
geckodriver_path = '/usr/local/bin/geckodriver'  # Replace with your geckodriver executable path
service = webdriver.firefox.service.Service(geckodriver_path)
service.start()

# Use the Tor browser profile with Selenium WebDriver and Service object for geckodriver
driver = webdriver.Firefox(service=service, options=options)

# Open Ahmia website
driver.get('https://ahmia.fi/')

# Wait for the page to load completely (adjust the time according to your internet speed)
time.sleep(5)

# Find the search input field by its name (you can inspect the webpage to get the correct selector)
search_input = driver.find_element_by_name('q')

# Enter the keyword(s) you want to search for
keyword = 'drugs'
search_input.send_keys(keyword)

# Simulate pressing Enter to perform the search
search_input.send_keys(Keys.RETURN)

# Wait for search results to load (you might need to adjust this wait time)
time.sleep(5)

# Now you can extract and process the search results as needed

# Finally, close the browser window
driver.quit()
