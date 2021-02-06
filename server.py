from flask import (Flask, request, send_from_directory)
import os
from searchQuery import SearchQuery
from flask_cors import CORS

app = Flask(__name__, static_folder='client/build')

CORS(app)


searchObj = SearchQuery()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/searchOption')
def searchOption():
    query = request.args.get("qu", "")
    # print("text")
    # print(query)
    response = {}
    response['data'] = searchObj.getSugestedSideNote(query, 50)
    return response
    

@app.route('/api/search')
def search():
    query = request.args.get("qu", "")
    print(query)
    response = {}
    response['data'] = searchObj.makeQueryResult(query)
    return response

if __name__ == "__main__":
    app.run(debug=True)

    # ק"ת תש"ס, ק"ת תשס"ו־2, ק"ת תש"ע, ק"ת תשע"א־3, ק"ת תשע"ג, ק"ת תשע"ד