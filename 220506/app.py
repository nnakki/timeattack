from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.test


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detail/<idx>')
def detail(idx):
    # todo
    return


@app.route('/articleList', methods=['GET'])
def get_article_list():
    article_list = list(db.articles.find({}, {'_id': False}))
    for article in article_list:
        article['reg_date'] = article['reg_date'].strftime('%Y.%m.%d %H:%M:%S')

    return jsonify({"article_list": article_list})


# Create
@app.route('/article', methods=['POST'])
def create_article():
    title = request.form['title']
    content = request.form['content']
    pw = request.form['pw']
    col = db.articles

    doc = {
        'idx': col.estimated_document_count()+1,
        'title': title,
        'content': content,
        'pw': pw,
        'reg_date': datetime.now()
    }
    db.articles.insert_one(doc)
    return {"result": "success"}


# Read
@app.route('/article', methods=['GET'])
def read_article():
    idx = request.args.get("idx")
    article = db.articles.find_one({'idx': int(idx)})
    return jsonify({"article": article})


# Update
@app.route('/article', methods=['PUT'])
def update_article():
    idx = request.args.get("idx")
    article = db.articles.update()
    return {"result": "success"}


# Delete
@app.route('/article', methods=['DELETE'])
def delete_article():
    idx = request.args.get('idx')
    db.test.delete_one({'idx': int(idx)})
    return {"result": "success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
