import os
from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm import *
from sqlalchemy import *




project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "ardb.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
meta = MetaData()
meta.bind = db


marked_association = Table('marked_association', meta,
	Column('user_id', String, ForeignKey('User.ID')),
	Column('asset_id', String, ForeignKey('Asset.ID'))
)

placed_association = Table('placed_association', meta,
	Column('user_id', String, ForeignKey('User.ID')),
	Column('asset_id', String, ForeignKey('Asset.ID'))
)

class User(db.Model):
	__tablename__ = 'User'
	ID = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
	firstName = db.Column(db.String(10), nullable=False)
	lastName = db.Column(db.String(10), nullable=False)
	radiusSettings = db.Column(db.Integer)
	markedList = relationship("Asset", secondary=marked_association, back_populates="User")
	placedList = markedList = relationship("Asset", secondary=placed_association, back_populates="User")

	def __repr__(self):
		return "<User(firstName='%s', lastName='%s', ID='%s')>" % (self.firstName, self.lastName, self.ID)

class Asset(db.Model):
	__tablename__ = 'Asset'
	ID = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
	owner = db.Column(db.String(80), db.ForeignKey('User.ID'), nullable=False)
	link = db.Column(db.String(256))
	type = db.Column(Enum("image", "3d", "video"))
	markedBy = relationship("Mark", collection_class=attribute_mapped_collection("idMark"), backref="note")

class Mark(db.Model):
	__tablename__ = 'Mark'
	idMark = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
	user: db.Column(db.String(80), db.ForeignKey('User.ID'), nullable=False)
	note: Column(String(200))




#db.create_all()

@app.route('/user/create')
def createUser():
	newUser = User(ID='123', firstName='Jeimmi', lastName='Gomez',radiusSettings=1)
	db.session.add(newUser)
	db.create_all()
	db.session.commit()
	our_user = session.query(User).filter_by(firstName='Jeimmi').first()

#print(User.query.all()) 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



#DefaultUser = { 'ID':'1asf2sg3gdfg456g7f890', 
# 'Username':'xXChuckersXx420', 
# 'FirstName' : 'Chuck', 
# 'LastName' : 'Beans', 
# 'RaiusSettings':20, 
# 'PlacedList' : ['7ghf87gfgw7fg87g', 'frgd545y4g4gr','wegf34t45grthe4ewg','ew4gerethrh5rhh','wefgwe4egegsrgerg'],
# 'MarkedList':['sdfsgdbb54rsr6s5hbh45','b45w56nb5n6e5n','h5w6srnb56n5n','6he56hn5yjnd5j','56je5heserhs5rh5','e5hsrhrssrjs6jsr'] }

# DefaultAsset = {'ID':'sdkfuh78hfih8', 
# 'Owner':'1asf2sg3gdfg456g7f890', 
# 'Link':'iwh87a4gh8w7gh8g.dae', 
# 'MarkedBy':['sfgzsrgs54gser5h','5sehsrhrh','se5hsrhrthsr5h','w43gw3aw3awag','hr6jtd7kfy7kfkj','gergsregzw4g']}

# DefaultMark = {'ID':'d9a8dhfhsiufhis',
# 'UserID':'1asf2sg3gdfg456g7f890',
# 'Note':'xXCHUCKIEXx BBBOOIIIIIIIIII'}


