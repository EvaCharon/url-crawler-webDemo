import spider
from flask import Flask, render_template, json, jsonify, request
import flask_restful

app = Flask(__name__)
api = flask_restful.Api(app)

display_url = {"masterURL": [], "childURL": []}
working_state = [{}]


# @app.route('/')
# def hello_word():
#     result = str(spider.scan_url_list({'https://www.canadapharmacy.com'}, 1))
#     return render_template('default.html', page_title='haha', result=result)


@app.route('/getMaster', methods=['get', 'post'])
def postMasterURL():
    master_set = spider.read('master_website.txt')
    master_url_list = []
    for i in iter(master_set):
        master_url_list.append(i)
    display_url["masterURL"] = master_url_list
    return jsonify(display_url)


@app.route('/scanAll', methods=['get', 'post'])
def scanAllURL():
    print("haha")
    _if_update_state = True
    if len(display_url["masterURL"]) == 0:
        working_state.clear()
        working_state.append({"text": "No Selected Master URL!"})
        return jsonify({"content": working_state})
    else:
        working_state.clear()
        cnt = 1
        for i in display_url["masterURL"]:
            working_state.append({"text": "Scanning "+i+" ("+str(cnt)+"/"+str(len(display_url["masterURL"]))+")"})
            working_state.append({"text": "Processing...Please Wait"})
            tmp = set()
            tmp.add(i)
            childURLs, states = spider.scan_url_list(tmp, 1)
            child_tmp = []
            for j in iter(childURLs):
                child_tmp.append(j)
            display_url["childURL"].append(child_tmp)
            for k in states:
                working_state.append({"text": k})
            cnt+=1;
        working_state.append({"text": "All Scanning Done"})
    return jsonify({"state": True})


@app.route('/updateState', methods=['get', 'post'])
def updateState():
    return jsonify({"content": working_state})


@app.route('/updateURL', methods=['get', 'post'])
def updateURL():
    print("haha1")
    return jsonify(display_url)

if __name__ == '__main__':
    app.run()
