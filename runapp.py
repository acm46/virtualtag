from flask import Flask, request, url_for
from flask.ext.mongoengine import MongoEngine
from mongoengine import *
import os, datetime, json, math

app = Flask(__name__)
app.debug = True
# app.config["MONGODB_SETTINGS"] = {'DB':"virtual_tag"}
# app.config["SECRET_KEY"] = "hackathon2013"

connect('app14643328', username='animohan', password='hello123', host='alex.mongohq.com',port=10091)

# db = MongoEngine(app)

# import views, models

class Tag(Document):
	created_at = DateTimeField(default=datetime.datetime.now, required=True)
	modified_at = DateTimeField(default=datetime.datetime.now, required=True)
	qr_id = StringField(required=True)
	message = StringField(required=True)
	location_x = FloatField(required=True)
	location_y = FloatField(required=True)
	init_direction = FloatField(required=True)
	direction = FloatField(required=True)
	features = StringField()

	def to_hash(self):
		ret_hash = {
			"created_at":self.created_at.strftime('%Y-%m-%d-%H:%M:%S'),
			"modified_at":self.modified_at.strftime('%Y-%m-%d-%H:%M:%S'),
			"qr_id":self.qr_id,
			"message":self.message,
			"location_x":self.location_x,
			"location_y":self.location_y,
			"init_direction":self.init_direction,
			"direction":self.direction,
			"features":self.features
		}
		return ret_hash

	meta = {
		'indexes': ['-created_at'],
		'ordering': ['-created_at']
	}

@app.route('/task',methods=['GET','POST','DELETE'])
def task():
	if request.method == 'POST':
		tag = Tag()
		tag.qr_id = request.form.get('qr_id')
		tag.location_x = float(request.form.get('location_x'))
		tag.location_y = float(request.form.get('location_y'))
		tag.init_direction = float(request.form.get('init_direction'))
		tag.direction = float(request.form.get('direction'))
		tag.message = request.form.get('message')
		tag.features = request.form.get('features')
		tag.save()

		return json.dumps(tag.to_hash()), 200, {
		"Content-Type": "application/json"}
	elif request.method == 'DELETE':
		Tag.drop_collection()
		
		return json.dumps("All deleted"), 200, {
		"Content-Type": "application/json"}

	else:
		tags = Tag.objects.all()
		taghashes = [tag.to_hash() for tag in tags]

		return json.dumps(taghashes), 200, {
		"Content-Type": "application/json"}

@app.route('/intersect',methods=['POST'])
def intersect():
	if request.method == 'POST':
		ref_x1 = float(request.form.get('location_x'))
		ref_y1 = float(request.form.get('location_y'))
		theta1 = float(request.form.get('direction'))

		tag = Tag.objects.all()[0]
		cand_x1 =  tag.location_x
		cand_y1 = tag.location_y
		theta2 = tag.direction
		offset = tag.init_direction

		theta1 = (theta1 - offset)/360*2*math.pi
		theta2 = (theta2 - offset)/360*2*math.pi


		if (math.cos(theta1) > 0 and math.sin(theta1) > 0):
			ref_x2 = -30*math.cos(theta1) + ref_x1
			ref_y2 = -30*math.sin(theta1) + ref_y1
		elif (math.cos(theta1) < 0 and math.sin(theta1) < 0):		
			ref_x2 = -30*math.cos(theta1) + ref_x1
			ref_y2 = -30*math.sin(theta1) + ref_y1
		else:
			ref_x2 = 30*math.cos(theta1) + ref_x1
			ref_y2 = 30*math.sin(theta1) + ref_y1

		if (math.cos(theta2) > 0 and math.sin(theta2) > 0):
			cand_x2 = -30*math.cos(theta2) + cand_x1
			cand_y2 = -30*math.sin(theta2) + cand_y1
		elif (math.cos(theta2) < 0 and math.sin(theta2) < 0):		
			cand_x2 = -30*math.cos(theta2) + cand_x1
			cand_y2 = -30*math.sin(theta2) + cand_y1
		else:
			cand_x2 = 30*math.cos(theta2) + cand_x1
			cand_y2 = 30*math.sin(theta2) + cand_y1
		
		intersect_min = max(min(ref_x1,ref_x2),min(cand_x1,cand_x2))
		intersect_max = min(max(ref_x1,ref_x2),max(cand_x1,cand_x2))

		if(max(ref_x1,ref_x2) < max(cand_x1,cand_x2)):
			return json.dumps("false"), 200, {
			"Content-Type": "application/json"}

		Aref = (ref_y1-ref_y2)/(ref_x1-ref_x2)
		Acand = (cand_y1-cand_y2)/(cand_x1-cand_x2)
		bref = ref_y1-Aref*ref_x1
		bcand = cand_y1-Acand*cand_x1

		if(Aref==Acand):
			return json.dumps("false"), 200, {
			"Content-Type": "application/json"}

		Xa = (bcand-bref)/(Aref-Acand)

		if (Xa < intersect_min) or (Xa > intersect_max):
			return json.dumps("false"), 200, {
			"Content-Type": "application/json"}
		else:
			return json.dumps("true"), 200, {
			"Content-Type": "application/json"}

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)