from peewee import *
import datetime
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash, check_password_hash

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('-joined_at',) # - means descending

	def get_posts(self):
		return Posts.select().where(Post.user == self)

	def get_stream(self):
		return Post.select().where(
			(Post.user == self)
		)

	@classmethod  # do this to create an instance of the class it belongs to
	def create_user(cls, username, email, password, admin=False):  # cls instead of self
		# if user gets, say, halfway created, to go back
		with DATABASE.transaction():
			try:
				cls.create(
					username=username,
					email=email,
					password=generate_password_hash(password),
					is_admin=admin)
			except IntegrityError:
				raise ValueError

class Post(Model):
	timestamp = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(
		rel_model=User,
		related_name='posts'
	)
	content = TextField()

	class Meta:
		database = DATABASE
		order_by = ('-timestamp',)

def initalize():
	DATABASE.connect()
	DATABASE.create_tables([User, Post], safe=True)
	DATABASE.close()
