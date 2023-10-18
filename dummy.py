# --------------------------------------------------------------------------------
# extracting data from elms instead of json data
# --------------------------------------------------------------------------------

# doctor_elm = docListSoup.find("div", class_="u-border-general--bottom")

# doctor_info["profile"] = (
#     doctor_elm.find("img", {"data-qa-id": "doctor-profile-image"})
#     .get("srcset")
#     .split(",")[2]
#     .split(" ")[0]
#     .strip()
# )

# doctor_info["name"] = (
#     doctor_elm.find("h1", {"data-qa-id": "doctor-name"}).get_text().strip()
# )

# specs_elm = doctor_elm.find("div", {"data-qa-id": "doctor-specializations"}).find("div")
# specs = [h2.get_text().strip() for h2 in specs_elm.find_all("h2")]
# doctor_info["specializations"] = " ".join(specs)

# doctor_info["experience"] = (
#     doctor_elm.find("div", {"data-qa-id": "doctor-specializations"})
#     .find_all("h2")[-1]
#     .get_text()[0:2]
# )

# doctor_info["varified_label"] = (
#     doctor_elm.find("span", {"data-qa-id": "doctor-verification-label"})
#     .find("span")
#     .get_text()
#     .strip()
# )

# doctor_info["experience_score"] = (
#     doctor_elm.find("p", {"data-qa-id": "doctor-patient-experience-score"})
#     .find("span", class_="u-green-text u-bold u-large-font")
#     .get_text()
#     .strip()
# )


# --------------------------------------------------------------------------------
# # checking if doctor_specilities is in the LIST
# --------------------------------------------------------------------------------
# doc_specialities = jsonData[0]["medicalSpecialty"]
# is_in_specilities_list = False

# for each in doc_specialities:
#     speciality = each.lower()

#     if speciality in specialities:
#         is_in_specilities_list = True
#     else:
#         new_specialities.append(speciality)

# if not is_in_specilities_list:
#     return {"status": False}


# specialities = [
#     "cardiology",
#     "neurology",
#     "orthopedics",
#     "endocrinology",
#     "gastroenterology",
#     "oncology",
#     "nephrology",
#     "rheumatology",
#     "pulmonology",
#     "dermatology",
#     "psychiatry",
#     "ophthalmology",
#     "radiology",
#     "anesthesiology",
#     "critical care medicine",
#     "hematology",
#     "neonatology",
#     "pathology",
#     "urology",
#     "gynecology and obstetrics",
#     "pediatrics",
#     "nuclear medicine",
#     "transplant surgery",
#     "plastic surgery",
#     "sports medicine",
#     "neurosurgery",
#     "pediatric surgery",
#     "interventional radiology",
#     "geriatric medicine",
#     "allergy and immunology",
#     "cardiothoracic surgery",
#     "forensic medicine",
#     "palliative medicine",
#     "infectious disease",
#     "emergency medicine",
#     "hepatology",
#     "vascular surgery",
#     "maxillofacial surgery",
#     "preventive and social medicine",
#     "trauma and acute care surgery",
# ]
