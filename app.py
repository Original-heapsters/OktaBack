import os
import uuid
from flask import Flask, json, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from flasgger import Swagger


UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['dae', 'mp4', 'png', 'jpg', 'jpeg', 'mp3', 'mov'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEFAULT_RADIUS'] = 20
swagger = Swagger(app)

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
        if radiusSettings is None:
           radiusSettings = app.config['DEFAULT_RADIUS']
        print(username)
        print(radiusSettings)
        data = DefaultUser
        data['id'] = userId
        data['userName'] = username
        data['radiusSettings'] = radiusSettings#DBMan.createUser(userId,username,radiusSettings)
        response['status'] = 200
        response['message'] = 'User successfully created'
        response['data'] = data


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

@app.route('/assets/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=True)
