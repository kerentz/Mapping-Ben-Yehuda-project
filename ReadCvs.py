import csv
import requests
from bs4 import BeautifulSoup

csv_data = {}


def create_data_dictionary_from_csv():
    with open('pseudocatalogue.csv', mode='r', encoding="UTF-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if 'פרוזה' == row["genre"] or '' == row["genre"]:
                author_id = row["path"][1:].split("/")[0][1:]
                csv_data[row["ID"]] = {'authorId': author_id, 'path': row["path"], 'title': row["title"],
                                       'authors': row["authors"],
                                       'translators': row["translators"], 'original_language': row["original_language"],
                                       'genre': row["genre"], 'source_edition': row["source_edition"]}


def get_csv_data_one(book_id):
    try:
        return csv_data[book_id]
    except KeyError:
        return "No data for this key"


def get_csv_data_two(book_id, field):
    try:
        return csv_data[book_id][field]
    except KeyError:
        return "No data for those keys"


def write_csv_data(book_id, field, data): csv_data[book_id][field] = data


def enter_csv_to_db():
    web_link_prefix = "https://benyehuda.org/read/"
    for book_id in csv_data:
        web_link = web_link_prefix + book_id
        html = requests.get(web_link)
        parsed_html = BeautifulSoup(html.text, 'html.parser')
        work_details = parsed_html.body.find_all('div', attrs={'class': 'work-details'})
        for work_detail in work_details:
            if "פרוזה" in work_detail.text:
                enter_short_story_to_db(book_id)
                break


def enter_short_story_to_db(book_id):
    return book_id
