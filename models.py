from flask import Flask
from db import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each order
    section1 = db.relationship('Section1', backref='order', lazy=True, cascade="all, delete")
    section2 = db.relationship('Section2', backref='order', lazy=True, cascade="all, delete")
    section3 = db.relationship('Section3', backref='order', lazy=True, cascade="all, delete")
    section4 = db.relationship('Section4', backref='order', lazy=True, cascade="all, delete")

class Section1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', name="section1Fkey" , ondelete="CASCADE"), nullable=False)
    filename = db.Column(db.String(300), nullable=True)
    filedata = db.Column(db.LargeBinary, nullable=True)  # Stores binary file data
    text_input = db.Column(db.String(500), nullable=True)

class Section2(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each tag
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', name="section2Fkey", ondelete="CASCADE"), nullable=False)
    class_selected = db.Column(db.String(300), nullable=False)
    tags = db.Column(db.String(300), nullable=False)

class Section3(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Foreign key
    order_id = db.Column(db.Integer, db.ForeignKey('order.id',  name="section3Fkey",  ondelete="CASCADE"), nullable=False)
    isBusiness = db.Column(db.Boolean, nullable=False)
    fullname = db.Column(db.String(200), nullable=True)
    businessname = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Section4(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Foreign key
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', name="section4Fkey",  ondelete="CASCADE"), nullable=False)
    hasPaid = db.Column(db.Boolean, nullable=False)

class Tags(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each tag
    category = db.Column(db.Integer, nullable=False)  
    tags = db.Column(db.String(300), nullable=False)  