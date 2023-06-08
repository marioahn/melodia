from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.gdqs5qt.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
	return render_template('index.html')

# 크롤링해서 가져올 것: 발매일, 장르
@app.route("/melodia", methods=["POST"])
def melodia_post():
    url_receive = request.form['url_give'] # = img_receive = request.form['img_receive']
    # title_receive = request.form['title_receive']
    # artist_receive = request.form['artist_receive']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers) # url을 위에서 만든 url_receive 변수로 교체
    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content'] # title+artist
    ogimage = soup.select_one('meta[property="og:image"]')['content']

    doc = {
	    'title': ogtitle,
	    'image': ogimage,
        'url': url_receive,
	    'comment': comment_receive,
        'star': star_receive # 일단 5개로 받고 처리
    }
    db.melodia.insert_one(doc) 

    return jsonify({'msg':'노래 추천 완료!'})

# API.2
@app.route("/melodia", methods=["GET"])
def melodia_get():

    all_melodias = list(db.melodia.find({},{'_id':False}))
    return jsonify({'result':all_melodias}) 

if __name__ == '__main__':
	app.run('0.0.0.0', port=5000, debug=True)