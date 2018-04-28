import os
from flask import Flask, json, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
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
#
# Asset:
#   ID: UUID
#   Owner: User.ID
#   Link: URL
#   Marked By: [MARK]
@app.route('/place', methods=['POST'])
def place():
    # userId
    # latlonstring
    # dae binary
    response = {}
    if request.method != 'POST':
        response['status'] = 404
        response['message'] = '/place only supports POST requests'
    userID = request.args


    return retResp

# @app.route('/hello/<hello>')
# def hello(hello = None):
#     """Endpoint returning a blank index file
#     ---
#      parameters:
#      - name: hello
#        in: path
#        type: string
#        required: false
#        default: World!
#        responses:
#         200:
#        description: A Hello World message
#
#     """
#
#     print(hello)
#     return ("Hello"+ hello)
#
# @app.route('/healthcheck')
# def healthcheck():
#     """Endpoint returning a blank index file
#     ---
#     responses:
#       200:
#        description: A healthcheck
#
#     """
#
#     return ("healthcheck")
#
# @app.route('/user/settings/<userid>')
# def userSettings(userid=None):
#     """
#         This is the endpoint to handle user settings configuration
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#     responses:
#       200:
#         description: User settings updated
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = " User settings updated for UserID :" + userid
#     response["userid"] = userid
#     responseJSON = jsonify(response)
#     return responseJSON
#
# @app.route('/search/<lat>/<lon>')
# def search(lat = None, lon = None):
#     """Endpoint returning a blank index file
#     ---
#     parameters:
#      - name: lat
#        in: path
#        type: string
#        required: true
#        default: None
#      - name: lon
#        in: path
#        type: string
#        required: true
#        default: None
#     responses:
#      200:
#        description: The latitude and longitude"
#
#     """
#     return ("search:"+ lat + "," + lon)
#
# @app.route('/place/lat/lon')
# def place():
#     """Endpoint returning a blank index file
#     """
#     return "place/lat/lon"
#
# @app.route('/collect/<userid>/<itemid>')
# def collect(userid=None, itemid=None):
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON
#
# @app.route('/user/<userID>')
# def getUser(userID = None):
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON
#
#
# @app.route('/asset/post')
# def postAsset():
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON
#
# @app.route('/asset/<assetID>')
# def getAsset(assetID=None):
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON
#
# @app.route('/collect/<userID>/<assetID>')
# def collectAsset(userID=None, assetID=None):
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON
#
# @app.route('/asset/nearby/<location>/<radius>')
# def getAssetsNearby(location='0.0,0.0', radius=10):
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON
#
#
#
# @app.route('/user/create')
# def createUser():
#     """
#         This is the endpoint to handle adding an item to a users collection
#     ---
#     parameters:
#       - in: path
#         name: userid
#         type: string
#       - in: path
#         name: itemid
#         type: string
#     responses:
#       200:
#         description: The task has been created
#     """
#     response = {}
#     response["status"] = 200
#     response["body"] = "UserID :" + userid + " ItemID : " + itemid
#     response["userid"] = userid
#     response["itemid"] = itemid
#     responseJSON = jsonify(response)
#     return responseJSON

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=True)
