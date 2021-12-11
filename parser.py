import requests
from bs4 import BeautifulSoup
from DB import db, Work
import time
import re

WORK_ID_RANGE = 100
work_link_prefix = "https://benyehuda.org/read/"
author_link_prefix = "https://benyehuda.org/author/"


def parse_ben_yehuda():
    with open('errors', 'w+') as fd:
        for work_id in range(1, 30654):
            print(work_id)
            work = parse_work(work_id)
            print(work)
            if type(work) == str:
                fd.write(work + "\n")
            time.sleep(0.2)


def is_prose(work_details):
    for work_detail in work_details:
        if "פרוזה" in work_detail.text:
            return True
    return False


def get_author_id(work_html):
    author_id = None
    work_page_top_info_card = work_html.body.find('div', attrs={'class': 'work-page-top-info-card'})
    search_result = re.search('\/author\/(\d+)', str(work_page_top_info_card))
    if search_result is not None:
        author_id = search_result.group(1)
    return author_id
    # breadcrumbs_texts = work_html.body.find_all('div', attrs={'class': 'breadcrumbs-text'})
    # for breadcrumb in breadcrumbs_texts:
    #     search_result = re.search('\/author\/(\d+)', str(breadcrumb))
    #     if search_result is not None:
    #         author_id = search_result.group(1)
    #         break
    # return author_id


def get_work_name(work_html):
    return work_html.body.find('div', attrs={'class': 'headline-1-v02'}).text


def is_volume(item):
    text = item.text
    return text.startswith("כרך ") or text.startswith("חלק ")


def check_binding_book_problematic_cases(binding_book):
    return "href" in str(binding_book) or "במקור" in binding_book.text


def get_binding_book_and_volume(work_tag, possible_tags):
    binding_book = work_tag
    while binding_book and (binding_book.name not in possible_tags or check_binding_book_problematic_cases(binding_book)):
        binding_book = binding_book.previous_sibling
    if not binding_book:
        return None, None
    if not is_volume(binding_book):
        return binding_book, None
    volume = binding_book.text
    binding_book = binding_book.previous_sibling
    while binding_book and (binding_book.name not in possible_tags or check_binding_book_problematic_cases(binding_book) or is_volume(binding_book)):
        binding_book = binding_book.previous_sibling
    return binding_book, volume


def get_binding_book_and_more_information(author_response, work_id):
    author_html = BeautifulSoup(author_response.text, 'html.parser')
    # TODO make sure v02 is the only version
    all_prose = author_html.body.find('div', attrs={'class': 'by-card-v02', 'id': 'works-prose'})
    if not all_prose:
        return 'error', 'error', 'error', 'error'
    general_note = get_general_note(all_prose)
    work_tag = all_prose.find('a', attrs={'href': f'https://benyehuda.org/read/{work_id}'})
    if not work_tag:
        work_tag = all_prose.find('a', attrs={'href': f'/read/{work_id}'})
        if not work_tag:
            return 'error', 'error', 'error', 'error'
    work_tag = work_tag.parent
    if work_tag.name == 'h3':
        more_information = get_more_information(work_tag)
        return None, None, more_information, general_note
    elif work_tag.name == 'h4':
        # TODO - find a good way to find edition details
        binding_book, volume = get_binding_book_and_volume(work_tag, ['h3'])
        return clean_binding_book(binding_book), volume, get_more_information(binding_book), general_note
    elif work_tag.name == 'p' or work_tag.name == 'h5':
        binding_book, volume = get_binding_book_and_volume(work_tag, ['h3', 'h4'])
        return clean_binding_book(binding_book), volume, get_more_information(binding_book), general_note
    else:
        return 'error', 'error', 'error', 'error'


def clean_binding_book(binding_book):
    if not binding_book:
        return None
    name = binding_book.text
    if len(name) == 0 or name == "סיפורים" or name == "סיפורים בלתי-מקובצים":
        return None
    if name[-1] == ":":
        name = name[:-1]
    if name[0] in ["”", "“"] and name[-1] in ["”", "“"]:
        name = name[1:-1]
    if len(name) == 0:
        return None
    return name


def get_general_note(all_prose):
    content = all_prose.find('div', attrs={'class': 'by-card-content-v02'})
    for child in content.children:
        first_child = child
        break
    second_child = first_child.nextSibling
    maybe_second_child = all_prose.find('a', attrs={'class': 'g_anch', 'name': 'prose_g', 'id': 'prose_g'})
    if maybe_second_child and second_child == maybe_second_child.parent and "/read/" not in str(second_child):
        val = second_child.get_text(strip=True)
        if val:
            return val
    return None


def get_edition_details(work_details):
    for work_detail in work_details:
        if "פרטי מהדורת מקור:" in work_detail.text:
            return work_detail.text.replace("פרטי מהדורת מקור:", "").replace("מתוך:", "")
    return None


def get_more_information(work_tag):
    if not work_tag:
        return None
    next_sibiling = work_tag.nextSibling.nextSibling
    if next_sibiling is not None and next_sibiling.name == 'p' and "/read/" not in str(next_sibiling):
        return next_sibiling.text.replace("מתוך:", "")
    return None


def remove_binding_book_from_work_name(work_name, binding_book):
    if not work_name or not binding_book:
        return work_name
    for delimiter in [':', '-']:
        if work_name.startswith(f'{binding_book} {delimiter} '):
            return work_name.replace(f'{binding_book} {delimiter} ', "", 1)
        elif work_name.startswith(f'{binding_book}{delimiter} '):
            return work_name.replace(f'{binding_book}{delimiter} ', "", 1)
        elif work_name.startswith(f'{binding_book} {delimiter}'):
            return work_name.replace(f'{binding_book} {delimiter}', "", 1)
        elif work_name.startswith(f'{binding_book}{delimiter}'):
            return work_name.replace(f'{binding_book}{delimiter}', "", 1)
    return work_name


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
    author_link = author_link_prefix + author_id
    author_response = requests.get(author_link)
    if author_response.status_code != 200:
        return f"author_link did not work for {work_id}"
    print(author_response, work_id)
    binding_book, volume, more_information, general_note = get_binding_book_and_more_information(author_response, work_id)
    if binding_book == 'error':
        return f"couldnt find {work_id} in the authors page"
    type_of_work = "סיפור" if binding_book else "ספר"

    work_name = remove_binding_book_from_work_name(work_name, binding_book)

    work = Work(
        general_note=general_note,
        genre="פרוזה",
        author_id=int(author_id),
        work_id=work_id,
        work_name=work_name,
        edition_details=edition_details,
        binding_book=binding_book,
        volume=volume,
        edition_id="",
        more_information=more_information,
        type=type_of_work,
    )

    db.session.add(work)
    db.session.commit()

    return work

parse_ben_yehuda()

# author_link = author_link_prefix + '3'
# author_response = requests.get(author_link)
# x, y = get_binding_book_and_more_information(author_response, 100)
# print('binding book:')
# print(x)
# print('more information:')
# print(y)
