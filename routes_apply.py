from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import Section1, Section2, Section3, Section4, Tags, Order
from dotenv import load_dotenv
from sqlalchemy import func
from db import db
import stripe
import base64
import json
import os
from werkzeug.utils import secure_filename
import requests

apply = Blueprint('apply', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@apply.route('/create-order', methods=['POST'])
def create_order():
    # Create a new order in the database
    new_order = Order()
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'order_id': new_order.id}), 201  # Return the order ID as JSON response


@apply.route('/add-trademark', methods=['GET', 'POST'])
def add_trademark_section_1():
    if request.method == 'GET':
        return render_template('add-trademark.html')


    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file = request.files.get('file')

        if file and text_input:
            flash('Please upload either an image or enter text, not both!', 'danger')
            return redirect(url_for('apply.add_trademark_section_1'))
        
        # create order
        response = requests.post(YOUR_DOMAIN + '/create-order')
        if response.status_code == 201:
            data = response.json()
            order_id = data['order_id']
            session['order_id'] = order_id  # Store order ID in session
        else:
            return "Error creating order", 500
            
        if order_id != None:
            print("Order created successfully with ID:", order_id)
        
            if file and allowed_file(file.filename) and file != None:
                filename = secure_filename(file.filename)
                filedata = file.read()  # Read file as binary
                
                # Store in database
                new_file = Section1(order_id=order_id, filename=filename, filedata=filedata, text_input=None)
                db.session.add(new_file)
                db.session.commit()

                flash('File successfully uploaded and stored in the database!', 'success')
                return redirect(url_for('apply.add_trademark_section_2'))

            elif text_input and  text_input != None:
                new_entry = Section1(order_id=order_id, filename=None, filedata=None, text_input=text_input)
                db.session.add(new_entry)
                db.session.commit()

                flash('Text successfully submitted!', 'success')
                return redirect(url_for('apply.add_trademark_section_2'))

            else:
                flash('Please upload a valid image or enter text!', 'danger')
        else:
            return "Error creating order", 500  # Internal Server Error
    


@apply.route('/search-tags')
def search_tags():
    query = request.args.get('q', '')  # Get user input from request
    if query:
        results = Tags.query.with_entities(Tags.tags, Tags.category).filter(Tags.tags.ilike(f"%{query}%")).limit(5).all()
        return jsonify([{"tag": tag, "category": category} for tag, category in results])
    return jsonify([])  # Return empty list if no input





@apply.route('/add-trademark-2', methods=['GET', 'POST'])
def add_trademark_section_2():
    if request.method == 'GET':
        return render_template('add-trademark-2.html')
    
    if request.method == 'POST':
        tags_json = request.form.get('tags')
        
        if not tags_json:
            return "Error: No tags received", 400  # Return error if empty

        try:
            tags = json.loads(tags_json)  # Convert JSON string to Python dictionary

        except json.JSONDecodeError:
            return "Error: Invalid JSON format", 400

        # Iterate through the dictionary: key = category, value = list of tags
        for category_current, tag_list in tags.items():
            for tag_current in tag_list:
                new_tag = Section2(
                    order_id=session['order_id'],  
                    class_selected=category_current,  # Use correct column name
                    tags=tag_current
                )
                db.session.add(new_tag)

        db.session.commit()  # Commit all changes once, not in every loop iteration
        flash('tags added successfully in the database!', 'success')

        return redirect(url_for('apply.add_trademark_section_3'))

    




@apply.route('/add-trademark-3', methods=['GET', 'POST'])
def add_trademark_section_3():
    if request.method == 'GET':
        return render_template('add-trademark-3.html')
    
    if request.method == 'POST':
        # get input from the form
        order_id=session['order_id']
        isBusiness = 1 if request.form.get('isBusiness') == "true" else 0
        fullName = request.form.get('fullName')
        businessName = request.form.get('businessName')
        address = request.form.get('address')
        country = request.form.get('country')
        email = request.form.get('email')
        phone = request.form.get('phone')

        session['address'] = address
        session['country'] = country
        session['email'] = email
        session['phone'] = phone

        new_info = Section3(order_id=order_id, isBusiness=isBusiness, fullname=fullName, businessname=businessName, address=address, country=country, email=email, phone=phone)
        db.session.add(new_info)
        db.session.commit()
        flash('successfully completed section 3', 'success')
        return redirect(url_for('apply.add_trademark_section_4'))
   

@apply.route('/add-trademark-4')
def add_trademark_section_4():
    return render_template('add-trademark-4.html')


@apply.route('/success')
def success():
    return render_template('success.html')


@apply.route('/cancel')
def cancel():
    return render_template('cancel.html')


load_dotenv()
YOUR_DOMAIN = 'http://localhost:4242'
BASE_COST = 200
CATEGORY_COST = 50
PRODUCTS_PRICEID = {## price id for each product
    'base': "price_1R7JthBtR3owG6M6bDRqy0Jp",
    '1':  "price_1R7JtyBtR3owG6M6q4QkNpMX",
    '2': "price_1R7JuDBtR3owG6M65e7PS9Lo",
}



endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@apply.route('/get-section-1', methods=['GET'])
def get_section_1():
    # Check if 'order_id' exists in the session
    if 'order_id' not in session:
        return jsonify({'error': 'order_id not found in session'}), 400  # Bad Request

    order_id = session['order_id']

    # Query the database for the specific record
    data = Section1.query.filter_by(id=order_id).first()

    if data:
        # Encode the BLOB as a Base64 string
        if data.filedata is not None:
            file_data_base64 = base64.b64encode(data.filedata).decode('utf-8')

            # Return the data as JSON
            return jsonify({
                'file-name': data.filename,
                'file-data': file_data_base64,
                'text': data.text_input
            })

        else:
            # Return the text data as JSON
            return jsonify({
                'file-name': None,
                'file-data': None,
                'text': data.text_input
            })
    
    else:
        # Return an error if no data is found
        return jsonify({'error': 'No data found'}), 404  # Not Found
    

@apply.route('/get-section-2', methods=['GET'])
def get_section_2():
    if 'order_id' not in session:
        return jsonify({'error': 'order_id not found in session'}), 400  # Bad Request  
    
    order_id = session['order_id']
    data = Section2.query.filter_by(order_id=order_id).all()
    if data:
        return jsonify([{
            'class_selected': item.class_selected,
            'tags': item.tags
        } for item in data])
    else:
        return jsonify({'error': 'No data found'}), 404
    


@apply.route('/get-section-3', methods=['GET'])
def get_section_3():
    if 'order_id' not in session:
        return jsonify({'error': 'order_id not found in session'}), 400  # Bad Request

    order_id = session['order_id']
    data = Section3.query.filter_by(order_id=order_id).first()
    if data:
        return jsonify({
            'isBusiness': bool(data.isBusiness),
            'fullname': data.fullname,
            'businessname': data.businessname,
            'address': data.address,
            'country': data.country,
            'email': data.email,
            'phone': data.phone
        })
    else:
        return jsonify({'error': 'No data found'}), 404


@apply.route('/get-price', methods=['GET'])
def get_price():
    if 'order_id' not in session:
        return jsonify({'error': 'order_id not found in session'}), 400  # Bad Request  
    
    order_id = session['order_id']

    num_categories = Section2.query.with_entities(func.count(func.distinct(Section2.class_selected))).filter_by(order_id=order_id).scalar()
    total_cost = BASE_COST + (num_categories * CATEGORY_COST)
    return jsonify({'price': total_cost})


@apply.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # Call get_section_2() and parse its response
    response = get_section_2()
    
    if response.status_code != 200:  # Check if data retrieval was successful
        return response  

    class_selected = json.loads(response.get_data(as_text=True))  # Parse JSON response

    if not isinstance(class_selected, list):  # Ensure data is a list
        return jsonify({'error': 'Invalid data format'}), 400

    categories = set()  # Use a set to store unique categories
    print(categories)

    for item in class_selected:
        key = item.get('class_selected')  # Get class_selected from each item
        if key:
            categories.add(key)

    line_items = [
        {
            'price': PRODUCTS_PRICEID['base'],
            'quantity': 1,
        }
    ]

    for category in categories:
        if category in PRODUCTS_PRICEID:  # Ensure the category exists in the price dictionary
            line_items.append({
                'price': PRODUCTS_PRICEID[category],
                'quantity': 1,
            })

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=session['email'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
            metadata={'order_id': session['order_id'],
                      'address': session['address'],
                      'country': session['country'],
                      'phone': session['phone']}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return proper JSON error response

    return redirect(checkout_session.url, code=303)

def update_order(order_id):
    print("Updating order with ID:", order_id) 
    order = Section4(order_id=order_id, hasPaid=True)
    db.session.add(order)
    db.session.commit()
    print('Order updated successfully')
    session.clear()


@apply.route('/webhook', methods=['POST'])
def webhook():
    print("entered webhook")
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f'⚠️  Webhook error while parsing basic request: {e}')
        return jsonify({'status': 'invalid payload'}), 400
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f'⚠️  Webhook signature verification failed: {e}')
        return jsonify({'status': 'invalid signature'}), 400

    # Handle the event
    if  event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("checkout.session.completed event received")
        order_id = session.get('metadata', {}).get('order_id')

        if not order_id:
            print("⚠️  No order_id found in checkout session metadata.")
            return jsonify({'status': 'no order id'}), 400  
              
        # Update the order
        else:
            update_order(order_id)
            print("Order updated successfully.")
            return jsonify({'status': 'success'}), 200

    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return jsonify({'status': 'success'}), 200