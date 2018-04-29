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
ALLOWED_EXTENSIONS = set(['dae', 'mp4', 'png', 'jpg', 'jpeg', 'mp3', 'mov'])
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
    ID = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    firstName = db.Column(db.String(10), nullable=False)
    lastName = db.Column(db.String(10), nullable=False)
    radiusSettings = db.Column(db.Integer)

    def serialized(self):
        return { 'ID':self.ID,
        'firstName':self.firstName,
        'lastName':self.lastName,
        'radiusSettings':self.radiusSettings
        }
    def __repr__(self):
        return "<User(firstName='%s', lastName='%s', ID='%s')>" % (self.firstName, self.lastName, self.ID)

class Asset(db.Model):
    __tablename__ = 'assets'
    ID = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    owner = db.Column(db.String(80), db.ForeignKey('users.ID'), nullable=False)
    link = db.Column(db.String(256))
    type = db.Column(Enum("image", "3d", "video"))
    latlon = db.Column(db.String(256))

    def serialized(self):
        return {
        'ID':self.ID,
        'owner':self.owner,
        'link':self.link,
        'type':self.type,
        'latlon':self.latlon
        }


class Mark(db.Model):
    __tablename__ = 'marks'
    idMark = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    user: db.Column(db.String(80), db.ForeignKey('users.ID'), nullable=False)
    note: Column(String(200))

    def serialized(self):
        return {
        'idMark':self.idMark,
        'user':self.user,
        'note':self.note
        }

DefaultUser = { 'id':'1asf2sg3gdfg456g7f890', 'username':'xXChuckersXx420', 'firstName' : 'Chuck', 'lastName' : 'Beans', 'radiusSettings':20, 'placedList' : ['7ghf87gfgw7fg87g', 'frgd545y4g4gr','wegf34t45grthe4ewg','ew4gerethrh5rhh','wefgwe4egegsrgerg'], 'markedList':['sdfsgdbb54rsr6s5hbh45','b45w56nb5n6e5n','h5w6srnb56n5n','6he56hn5yjnd5j','56je5heserhs5rh5','e5hsrhrssrjs6jsr'] }

DefaultAsset = {'id':'sdkfuh78hfih8', 'owner':'1asf2sg3gdfg456g7f890', 'link':'iwh87a4gh8w7gh8g.dae', 'markedBy':['sfgzsrgs54gser5h','5sehsrhrh','se5hsrhrthsr5h','w43gw3aw3awag','hr6jtd7kfy7kfkj','gergsregzw4g']}

DefaultMark = {'id':'d9a8dhfhsiufhis','userId':'1asf2sg3gdfg456g7f890','note':'xXCHUCKIEXx BBBOOIIIIIIIIII'}

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
        print (userObj)
        response['status'] = 200
        response['message'] = 'User successfully created'
        response['data'] = userObj.serialized()


    elif request.method == 'GET':
       username = request.args.get('username', '')
       if username is None:
           response['status'] = 404
           response['message'] = 'username was missing'
           retResp = jsonify(response)
           return retResp
       data = DefaultUser#DBMan.GetUser(username)
       response['status'] = 200
       response['message'] = 'User successfully fetched'
       response['data'] = data

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

    userId = request.args.get('userId', None)
    if userId is None:
        response['status'] = 404
        response['message'] = 'userId missing'
        retResp = jsonify(response)
        return retResp
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)

    if lat is None or lon is None:
        response['status'] = 404
        response['message'] = 'lat or lon missing'
        retResp = jsonify(response)
        return retResp

    latLongString = str(lat) + ',' + str(lon)
    assetType = request.args.get('assetType', None)
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
    #data = DBMan.placeAsset(assetId,userId,assetLink,assetType,latLongString)
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
    data = DefaultAsset #DBMan.found(assetId)
    response['status'] = 200
    response['message'] = 'Successfully fetched found asset'
    response['data'] = data
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
    #DBMan.mark(markId, assetId, userId, note)
    data = {}
    data['markId'] = markId
    data['assetId'] = assetId
    data['userId'] = userId
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
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createUser(id, radiusSettings, first=None, last = None,):
    exists = User.query.filter_by(ID=id).first()
    newUser = User(ID=id, radiusSettings=radiusSettings, firstName=first, lastName=last)
    if not exists:
        db.session.add(newUser)
        db.session.commit()
        return newUser
    else:
        return newUser

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=True)
