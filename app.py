from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.vxurnmg.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.theTomorrowCamp

@app.route('/')
def home():
   return render_template('bsy.html')


## 등록하기
@app.route("/yun/guestbook", methods=["POST"])
def introduction_post():
    name_receive = request.form["name_give"]
    guestComment_receive = request.form["guestComment_give"]
    date_receive = request.form["date_give"]
    dateId_receive = request.form["dateId_give"]
    ## 추가기능 - num 받아오기
    guestbookList = list(db.bsy.find({}, {'_id': False}))
    count = len(guestbookList) + 1
    doc = {
        'name': name_receive,
        'comment': guestComment_receive,
        'date': date_receive,
        'num': count,
        'read': 0,
        'selfId': dateId_receive + str(count)
    }
    db.bsy.insert_one(doc)

    return jsonify({'msg':'😘'})


## 불러오기
@app.route("/yun/guestbook", methods=["GET"])
def introduction_get():
    guestComment_list = list(db.bsy.find({},{'_id':False}))
    return jsonify({'guestComments':guestComment_list})


## 삭제하기
@app.route("/yun/guestbook/remove", methods=["POST"])
def introduction_remove():
    selfId_receive = request.form["selfId_give"]
    db.bsy.delete_one({'selfId': selfId_receive})
    return jsonify({'msg': '삭제완료'})


## 추가기능 - 읽음 확인
@app.route("/yun/guestbook/read", methods=["POST"])
def introduction_read():
    selfId_receive = request.form["selfId_give"]
    db.bsy.update_one({'selfId': selfId_receive}, {'$set': {'read': 1}})
    return jsonify({'msg': '방명록 확인 ✅'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)