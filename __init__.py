from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"virtual_tag"}
app.config["SECRET_KEY"] = "hackathon2013"

db = MongoEngine(app)

import views, models

if __name__ == '__main__':
	app.run(debug=True)