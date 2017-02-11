# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Customer(db.Model):
    """
    Create a Customer table
    """

    __tablename__ =  "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    TIN = db.Column(db.String(11),unique = True)
    phone_number = db.Column(db.String(10))
    address = db.Column(db.String(200))

    def __repr__(self):
        return '<Customer: {}>'.format(self.name)

class Item(db.Model):
    """
    Create a Item table
    """

    __tablename__ =  "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    brand = db.Column(db.String(50))
    tax_type = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(10,2))
    
    def __repr__(self):
        return '<Item: {}>'.format(self.name)

class BillItem(db.Model):
    """
    Create a Bill Items table
    """

    __tablename__ =  "bill_items"

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer,db.ForeignKey('bills.id'))
    item_id = db.Column(db.Integer,db.ForeignKey('items.id'))
    item_price = db.Column(db.DECIMAL(10,2))
    quantity = db.Column(db.Integer)
    discount = db.Column(db.DECIMAL(10,2))
    total_price = db.Column(db.DECIMAL(10,2))
    
    def __repr__(self):
        return '<BillItem: {}>'.format(self.bill_id)
 
class Bill(db.Model):

    """
    Create a Bill table
    """

    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.Integer, unique=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'))
    customer_name = db.Column(db.String(60))
    customer_address = db.Column(db.String(200))
    date = db.Column(db.Date)
    bill_amount_1 = db.Column(db.DECIMAL(10,2))
    bill_amount_2 = db.Column(db.DECIMAL(10,2))
    tax_amount_1 = db.Column(db.DECIMAL(10,2))
    tax_amount_2 = db.Column(db.DECIMAL(10,2))
    total_bill = db.Column(db.DECIMAL(10,2))
    status = db.Column(db.Boolean,default=False)
    
    def __repr__(self):
        return '<Bill: {}>'.format(self.bill_number)