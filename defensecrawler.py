import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openai import OpenAI

class Contract:
    def __init__(self, company, amount, branch, project, duedate, stockticker, stramt):
        self.company = company
        self.amount = amount
        self.branch = branch
        self.project = project
        self.duedate = duedate
        self.stockticker = stockticker
        self.stramt = stramt

    def __str__(self):
        return f"{self.company} \nContract Amount: {self.stramt} \nContracting Branch: {self.branch} \nProject: {self.project} \nDelivery Due Date: {self.duedate} \nStock Ticker: {self.stockticker}"

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch page: {url}")
    
# def parse_main_page(html):
#     driver = webdriver.Chrome()

#     driver.get("https://www.defense.gov/News/Contracts/")

#     wait = WebDriverWait(driver, 10)
#     contracts_list = wait.until(EC.visibility_of_element_located((By.ID, "alist")))

#     # Find all contract links
#     contract_links = contracts_list.find_elements(By.CSS_SELECTOR, "h3.title a")

#     # Extract the href attributes
#     article_links = [link.get_attribute("href") for link in contract_links]

#     # # Print the links
#     # for link in article_links:
#     #     print(link)

#     return article_links

def parse_page(html):
    # Initialize the WebDriver (make sure to have the appropriate WebDriver installed, e.g., ChromeDriver)
    driver = webdriver.Chrome()

    # Open the page
    driver.get(html)

    # Wait for the page to fully load
    time.sleep(5)  # Adjust the sleep time if necessary

    # Wait for the article content to load
    wait = WebDriverWait(driver, 10)
    article_content = driver.find_elements(By.TAG_NAME, 'p')

    # Extract the article text
    article_text = ' '.join([element.text for element in article_content])

    return article_text

def submit_to_ai(daily_contract):
    client = OpenAI()
    content_plus_contract = "Please list the names of the companies awarded a contract, the dollar amount of the contract, the branch that was creating the contract, what is being asked, the delivery due date, and the stock ticker for the company if applicable. Use Textron Aviation as the template for each contract: Textron Aviation Inc. Contract Amount: $8,388,771 Contracting Branch: Navy Project: Production and delivery of a multi-engine training system aircraft Delivery Due Date: November 2025 Stock Ticker: TXT There should be no new lines except for one inbetween each contract template. Add no labels in between each template contract. If any of the categories do not apply or do not have an answer, put N/A. If the contract is awarded to multiple companies, list all companies separated by semicolons on the same line under 'Company.' Ensure the format remains consistent.: " + daily_contract
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        { "role": "system", "content": content_plus_contract }
    ]
    )

    contracts = completion.choices[0].message.content.strip().split("\n")

    # f = open("Desktop/DadProj/dodhtml.txt", "w")
    # f.write(completion.choices[0].message.content)
    # f.close()

    newlist = [x.strip() for x in contracts if any(y.isalpha() for y in x)]

    return newlist

def create_obj_list(contract_list):
    contract_objs = []
    for first in contract_list:
        
        company = first[0: first.index("Contract Amount:")].strip()

        amount = first[first.index("$"):first.index("Contracting")].strip()
        stramt = amount
        amount = amount.strip("$").replace(",", "")
        amount = int(amount)

        branch = first[first.index("Contracting Branch: "):first.index("Project")].strip().strip("Contracting Branch:")

        project = first[first.index("Project: "):first.index("Delivery Due Date:")].strip().strip("Project:")
        project = project.strip()

        duedate = first[first.index("Delivery Due Date:"):first.index("Stock Ticker:")].strip().strip("Delivery Due Date:")
        duedate = duedate.strip()

        stockticker = first[first.index("Stock Ticker:"):].strip().strip("Stock Ticker:")
        stockticker = stockticker.strip()

        c = Contract(company, amount, branch, project, duedate, stockticker, stramt)
        contract_objs.append(c)

    return contract_objs

def order_by_contract_size(contract_objs):
    new_list = sorted(contract_objs, key=lambda x: x.amount, reverse=True)
    return new_list

def main():
    url = input("Enter link to contract: ") 
    contract_text = parse_page(url)
    ai_output = submit_to_ai(contract_text)
    objs_ouput = create_obj_list(ai_output)
    ordered_objs = order_by_contract_size(objs_ouput)
    for i in range(5): 
        print(ordered_objs[i])
        print("\n")

if __name__ == "__main__":
    main()
