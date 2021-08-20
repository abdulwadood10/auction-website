from src import db,login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    contact = db.Column(db.String(20),nullable=False)
    address = db.Column(db.Text,nullable=False)
    bid_price = db.relationship('Bid',backref='user',lazy=True)

    @staticmethod
    def get_emails():
        return [x for x, in db.session.query(User.email)]


    def __repr__(self):
        return f"User('{self.username}','{self.email}',{self.bid_price})"


class Bid(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    bid_price = db.Column(db.Integer,nullable=False)
    bid_status = db.Column(db.Boolean,default=True)
    bid_date = db.Column(db.DateTime,default=datetime.utcnow)
    user_name = db.Column(db.String,db.ForeignKey('user.username'),nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),nullable=False)

    def __repr__(self):
        return f"Bid('{self.bid_date}','{self.bid_price}','{self.bid_status}','{self.item_id}','{self.user_name}')"



class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.Text,nullable=False)
    name = db.Column(db.String(60),nullable=False)
    bid_price = db.relationship('Bid',backref='item',lazy=True)
    starting_bid = db.Column(db.Integer,nullable=False)
    category = db.Column(db.String(60),nullable=False)
    item_image = db.Column(db.String(30),nullable=False,default='default.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Boolean,default=True)

    def __repr__(self):
        return f"Item({self.id},'{self.name}','{self.category}','{self.starting_bid}','{self.bid_price}')"




class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False,default=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'),nullable=False)

    def __repr__(self):
        return f"WatchList(''{self.id},'{self.status}')"




