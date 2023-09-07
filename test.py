from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from bs4 import BeautifulSoup

url = "https://www.practo.com/bangalore/doctor/dr-anjali-shetty-dentist-1/recommended?practice_id=648474&specialization=Dentist&referrer=doctor_listing&page_uid=7545b5c4-b143-47db-8136-cfc174d50065"

driver = webdriver.Chrome()
driver.get(url)
names = set()


while True:
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa-id="view-more-feedback"]')
            )
        )
        load_more_button.click()
    except (NoSuchElementException, TimeoutException):
        break  # button not found or not clickable
    except StaleElementReferenceException:
        pass  # element is stale > continue the loop

soup = BeautifulSoup(driver.page_source, "html.parser")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


stories = []
seen_stories = set()
stories_elms = soup.find_all(
    "div", class_="pure-g feedback--item u-cushion--medium-vertical"
)

for story_elm in stories_elms:
    story = {}

    visitedSnippets = story_elm.find("p", {"data-qa-id": "visited-for"})
    if visitedSnippets is not None:
        titleSnippets = [
            each.text.strip()
            for each in visitedSnippets.find_all("span", class_="procedure")
        ]
        if len(titleSnippets) > 0:
            story["title"] = "Visited for " + ", ".join(titleSnippets)
    else:
        story["title"] = ""

    date_elm = story_elm.find("span", {"data-qa-id": "web-review-time"})
    story["date"] = " ".join(date_elm.stripped_strings)

    happyWithElms = story_elm.find("p", {"data-qa-id": "happy-with"})
    happy_with_list = (
        []
        if happyWithElms == None
        else [
            each.text.strip()
            for each in happyWithElms.find_all("span", class_="feedback__context")
        ]
    )
    story["happyWith"] = tuple(happy_with_list)

    story["review_text"] = (
        story_elm.find("p", {"data-qa-id": "review-text"})
        .get_text()
        .replace("*", "")
        .strip()
    )

    story_tuple = tuple(story.items())
    frozen_story = frozenset(story_tuple)

    if frozen_story not in seen_stories:
        seen_stories.add(frozen_story)  # making it 'seen'
        stories.append(dict(frozen_story))  # appending to list


print(f"\n\n{stories}\n\n")
print(len(stories))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# elements = driver.find_elements(
#     By.CSS_SELECTOR, "div.pure-g.feedback--item.u-cushion--medium-vertical"
# )

# for element in elements:
#     names.add(element.text)
#     # print(f"\n{element.text}\n")

# print(f"\n\n{names}\n\n")

driver.quit()
