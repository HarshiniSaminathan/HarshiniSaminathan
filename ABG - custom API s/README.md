To run Flask at Environment
#Add this to .bashrc
export FLASK_CONFIG=development
export FLASK_ENV=development
export FLASK_APP=application.py
flask run

DATABASE :
pip install flask-migrate
#Create setup for migrations - Only once
flask db init
#To generate Migrations files
flask db migrate
#To apply changes
flask db upgrade || flask db upgrade 
#To unapply migrations
flask db downgrade || flask db downgrade 
###Syntax:

ORM :

Object to Dict
User._asdict()
User.query.get(1)._asdict()
User.query.first()._asdict()
result = User.query.all()
result = serialize_list(result)
User.query.order_by(User.username).all()
User.query.limit(1).all()
User.query.filter(User.email.endswith('@example.com')).all()
User.query.filter_by(username='missing').first()
result = User.objects(User.id, User.name).filter_by(phone_no=123).all()
--------------- (or) ------------------
db.session.query(User.id, User.name, User.phone_no, User.email).filter_by(phone_no=123)
result = query_list_to_dict(result)
---------------------------------------- Raw query select ----------------------------------------------------
raw_select(sql_query)
get_count(sql)
------------------------------------------- Sample ------------------------------------------------------------
for name in session.query(Tag.name).order_by(Tag.name):
print name

How many tags do we have?
session.query(Tag).count()

Get all images created yesterday:
session.query(Image) 
.filter(Image.created_at < datetime.utcnow().date()) 
.all()

Get all images, that belong to the tag 'car' or 'animal', using a subselect:
session.query(Image) 
.filter(Image.tags.any(Tag.name.in_(['car', 'animal']))) 
.all()

This can also be expressed with a join:
session.query(Image) 
.join(Tag, Image.tags) 
.filter(Tag.name.in_(['car', 'animal'])) 
.all()

Play around with functions:
from sqlalchemy.sql import func, desc
max_date = session.query(func.max(Image.created_at))
session.query(Image).filter(Image.created_at == max_date).first()

Get a list of tags with the number of images:
q = session.query(Tag, func.count(Tag.name)) 
.outerjoin(Image, Tag.images) 
.group_by(Tag.name) 
.order_by(desc(func.count(Tag.name))) 
.all()
for tag, count in q:
print 'Tag "%s" has %d images.' % (tag.name, count)

Get images created in the last two hours and zero likes so far:
session.query(Image) 
.join(Tag, Image.tags) 
.filter(Image.created_at > (datetime.utcnow() - timedelta(hours=2))) 
.filter(Image.likes == 0) 
.all()
----------------------------------- versioning using Blueprint -----------------------------------

By default /api/v1 will be appended in api url
from common.blueprint import Blueprint
user_api = Blueprint('user', name, url_postfix='user')
eg url: /api/v1/user
@user_api.route("/welcome", methods=['GET'], version=2)
If v2 then method name should be different than v1