from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
	name = db.StringField(max_length=36, required=True, primary_key=True)
	store_num = db.IntField()
	pw_hash = db.StringField(max_length=255, required=True)
	rxs = db.ListField(db.EmbeddedDocumentField('Rx'))

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def set_store_num(self, store_num):
		self.store_num = store_num

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.name

	def __repr__(self):
		return '<User %r>' % (self.name)

class Rx(db.EmbeddedDocument):
	rx_num = db.IntField(required=True)
	rx_name = db.StringField(max_length=255)

	def __repr__(self):
		return '<Rx %r>' % (self.rx_num)