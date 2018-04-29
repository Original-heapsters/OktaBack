from os import system
from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sys import model.py

class DBManager(object):
	def __init__(self):
		project_dir = os.path.dirname(os.path.abspath(__file__))
		database_file = "sqlite:///{}".format(os.path.join(project_dir, "ardb.db"))


	def createUser(id, radiusSettings, first=None, last = None,):

	    newUser = User(id=id, radiusSettings=radiusSettings, firstName=first, lastName=last,)
	    db.session.add(newUser)
	    db.create_all()
	    db.session.commit()
	    session.query(Address).filter(Address.person == person).one()

	    print(User.query.all())    
	    return "user created"





if __name__ == "__main__":
	temp = DBManager()
	tmp.createUser("1234",1,"jeimmi","gomez")

    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port, debug=False)
    