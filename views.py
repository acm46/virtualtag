from flask import request
from flask.ext.mongoengine import MongoEngine
from models import Tag
from runapp import app
import json

@app.route('/task', methods=['GET','POST'])
def task():
	if request.method == 'POST':
		tag = Tag()
		tag.qr_id = request.form.get('qr_id')
		tag.location_x = float(request.form.get('location_x'))
		tag.location_y = float(request.form.get('location_y'))
		tag.direction = float(request.form.get('direction'))
		tag.message = request.form.get('message')
		tag.features = request.form.get('features')
		tag.save()

		return json.dumps(tag.to_hash()), 200, {
		"Content-Type": "application/json"}
	else:
		tags = Tag.objects.all()
		taghashes = [tag.to_hash() for tag in tags]

		return json.dumps(taghashes), 200, {
		"Content-Type": "application/json"}

@app.route('/intersect',methods=['POST'])
def intersect():
	if request.methods == 'POST':
		x1 = float(request.form.get('location_x'))
		y1 = float(request.form.get('location_y'))
		theta1 = float(request.form.get('direction'))
		


		tag = Tag.objects.all()[0]
		x2 =  tag.location_x
		y2 = tag.location_y
		theta2 = tag.direction








