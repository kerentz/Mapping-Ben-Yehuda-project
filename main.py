from flask import render_template
from DB import Work, app


@app.route('/')
def a():
    return render_template("layout.html")


@app.route('/get_table_data')
def get_table_data():
    all_works = Work.query.all()
    table_data = [[work.general_note,
                   work.genre,
                   work.author_id,
                   work.work_id,
                   work.work_name,
                   work.edition_details,
                   work.binding_book,
                   work.volume,
                   work.edition_id,
                   work.more_information,
                   work.type,
                   work.manually_changed
                   ] for work in all_works]
    return {'data': table_data}


if __name__ == '__main__':
    # When we want to create new DB need to use -> db.create_all()
    app.run('127.0.0.1', 5000)

