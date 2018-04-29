import os
import uuid
from flask import Flask, json, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm import *
from sqlalchemy import *
from DBManager import DBManager


UPLOAD_FOLDER = './static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['dae', 'mp4', 'png', 'jpg', 'jpeg', 'mp3', 'mov','zip'])
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "ardb.db"))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['DEFAULT_RADIUS'] = 20
swagger = Swagger(app)
db = SQLAlchemy(app)
meta = MetaData()
meta.bind = db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    firstName = db.Column(db.String(10), nullable=False)
    lastName = db.Column(db.String(10), nullable=False)
    radiusSettings = db.Column(db.Integer)

    def serialized(self):
        return { 'id':self.id,
        'firstName':self.firstName,
        'lastName':self.lastName,
        'radiusSettings':self.radiusSettings
        }
    def __repr__(self):
        return "<User(firstName='%s', lastName='%s', id='%s')>" % (self.firstName, self.lastName, self.id)

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    owner = db.Column(db.String(80), db.ForeignKey('users.id'), nullable=False)
    link = db.Column(db.String(256))

    type = db.Column(Enum("image", "3d", "video","dae", "mp4", "png", "jpg", "jpeg", "mp3", "mov"))
    latlon = db.Column(db.String(256))

    def serialized(self):
        return {
        'id':self.id,
        'owner':self.owner,
        'link':self.link,
        'type':self.type,
        'latlon':self.latlon
        }


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    user= db.Column(db.String(80), db.ForeignKey('users.id'), nullable=False)
    asset = db.Column(db.String(80), db.ForeignKey('assets.id'),nullable=False)
    note= Column(String(200))

    def serialized(self):
        return {
        'id':self.id,
        'user':self.user,
        'note':self.note
        }

# DefaultUser = { 'id':'1asf2sg3gdfg456g7f890', 'username':'xXChuckersXx420', 'firstName' : 'Chuck', 'lastName' : 'Beans', 'radiusSettings':20, 'placedList' : ['7ghf87gfgw7fg87g', 'frgd545y4g4gr','wegf34t45grthe4ewg','ew4gerethrh5rhh','wefgwe4egegsrgerg'], 'markedList':['sdfsgdbb54rsr6s5hbh45','b45w56nb5n6e5n','h5w6srnb56n5n','6he56hn5yjnd5j','56je5heserhs5rh5','e5hsrhrssrjs6jsr'] }

# DefaultAsset = {'id':'sdkfuh78hfih8', 'owner':'1asf2sg3gdfg456g7f890', 'link':'iwh87a4gh8w7gh8g.dae', 'markedBy':['sfgzsrgs54gser5h','5sehsrhrh','se5hsrhrthsr5h','w43gw3aw3awag','hr6jtd7kfy7kfkj','gergsregzw4g']}

# DefaultMark = {'id':'d9a8dhfhsiufhis','userId':'1asf2sg3gdfg456g7f890','note':'xXCHUCKIEXx BBBOOIIIIIIIIII'}

# db.create_all()

# newUser = User(id='jeimmi123', firstName='jeimmi',lastName='gomez', radiusSettings=20)
# db.session.add(newUser)
# db.session.commit()

# newAsset = Asset(id='assetIDtest', owner=newUser.id, link='iwh87a4gh8w7gh8g.dae', type='dae',latlon='51.5033640,-0.1276250')
# db.session.add(newAsset)
# db.session.commit()

# newMark = Mark(id='d9a8dhfhsiufhis', user='jeimmi123',asset= 'assetIDtest', note="WORK")
# db.session.add(newMark)
# db.session.commit()

@app.route('/')
def index():
    """Endpoint returning a blank index file
    ---
    responses:
     200:
       description: The index of app
    """
    return ("index")

@app.route('/user', methods=['POST', 'GET'])
def user():
    """Endpoint to post a user object and create the entry if necessary
    ---
    responses:
     200:
       description: The index of app
    """
    response = {}
    response['status'] = ''
    response['message'] = ''

    if request.method == 'POST':
        userId = request.args.get('userId', None)
        username = request.args.get('username', None)
        firstName = request.args.get('firstName', None)
        lastName = request.args.get('lastName', None)
        radiusSettings = request.args.get('radius', None)

        if userId is None:
            response['status'] = 404
            response['message'] = 'userId was missing'
            retResp = jsonify(response)
            return retResp

        if username is None:
           response['status'] = 404
           response['message'] = 'username was missing'
           retResp = jsonify(response)
           return retResp
        if firstName is None:
           response['status'] = 404
           response['message'] = 'firstName was missing'
           retResp = jsonify(response)
           return retResp
        if lastName is None:
           response['status'] = 404
           response['message'] = 'lastName was missing'
           retResp = jsonify(response)
           return retResp
        if radiusSettings is None:
           radiusSettings = app.config['DEFAULT_RADIUS']
        print(username)
        print(radiusSettings)
        userObj = createUser(userId,radiusSettings,firstName,lastName)
        response['status'] = 200
        response['message'] = 'User successfully created'
        response['data'] = userObj.serialized()


    elif request.method == 'GET':
       userId = request.args.get('userId', '')
       if userId is None:
           response['status'] = 404
           response['message'] = 'userId was missing'
           retResp = jsonify(response)
           return retResp

       data = getUser(userId)

       response['status'] = 200
       response['message'] = 'User successfully fetched'
       response['data'] = data.serialized()

    else:
       response['status'] = 404
       response['message'] = 'Bro dafuq'

    retResp = jsonify(response)
    return retResp

@app.route('/place', methods=['POST'])
def place():
    response = {}
    if request.method != 'POST':
        response['status'] = 404
        response['message'] = '/place only supports POST requests'
        retResp = jsonify(response)
        return retResp


    userId = request.form.get('userId', None)
    lat = request.form.get('lat', None)
    lon = request.form.get('lon', None)
    assetType = request.form.get('assetType', None)
    if userId is None:
        response['status'] = 404
        response['message'] = 'userId missing'
        retResp = jsonify(response)
        return retResp

    if lat is None or lon is None:
        response['status'] = 404
        response['message'] = 'lat or lon missing'
        retResp = jsonify(response)
        return retResp

    latLongString = str(lat) + ',' + str(lon)

    if assetType is None:
        response['status'] = 404
        response['message'] = 'Asset type is missing'
        retResp = jsonify(response)
        return retResp
# check if the post request has the file part
    if 'asset' not in request.files:
        response['status'] = 404
        response['message'] = 'asset not in files'
        retResp = jsonify(response)
        return retResp
    else:
        file = request.files['asset']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            response['status'] = 404
            response['message'] = 'asset name was blank'
            retResp = jsonify(response)
            return retResp
        if file and allowed_file(file.filename):
            extension = file.filename.split('.')[1]
            assetId = uuid.uuid4().hex
            filename = assetId + '.' + extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    asset = filename
    assetLink = request.url_root + 'static/' + asset
    data = placeAsset(assetId,userId,assetLink,assetType,latLongString)
    data = {}
    data['assetId'] = assetId
    data['owner'] = userId
    data['link'] = assetLink
    data['type'] = assetType
    data['latLon'] = latLongString

    response['status'] = 200
    response['message'] = 'Successfully posted asset'
    response['data'] = data
    retResp = jsonify(response)
    return retResp

@app.route('/nearby/<radius>/<locationString>', methods=['GET'])
def nearby(radius=None, locationString=None):
    response = {}
    radiusInt = int(radius)
    lat = locationString.split(',')[0]
    lon = locationString.split(',')[1]
    data = [DefaultAsset, DefaultAsset, DefaultAsset] #DBMan.findNearby(radiusInt, lat, lon)
    response['status'] = 200
    response['message'] = 'Successfully fetched nearby assets'
    response['data'] = data
    retResp = jsonify(response)
    return retResp

@app.route('/found/<assetId>', methods=['GET'])
def found(assetId=None):
    response = {}
    if request.method != 'GET':
        response['status'] = 404
        response['message'] = '/found only supports POST requests'
        retResp = jsonify(response)
        return retResp

    data =found(assetId)
    data['markedList'] = [
    {'userId':'lilTay', 'note':'Ive been stacking bricks here for ages scrub'},{'userId':'bobbychuck', 'note':'Hackathons here are dah shnitzel'},{'userId':'TAYNE', 'note':'woah vicky is BAE, check out this CUBE BBBOOIIIIIIIIII'}
    ]
    response['status'] = 200
    response['message'] = 'Successfully fetched found asset'
    if data is not None:
        response['data'] = data.serialized()
        retResp = jsonify(response)
    return retResp



@app.route('/mark/<assetId>', methods=['POST'])
def mark(assetId=None):
    response = {}
    markId = uuid.uuid4().hex
    userId = request.args.get('userId', None)
    if userId is None:
        response['status'] = 404
        response['message'] = 'missing userId'
        retResp = jsonify(response)
        return retResp
    note = request.args.get('note', None)
    if note is None:
        note = ''
    data = mark(markId, userId, assetId, note)

    data = {}
    data['markId'] = markId
    data['userId'] = userId
    data['assetId'] = assetId
    data['note'] = note
    response['status'] = 200
    response['message'] = 'Successfully marked asset'
    response['data'] = data
    retResp = jsonify(response)
    return retResp

@app.route('/assets/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/usersmarks/<userId>', methods=['GET'])
def usersmarks(userId):
    response = {}
    if request.method != 'GET':
        response['status'] = 404
        response['message'] = '/usersmarks only supports POST requests'
        retResp = jsonify(response)
        return retResp

    data =usersAssets(userId)
    response['status'] = 200
    response['message'] = 'Successfully fetched found marked assets'
    if data is not None:
        response['data'] = data.serialized()
        retResp = jsonify(response)
    return retResp



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createUser(id, radiusSettings, first=None, last = None,):
    exists = User.query.filter_by(id=id).first()
    newUser = User(id=id, radiusSettings=radiusSettings, firstName=first, lastName=last)
    if not exists:
        db.session.add(newUser)
        db.session.commit()
        return newUser
    else:
        return newUser

def getUser(id):
    instance = db.session.query(User).filter_by(id=id).first()
    if instance:

        return instance

def placeAsset(assetId,userId,link,type,latLongString=None):
    exists = Asset.query.filter_by(id=assetId).first()
    newAsset = Asset(id=assetId, owner=userId, link=link, type=type)
    print(newAsset.owner)
    if not exists:
        db.session.add(newAsset)
        db.session.commit()
        print(newAsset.owner)
        return newAsset
    else:
        return newAsset

def found(id):
    instance = db.session.query(Asset).filter_by(id=id).first()
    if instance:
        return instance
    else:
        return instance

def usersAssets(userId):
    instance = db.session.query(Mark).limit(3)
    if instance:
        print(instance)
        return instance


def mark(markId, userId, assetId, note=None):
    exists = Mark.query.filter_by(id=markId).first()
    newMark = Mark(id=markId, user=userId, asset=assetId, note=note)
    if not exists:
        db.session.add(newMark)
        db.session.commit()
        return newMark
    else:
        return newMark

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=True)
