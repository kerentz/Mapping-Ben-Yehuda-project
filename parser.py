import requests
from bs4 import BeautifulSoup
from DB import db, Work
import time
import re

WORK_ID_RANGE = 20
work_link_prefix = "https://benyehuda.org/read/"
author_link_prefix = "https://benyehuda.org/author/"


def parse_ben_yehuda():
    with open('errors', 'w+') as fd:
        all_works = []
        for work_id in range(10922,10923):
            work = parse_work(work_id)
            if type(work) != str:
                all_works.append(work)
            else:
                fd.write(work + "\n")
            time.sleep(1)

        db.session.bulk_save_objects(all_works)
        db.session.commit()


def is_prose(work_details):
    for work_detail in work_details:
        if "פרוזה" in work_detail.text:
            return True
    return False


def get_author_id(work_html):
    breadcrumbs_texts = work_html.body.find_all('div', attrs={'class': 'breadcrumbs-text'})
    for breadcrumb in breadcrumbs_texts:
        search_result = re.search('\/author\/(\d+)', str(breadcrumb))
        if search_result is not None:
            author_id = search_result.group(1)
            break
    return author_id


def get_work_name(work_html):
    return work_html.body.find('div', attrs={'class': 'headline-1-v02'}).text


def get_binding_book():
    # should return string or None
    return "Not_Yet_Implemented"


def get_general_note():
    return "Not_Yet_Implemented"


def get_edition_details(work_details):
    for work_detail in work_details:
        if "פרטי מהדורת מקור:" in work_detail.text:
            return work_detail.text.replace("פרטי מהדורת מקור:", "")
    return None


def get_more_information():
    return "Not_Yet_Implemented"


def parse_work(work_id):
    work_link = work_link_prefix + str(work_id)
    work_response = requests.get(work_link)
    if work_response.status_code != 200:
        return f"work_link did not work for {work_id}"
    work_html = BeautifulSoup(work_response.text, 'html.parser')
    work_details = work_html.body.find_all('div', attrs={'class': 'work-details'})
    if not is_prose(work_details):
        return ""
    edition_details = get_edition_details(work_details)
    author_id = get_author_id(work_html)
    work_name = get_work_name(work_html)
    author_link = author_link_prefix + str(author_id)
    author_response = requests.get(author_link)
    if author_response.status_code != 200:
        return f"author_link did not work for {work_id}"
    binding_book = get_binding_book()
    general_note = get_general_note()

    more_information = get_more_information()
    type_of_work = "סיפור" if binding_book else "ספר"

    return Work(
        general_note=general_note,
        genre="פרוזה",
        author_id=int(author_id),
        work_id=work_id,
        work_name=work_name,
        edition_details=edition_details,
        binding_book=binding_book,
        edition_id="",
        more_information=more_information,
        type=type_of_work,
    )

parse_ben_yehuda()
