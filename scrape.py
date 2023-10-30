from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
import requests
import json

# Name
# Degree
# Experience
# Verified
# Rating
# Description

# Slots available
# Clinic Name
# Address
# Work timings

# All the user stories
# Story title
# date
# tags
# story


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Scrape AVAILABLE SLOTS
def scrape_all_slots(doctor_page_url):
    driver = webdriver.Chrome()
    driver.get(doctor_page_url)

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
                session["no_of_slots"] = int(
                    re.search(r"\d+", session_details[1]).group()
                )

                session_timing_elms = session_elm.find(
                    "div", class_="c-day-session__body pure-g"
                ).find_all("button")

                session["session_timings"] = [each.text for each in session_timing_elms]

                available_sessions.append(session)

            available_slot["available_sessions"] = available_sessions

        # finally pushing the SLOT_DATA
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
    return all_available_slots


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Scrape FEEDBACKS
def scrape_all_feedbacks(docDetailSoup):
    feedbacks = []
    feedbacks_elms = docDetailSoup.find_all(
        "div", class_="pure-g feedback--item u-cushion--medium-vertical"
    )

    for eachFeedback in feedbacks_elms:
        print("\n------------------ FEEDBACKS -------------------------\n")
        feedback = {}

        visitedSnippets = eachFeedback.find("p", {"data-qa-id": "visited-for"})
        if visitedSnippets is not None:
            titleSnippets = [
                each.text.strip()
                for each in visitedSnippets.find_all("span", class_="procedure")
            ]
            if len(titleSnippets) > 0:
                feedback["title"] = "Visited for " + ", ".join(titleSnippets)

        date_elm = eachFeedback.find("span", {"data-qa-id": "web-review-time"})
        feedback["date"] = " ".join(date_elm.stripped_strings)

        happyWithElms = eachFeedback.find("p", {"data-qa-id": "happy-with"})
        feedback["happyWith"] = (
            []
            if happyWithElms == None
            else [
                each.text.strip()
                for each in happyWithElms.find_all("span", class_="feedback__context")
            ]
        )

        feedback["review_text"] = (
            eachFeedback.find("p", {"data-qa-id": "review-text"})
            .get_text()
            .replace("*", "")
            .strip()
        )

        feedbacks.append(feedback)

    return feedbacks


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Scrape DOCTOR_DETAILS
def scrape_doctor_details(doctor_elm):
    # extracting doctor_detail_URL and scraping data in it
    doctor_detail_page_url = "https://www.practo.com" + (
        doctor_elm.find("div", class_="info-section")
        .find("a")
        .get("href")
        .strip()
        .replace("?practice_id", "/recommended?practice_id")
    )
    response = requests.get(doctor_detail_page_url)
    docDetailSoup = BeautifulSoup(response.text, "html.parser")
    doctor_info = {}

    rawJsonData = docDetailSoup.find("script", {"type": "application/ld+json"}).string
    jsonData = json.loads(rawJsonData)

    # Name
    doctor_info["name"] = jsonData[0]["name"]

    # Page Url
    doctor_info["doctor_page_url"] = doctor_detail_page_url

    # Image
    doctor_info["image"] = jsonData[0]["image"]

    # Type
    doctor_info["type"] = jsonData[0]["@type"]

    # Description
    doctor_info["description"] = jsonData[0]["description"]

    # Degree
    doctor_info["degree"] = jsonData[0]["medicalSpecialty"]

    # Address
    doctor_info["address"] = jsonData[0]["address"]

    # Rating
    doctor_info["rating"] = jsonData[0]["aggregateRating"]["ratingValue"]

    # Work timings
    doctor_info["work_timings"] = jsonData[0]["memberOf"][0]["openingHours"][0]

    # Clinic Name
    doctor_info["clinic_name"] = jsonData[0]["memberOf"][0]["name"]

    # Varified Label
    doctor_info["varified_label"] = (
        docDetailSoup.find("span", {"data-qa-id": "doctor-verification-label"})
        .find("span")
        .get_text()
        .strip()
    )

    # Feedbacks (stories)
    doctor_info["feedbacks"] = scrape_all_feedbacks(docDetailSoup)

    # Avaliable Slots
    doctor_info["available_slots"] = scrape_all_slots(doctor_detail_page_url)

    return doctor_info


base_url = "https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22Dentist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=Bangalore&page="
doctors_data = []

for page_number in range(1, 6):
    url = base_url + str(page_number)
    response = requests.get(url)

    docListSoup = BeautifulSoup(response.text, "html.parser")
    doctors_list_elms = docListSoup.find_all("div", class_="listing-doctor-card")

    for doctor_elm in doctors_list_elms:
        print("\n------------------ DOCTOR DETAIL -------------------------\n")
        doc_data = scrape_doctor_details(doctor_elm)

        doctors_data.append(doc_data)

    time.sleep(1)  # optional delay before fetching next page
    break


# for data in doctors_data:
#     print("\n-------------------------------------------\n")
#     print(data)
#     print("\n-------------------------------------------\n")

with open("output.json", "w") as json_file:
    json.dump(doctors_data, json_file)
    print("\nOutput stored in JSON file")
