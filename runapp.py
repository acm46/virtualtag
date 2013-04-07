from flask import Flask, request, url_for
from flask.ext.mongoengine import MongoEngine
import os, datetime, json

app = Flask(__name__)
app.debug = True
app.config["MONGODB_SETTINGS"] = {'DB':"virtual_tag"}
app.config["SECRET_KEY"] = "hackathon2013"

db = MongoEngine(app)

# import views, models

class Tag(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	modified_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	qr_id = db.StringField(required=True)
	message = db.StringField(required=True)
	location_x = db.FloatField(required=True)
	location_y = db.FloatField(required=True)
	direction = db.FloatField(required=True)

	def to_hash(self):
		ret_hash = {
			"created_at":self.created_at.strftime('%Y-%m-%d-%H:%M:%S'),
			"modified_at":self.modified_at.strftime('%Y-%m-%d-%H:%M:%S'),
			"qr_id":self.qr_id,
			"message":self.message,
			"location_x":self.location_x,
			"location_y":self.location_y,
			"direction":self.direction
		}
		return ret_hash

	meta = {
		'indexes': ['-created_at'],
		'ordering': ['-created_at']
	}

@app.route('/task', methods=['GET','POST'])
def task():
	if request.method == 'POST':
		tag = Tag()
		tag.qr_id = request.form.get('qr_id')
		tag.location_x = float(request.form.get('location_x'))
		tag.location_y = float(request.form.get('location_y'))
		tag.direction = float(request.form.get('direction'))
		tag.message = request.form.get('message')
		tag.save()

		return json.dumps(tag.to_hash()), 200, {
		"Content-Type": "application/json"}
	else:
		tags = Tag.objects.all()
		taghashes = [tag.to_hash() for tag in tags]

		return json.dumps(taghashes), 200, {
		"Content-Type": "application/json"}

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)