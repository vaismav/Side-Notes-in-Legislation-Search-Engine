from flask import Flask
from main_search import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    words_list = [["הגדרות"], ["הגבלת פעילות מוסדות חינוך", "שעה"]]

    # find_words(5)
    x =find_words(words_list)
    return x


if __name__ == '__main__':
    app.run()
