from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

# mongo connection
clients = MongoClient('mongodb+srv://Badhani:sparta@cluster0.l2e4sqw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = clients.dbsparta

# flask connection
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bucket/done', methods = ['POST'])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': "Bucket List Completed.."})

@app.route('/bucket', methods=['POST'])
def bucket_post():
    bucket_reveive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1

    doc = {
        'num': num,
        'bucket': bucket_reveive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'Bucket List Added..'})

@app.route('/bucket', methods=['GET'])
def bucket_save():
    len_list = list(db.bucket.find({}, {'_id': False}))
    dbcount_reveive = db.bucket.count_documents({})
    # print(len_list)
    return jsonify({'msg':'List Updated', 'bkt_list': len_list, 'dbcount': dbcount_reveive})

@app.route('/delete', methods = ['POST'])
def delete_item():
    list_receive = request.form['list_give']
    print(list_receive)
    db.bucket.delete_one({'num': int(list_receive)})
    return jsonify({'msg': 'List Deleted..'})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000, debug=True)