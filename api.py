from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configurarea bazei de date MySQL deja existentă
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://victor:quesadilla@localhost/api_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definirea modelelor pentru a accesa tabelele existente
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    google_id = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Community(db.Model):
    __tablename__ = 'Communities'
    community_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserCommunity(db.Model):
    __tablename__ = 'UserCommunities'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('Communities.community_id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inventory(db.Model):
    __tablename__ = 'Inventory'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.Enum('utensil', 'food'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    __tablename__ = 'Posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('Communities.community_id'), nullable=False)
    dish = db.Column(db.String(150), nullable=False)
    num_of_people = db.Column(db.Integer)
    hour = db.Column(db.Time)
    location = db.Column(db.String(255))
    status = db.Column(db.Enum('active', 'archived'), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserItem(db.Model):
    __tablename__ = 'UserItems'
    user_item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('Inventory.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Rutele API
# Crearea unui utilizator nou
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'], google_id=data.get('google_id'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Preluarea tuturor utilizatorilor
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"user_id": u.user_id, "name": u.name, "email": u.email} for u in users])

# Crearea unei comunități noi
@app.route('/communities', methods=['POST'])
def create_community():
    data = request.json
    new_community = Community(name=data['name'], description=data.get('description'))
    db.session.add(new_community)
    db.session.commit()
    return jsonify({"message": "Community created successfully"}), 201

# Afișarea tuturor comunităților
@app.route('/communities', methods=['GET'])
def get_communities():
    communities = Community.query.all()
    return jsonify([{"community_id": c.community_id, "name": c.name, "description": c.description} for c in communities])

# Crearea unui post nou
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    new_post = Post(
        user_id=data['user_id'],
        community_id=data['community_id'],
        dish=data['dish'],
        num_of_people=data.get('num_of_people'),
        hour=data.get('hour'),
        location=data.get('location'),
        status=data.get('status', 'active')
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201

# Preluarea tuturor posturilor
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {
            "post_id": p.post_id,
            "user_id": p.user_id,
            "community_id": p.community_id,
            "dish": p.dish,
            "num_of_people": p.num_of_people,
            "hour": str(p.hour),
            "location": p.location,
            "status": p.status
        } for p in posts
    ])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
