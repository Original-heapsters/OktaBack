from sqlalchemy import *

class DBManager:
    db = None
    marked_association = None
    placed_association = None
    meta = None
    def __init__(self, db=None):
        self.db = db
        self.meta = MetaData()
        self.meta.bind = self.db

        self.marked_association = Table('marked_association', self.meta,
            Column('user_id', String, ForeignKey('users.ID')),
            Column('asset_id', String, ForeignKey('assets.ID'))
        )

        self.placed_association = Table('placed_association', self.meta,
            Column('user_id', String, ForeignKey('users.ID')),
            Column('asset_id', String, ForeignKey('assets.ID'))
        )

    def createUser(self,id, radiusSettings, first=None, last = None,):
        newUser = User(id=id, radiusSettings=radiusSettings, firstName=first, lastName=last,)
        self.db.session.add(newUser)
        self.db.create_all()
        self.db.session.commit()
        self.db.session.query(Address).filter(Address.person == person).one()

        print(User.query.all())
        return "user created"
