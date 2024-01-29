from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.app_context().push()
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "verySecret"
app.config["CORS_SUPPORTS_CREDENTIALS"]=True 
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PATCH", "DELETE"]}})

connect_db(app)

@app.route('/')
def go_to_cupcakes_page():
    return render_template('cupcakes.html')


@app.route('/api/cupcakes/')
def get_data_about_cupcakes():
    all_cupcakes = Cupcake.query.all()
    #
    cupcakes_dict = [cupcake.to_dict() for cupcake in all_cupcakes]
    #
    dict_cupcakes = jsonify(cupcakes_dict)
    return render_template('show_cupcakes.html', cupcakes=dict_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_info_about_cupcake(id):
    cupcake = Cupcake.query.get(id)
    print(cupcake)
    #
    cupcake = cupcake.to_dict()
    #
    cupcake = jsonify(cupcake)
    return render_template('show_cupcake.html', cupcake=cupcake)


@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    #
    req = request.json
    cupcake = Cupcake(
        flavor = req['flavor'],
        size = req['size'],
        rating = req['rating'],
        image = req['image']
        )
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())
                  
 
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get(id)
    req = request.json
    cupcake.flavor = req['flavor']
    cupcake.size = req['size']
    cupcake.rating = req['rating']
    cupcake.image = req['image']
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())
    


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get(id)
    #
    db.session.delete(cupcake)
    db.session.commit()
    #
    return jsonify(message = 'Deleted')
