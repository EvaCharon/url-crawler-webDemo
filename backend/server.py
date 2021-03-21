import spider
from flask import Flask, render_template, json, jsonify, request
import flask_restful
import threading
import time

app = Flask(__name__)
api = flask_restful.Api(app)

display_url = {"masterURL": [], "childURL": []}
working_state = [{"text": "No task running."}]

_if_update_state = False
_if_update_URL = False


def run_select(indexList):
    print("haha2")
    working_state.clear()
    cnt = 1
    for i in indexList:
        working_state.append(
            {"text": "Scanning " + display_url["masterURL"][i] + " (" + str(cnt) + "/" + str(len(indexList)) + ")"})
        working_state.append({"text": "Processing...Please Wait"})
        tmp = set()
        tmp.add(display_url["masterURL"][i])
        childURLs, states = spider.scan_url_list(tmp, 1)
        child_tmp = []
        for j in iter(childURLs):
            child_tmp.append(j)
        display_url["childURL"][i] = child_tmp
        for k in states:
            working_state.append({"text": k})
        cnt += 1
        spider.output('output.txt', child_tmp)
    working_state.append({"text": "All Scanning Done"})
    time.sleep(1.5)
    global _if_update_state
    global _if_update_URL
    _if_update_state = False
    _if_update_URL = False


def run():
    print("haha")
    if len(display_url["masterURL"]) == 0:
        working_state.clear()
        working_state.append({"text": "No Selected Master URL!"})
        return jsonify({"content": working_state})
    else:
        working_state.clear()
        cnt = 1
        for i in display_url["masterURL"]:
            working_state.append(
                {"text": "Scanning " + i + " (" + str(cnt) + "/" + str(len(display_url["masterURL"])) + ")"})
            working_state.append({"text": "Processing...Please Wait"})
            tmp = set()
            tmp.add(i)
            childURLs, states = spider.scan_url_list(tmp, 1)
            child_tmp = []
            for j in iter(childURLs):
                child_tmp.append(j)
            display_url["childURL"][cnt-1] = child_tmp
            for k in states:
                working_state.append({"text": k})
            cnt += 1
            # add content to output.txt
            spider.output("output.txt", child_tmp)
        working_state.append({"text": "All Scanning Done"})
        time.sleep(1.5)
        global _if_update_state
        global _if_update_URL
        _if_update_state = False
        _if_update_URL = False


@app.route('/ifUpdate', methods=['get', 'post'])
def ifUpdate():
    return jsonify({"if_updateURL": _if_update_URL, "if_updateState": _if_update_state})


@app.route('/getMaster', methods=['get', 'post'])
def postMasterURL():
    global _if_update_URL
    master_set = spider.read('master_website.txt')
    master_url_list = []
    for i in iter(master_set):
        master_url_list.append(i)
        tmp = []
        display_url["childURL"].append(tmp)
    display_url["masterURL"] = master_url_list
    return jsonify(display_url)


@app.route('/getSelected', methods=['get', 'post'])
def getSelectedURL():
    data = request.get_json()
    urlList = data['index']
    print(str(type(urlList)))
    global _if_update_URL
    _if_update_URL = True
    global _if_update_state
    _if_update_state = True
    t = threading.Thread(target=run_select, args=(urlList,))
    t.start()
    return jsonify({"state": True})


@app.route('/scanAll', methods=['get', 'post'])
def scanAllURL():
    global _if_update_URL
    _if_update_URL = True
    global _if_update_state
    _if_update_state = True
    t = threading.Thread(target=run)
    t.start()
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
