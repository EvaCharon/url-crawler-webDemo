import spider
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

#球哥后面加接口代码