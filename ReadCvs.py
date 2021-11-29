import csv

csv_data = {}


def create_data_dictionary_from_csv():
    with open('pseudocatalogue.csv', mode='r', encoding="UTF-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data[row["ID"]] = {'path': row["path"], 'title': row["title"], 'authors': row["authors"],
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
