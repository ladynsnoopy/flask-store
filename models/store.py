from db import db
class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #------------------------------------ lazy=dyanmic is look into items table only when you all json()
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all() ]}

    @classmethod
    def find_by_name(cls, name):
        
        return cls.query.filter_by(name=name).first()  # returns ItemModel object

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
  
    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # print(self.name)

        # query = "INSERT INTO items VALUES(?, ?)"
        # cursor.execute(query, (self.name, self.price))

        # connection.commit()
        # connection.close()

        #----- session is a collection of objects to write----
        db.session.add(self)
        db.session.commit()