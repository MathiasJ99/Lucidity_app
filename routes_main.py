from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import db
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)


##Main page routes
@main.route('/')
def home():
    return render_template('index.html')

@main.route('/our-process')
def our_process():
    return render_template('our-process.html')

@main.route('/why-trademark')
def why_trademark():
    return render_template('why-trademark.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')





