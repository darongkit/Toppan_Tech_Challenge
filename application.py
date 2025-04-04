from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/University'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MySQL Table
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                   
    name = db.Column(db.String(100), nullable=False)                   
    country = db.Column(db.String(50), nullable=False)                    
    webpages = db.Column(db.String(100), nullable=True)                  
    isBookmarked = db.Column(db.Boolean, default=False)                   
    created = db.Column(db.DateTime, default=datetime.datetime.now)      
    lastModified = db.Column(db.DateTime, default=datetime.datetime.now)                
    isActive = db.Column(db.Boolean, default=True)                       
    deletedAt = db.Column(db.DateTime, nullable=True, default=None)    

with app.app_context():
    db.create_all()    

# API Methods
@app.route('/') # default
def index():
    return "Database connected successfully!"

# --------------- Challenge 1 ---------------
@app.route('/universities', methods=['GET']) # GET list of all unis
def get_unis():

    # Challenge 2: Filter
    id_filter = request.args.get("id")
    name_filter = request.args.get("name")
    country_filter = request.args.get("country")
    webpages_filter = request.args.get("webpages")
    isBookmarked_filter = request.args.get("isBookmarked")
    created_filter = request.args.get("created")
    lastModified_filter = request.args.get("lastModified")
    isActive_filter = request.args.get("isActive")
    deletedAt_filter = request.args.get("deletedAt")
    
    uni_query = University.query

    if id_filter:
        uni_query = uni_query.filter(University.id == id_filter)
        
    if name_filter:
        uni_query = uni_query.filter(University.name.ilike(f"%{name_filter}%"))

    if country_filter:
        uni_query = uni_query.filter(University.country.ilike(f"%{country_filter}%"))
        
    if webpages_filter:
        uni_query = uni_query.filter(University.webpages.ilike(f"%{webpages_filter}%"))

    if isBookmarked_filter:
        isBookmarked_val = isBookmarked_filter.lower() in ['true', '1']
        uni_query = uni_query.filter(University.isBookmarked == isBookmarked_val)

    if created_filter:
        created_date = datetime.datetime.strptime(created_filter, "%Y-%m-%d")    # yyyy-mm-dd
        uni_query = uni_query.filter(University.created >= created_date)

    if lastModified_filter:
        lastModified_dates = datetime.datetime.strptime(lastModified_filter, "%Y-%m-%d")    # yyyy-mm-dd
        uni_query = uni_query.filter(University.lastModified >= lastModified_dates)

    if isActive_filter:
        isActive_val = isActive_filter.lower() in ['true', '1']
        uni_query = uni_query.filter(University.isActive == isActive_val)

    if deletedAt_filter:
        deletedAt_dates = datetime.datetime.strptime(deletedAt_filter, "%Y-%m-%d")    # yyyy-mm-dd
        uni_query = uni_query.filter(University.deletedAt >= deletedAt_dates)

    # Challenge 2: Paginate
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # query bookmarked uni
    bookmark_query = University.query.filter(University.isBookmarked == True)
    bookmark_paginate = bookmark_query.paginate(page=page, per_page=per_page, error_out=False)
    bookmark_unis = bookmark_paginate.items

    uni_bookmarked = []
    for uni in bookmark_unis:
        uni_data = {
            "id": uni.id,
            "name": uni.name,
            "country": uni.country,
            "webpages": uni.webpages,
            "isBookmarked": uni.isBookmarked,
            "created": uni.created,
            "lastModified": uni.lastModified,
            "isActive": uni.isActive,
            "deletedAt": uni.deletedAt
        }
        uni_bookmarked.append(uni_data)


    # query all uni
    unis_query = uni_query.paginate(page=page, per_page=per_page, error_out=False)
    unis = unis_query.items
    
    uni_list = []
    for uni in unis:
        uni_data = {
            "id": uni.id,
            "name": uni.name,
            "country": uni.country,
            "webpages": uni.webpages,
            "isBookmarked": uni.isBookmarked,
            "created": uni.created,
            "lastModified": uni.lastModified,
            "isActive": uni.isActive,
            "deletedAt": uni.deletedAt
        }
        uni_list.append(uni_data)

    # meta = {
    #     "bookmarked_unis" : {
    #         "meta" : {
    #             "page" : bookmark_paginate.page,
    #             "pages" : bookmark_paginate.pages,
    #             "next_page" : bookmark_paginate.next_num,
    #             "prev_page" : bookmark_paginate.prev_num
    #             },
    #         "bookmarked_data" : uni_bookmarked
    #         },
    #         "unis" : {
    #         "meta" : {
    #             "page" : unis_query.page,
    #             "pages" : unis_query.pages,
    #             "next_page" : unis_query.next_num,
    #             "prev_page" : unis_query.prev_num
    #             },
    #         "bookmarked_data" : uni_list
    #         }
    # }

    # return jsonify(uni_bookmarked, uni_list)    # return Bookmarked Uni and all unis
    # return jsonify(uni_bookmarked, uni_list, meta)
    return jsonify({
        "bookmarked_unis" : {
            "meta" : {
                "page" : bookmark_paginate.page,
                "pages" : bookmark_paginate.pages,
                "next_page" : bookmark_paginate.next_num,
                "prev_page" : bookmark_paginate.prev_num
                },
            "bookmarked_data" : uni_bookmarked
        },
        
        "unis" : {
            "meta" : {
                "page" : unis_query.page,
                "pages" : unis_query.pages,
                "next_page" : unis_query.next_num,
                "prev_page" : unis_query.prev_num
                },
            "unis_data" : uni_list
        }
    })

@app.route('/universities', methods=['POST'])    # Add new univeristy
def add_uni():
    data = request.get_json()

    if not data or not all(key in data for key in ['name', 'country', 'webpages']):
        return jsonify({'message': 'Missing Required Fields'}), 400
     
    uni = University(name = data['name'],
                    country = data['country'],
                    webpages = data['webpages'],
                    isBookmarked = data.get('isBookmarked', False),
                    created = datetime.datetime.now(),
                    lastModified = datetime.datetime.now(),
                    isActive = data.get('isActive', True),
                    deletedAt = None
    )
    db.session.add(uni)
    db.session.commit()
    return jsonify({'id': uni.id}), 201

@app.route('/universities/<int:id>', methods=['GET'])   # GET list of uni by id
def get_specific_unis(id):
    uni = University.query.get_or_404(id)
    uni_data = {
        "id": uni.id,
        "name": uni.name,
        "country": uni.country,
        "webpages": uni.webpages,
        "isBookmarked": uni.isBookmarked,
        "created": uni.created,
        "lastModified": uni.lastModified,
        "isActive": uni.isActive,
        "deletedAt": uni.deletedAt
    }

    return jsonify(uni_data)

@app.route('/universities/<id>', methods=['PUT'])   # Update uni details
def update_uni(id):
    uni = University.query.get_or_404(id) 
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    uni.name = data.get('name', uni.name)
    uni.country = data.get('country', uni.country)
    uni.webpages = data.get('webpages', uni.webpages)
    uni.isBookmarked = data.get('isBookmarked', uni.isBookmarked)
    uni.isActive = data.get('isActive', uni.isActive)

    uni.lastModified = datetime.datetime.now() 

    db.session.commit()

    return jsonify({'message': 'University updated successfully', 'id': uni.id}), 200

@app.route('/universities/<id>', methods=['DELETE'])    # DELETE a uni
def delete_uni(id):
    uni = University.query.get(id)
    if uni is None:
        return {"Error" : "404"}

    db.session.delete(uni)
    db.session.commit()

    return jsonify({'message': 'University deleted successfully', 'id': uni.id}), 200

@app.route('/universities/bookmark/<id>', methods=['POST'])     # POST Bookmark a uni
def bookmark_uni(id):
    uni = University.query.get_or_404(id)
    if uni.isBookmarked == True:
        uni.isBookmarked = False
    else:
        uni.isBookmarked = True

    uni.lastModified = datetime.datetime.now() 
    db.session.commit()

    if uni.isBookmarked == True:
        return jsonify({'message': 'University is bookmarked successfully', 'id': uni.id}), 200
    else:
        return jsonify({'message': 'University removed from bookmarked successfully', 'id': uni.id}), 200