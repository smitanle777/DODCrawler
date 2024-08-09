from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (make sure to have the appropriate WebDriver installed, e.g., ChromeDriver)
driver = webdriver.Chrome()

# Open the page
driver.get("https://www.defense.gov/News/Contracts/Contract/Article/3799283/")

# Wait for the page to fully load
time.sleep(5)  # Adjust the sleep time if necessary

# Wait for the article content to load
wait = WebDriverWait(driver, 10)
article_content = driver.find_elements(By.TAG_NAME, 'p')

# Extract the article text
article_text = ' '.join([element.text for element in article_content])

# Print the page source to verify content
f = open("Desktop/DadProj/dodhtml.txt", "w")
f.write(article_text)
f.close()

# GETS THE LINKS FROM THE DOD WEBPAGE
# Open the page
# driver.get("https://www.defense.gov/News/Contracts/")

# Wait for the page to fully load
# time.sleep(5)  # Adjust the sleep time if necessary

# Print the page source to verify content
# f = open("Desktop/DadProj/dodhtml.txt", "w")
# f.write(driver.page_source)
# f.close()

# # Wait for the presence of elements containing the article links
# wait = WebDriverWait(driver, 10)
# contracts_list = wait.until(EC.visibility_of_element_located((By.ID, "alist")))

# # Find all contract links
# contract_links = contracts_list.find_elements(By.CSS_SELECTOR, "h3.title a")

# # Extract the href attributes
# article_links = [link.get_attribute("href") for link in contract_links]

# # Print the links
# for link in article_links:
#     print(link)

# Close the browser
driver.quit()
