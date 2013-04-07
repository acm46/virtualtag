import datetime
from flask import url_for
from runapp import db

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


