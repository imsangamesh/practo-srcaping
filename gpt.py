from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time

url = "https://www.practo.com/bangalore/doctor/dr-ganesh-shetty-dentist/recommended?practice_id=648474&specialization=Dentist&referrer=doctor_listing&page_uid=513c6021-660f-4d8f-8b53-9bca3b946f26"
driver = webdriver.Chrome()
driver.get(url)


all_available_slots = []

while True:
    # scraping AVAILABLE SLOTS
    soup = BeautifulSoup(driver.page_source, "html.parser")

    available_slots_elm = soup.find(
        "div", class_="pure-u-8-24 right-panel-section"
    ).find("div", class_="appointment")

    available_slot = {}

    raw_slot_details = (
        available_slots_elm.find("div", class_="c-slots-header pure-g")
        .find("div")
        .find(
            "button",
            class_="pure-u-1-3 c-btn--unstyled c-day-label c-day-label--selected",
        )
        .stripped_strings
    )
    slot_details = [each for each in raw_slot_details]

    available_slot["date"] = slot_details[0]
    no_of_slots = slot_details[1].replace(" slots available", "")

    if no_of_slots == "No":
        available_slot["no_of_slots"] = 0
    else:
        available_slot["no_of_slots"] = int(no_of_slots)

    # condition to check if NO_AVAILABLE_SLOT html element is present or not
    no_available_slots_elm = soup.find("div", {"data-qa-id": "no_slots_msg"})

    if no_available_slots_elm is None:
        # proceeding if slots are available
        slot_session_elms = available_slots_elm.find(
            "div", class_="c-day-slot"
        ).find_all("div", class_="pure-g c-day-session u-cushion--vertical")
        available_sessions = []

        for session_elm in slot_session_elms:
            session = {}

            raw_session_details = session_elm.find(
                "div", class_="c-day-session__header"
            ).stripped_strings
            session_details = [each for each in raw_session_details]

            session["time_of_the_day"] = session_details[0]
            session["no_of_slots"] = int(re.search(r"\d+", session_details[1]).group())

            session_timing_elms = session_elm.find(
                "div", class_="c-day-session__body pure-g"
            ).find_all("button")

            session["session_timings"] = [each.text for each in session_timing_elms]

            available_sessions.append(session)

        available_slot["available_sessions"] = available_sessions

    # finally pushing the SLOT_DATA
    print(f"\n\nAVALIABLE SLOT:\n{available_slot}\n\n")
    all_available_slots.append(available_slot)

    # TAPPING the NEXT_BUTTON if not 'disabled'
    try:
        next_button = driver.find_element(
            By.XPATH,
            '//button[@data-qa-id="slots_next"]',
        )
        next_button.click()
    except NoSuchElementException:
        break


driver.quit()


print("\n\n-----------------------------------\n")
print(all_available_slots)
