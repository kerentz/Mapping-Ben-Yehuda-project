# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, request, render_template
from DB import db, Students
app = Flask("KEREN")


@app.route('/')
def a():
    return render_template("layout.html")


@app.route('/parse_url', methods=['POST'])
def parse_url():
    return f'Parsing {request.form.get("url")}, please wait....'

#
# @app.route('/register', methods=['GET', 'POST'])
# def aaa():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     DB.register(email, password)
#     return "abc"
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def bbb():
#     ans = DB.login(request.form.get('email'), request.form.get('password'))
#     return ans


if __name__ == '__main__':
    db.create_all()
    app.run('127.0.0.1', 5000)



# curl --data "email=keren" --data "password=hhh" http://127.0.0.1:5000/register
