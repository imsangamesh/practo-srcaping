from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re


url = "https://www.practo.com/bangalore/doctor/dr-ganesh-shetty-dentist/recommended?practice_id=648474&specialization=Dentist&referrer=doctor_listing&page_uid=513c6021-660f-4d8f-8b53-9bca3b946f26"
driver = webdriver.Chrome()
driver.get(url)


# Wait for the right-side-panel element to LOAD
# WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.CLASS_NAME, "pure-u-8-24.right-panel-section"))
# )
soup = BeautifulSoup(driver.page_source, "html.parser")


html_text = soup.find("div", class_="c-slots-header pure-g")

print(html_text)
