import requests
from bs4 import BeautifulSoup
from DB import db, Work
import time

WORK_ID_RANGE = 20
work_link_prefix = "https://benyehuda.org/read/"
author_link_prefix = "https://benyehuda.org/author/"


def parse_ben_yehuda():
    with open('errors', 'w+') as fd:
        all_works = []
        for work_id in range(WORK_ID_RANGE):
            work = parse_work(work_id)
            print(work)
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


def get_author_id_and_work_name(work_details, work_html):
    # Should return int and string
    return 5, 'bla'


def get_binding_book():
    # should return string or None
    pass


def get_general_note():
    pass


def get_edition_details():
    pass


def get_more_information():
    pass


def parse_work(work_id):
    work_link = work_link_prefix + str(work_id)
    work_response = requests.get(work_link)
    if work_response.status_code != 200:
        return f"work_link did not work for {work_id}"
    work_html = BeautifulSoup(work_response.text, 'html.parser')
    work_details = work_html.body.find_all('div', attrs={'class': 'work-details'})
    if not is_prose(work_details):
        return ""
    author_id, work_name = get_author_id_and_work_name(work_details, work_html)
    author_link = author_link_prefix + str(author_id)
    author_response = requests.get(author_link)
    if author_response.status_code != 200:
        return f"author_link did not work for {work_id}"
    binding_book = get_binding_book()
    general_note = get_general_note()
    edition_details = get_edition_details()
    more_information = get_more_information()
    type_of_work = "סיפור" if binding_book else "ספר"

    return Work(
        general_note=general_note,
        genre="פרוזה",
        author_id=author_id,
        work_id=work_id,
        work_name=work_name,
        edition_details=edition_details,
        binding_book=binding_book,
        edition_id="",
        more_information=more_information,
        type=type_of_work,
    )

parse_ben_yehuda()
