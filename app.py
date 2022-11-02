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


## 등록
@app.route("/yun/guestbook", methods=["POST"])
def introduction_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]
    date_receive = request.form["date_give"]
    ## 추가
    guestbookList = list(db.bsy.find({}, {'_id': False}))
    count = len(guestbookList) + 1
    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'date': date_receive,
        'num': count,
        'read': 0
    }
    db.bsy.insert_one(doc)

    return jsonify({'msg':'😘'})


## 불러오기
@app.route("/yun/guestbook", methods=["GET"])
def introduction_get():
    comment_list = list(db.bsy.find({},{'_id':False}))
    return jsonify({'comments':comment_list})



## 삭제하기1
@app.route("/yun/guestbook", methods=["POST"])
def introduction_delete():
    id_receive = request.form["id_give"]
    doc = { 'id': id_receive }

    db.bsy.delete_one(doc)

    return jsonify({'msg': '삭제 완료 ✅'})    


## 삭제하기2
@app.route("/yun/guestbook/remove", methods=["POST"])
def introduction_remove():
    id_receive = request.form["id_give"]
    doc = { '_id': id_receive }

    db.bsy.insert_one(doc)

    return jsonify({'msg':'연결확인'})



## 읽음 확인
@app.route("/yun/guestbook/read", methods=["POST"])
def introduction_read():
    num_receive = request.form["num_give"]
    db.bsy.update_one({'num': int(num_receive)}, {'$set': {'read': 1}})
    return jsonify({'msg': '방명록 확인 ✅'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)