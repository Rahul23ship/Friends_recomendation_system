from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import networkx as nx

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    interests = db.Column(db.Text)
    description = db.Column(db.Text)

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create graph for recommendation system
G = nx.Graph()

def build_graph_from_db():
    G.clear()
    users = User.query.all()
    for user in users:
        G.add_node(user.username)

    friendships = Friendship.query.all()
    for f in friendships:
        user1 = User.query.get(f.user_id)
        user2 = User.query.get(f.friend_id)
        if user1 and user2:
            G.add_edge(user1.username, user2.username)

def interest_similarity(user_interests, other_interests):
    set_user = set(i.strip().lower() for i in user_interests.split(',')) if user_interests else set()
    set_other = set(i.strip().lower() for i in other_interests.split(',')) if other_interests else set()
    if not set_user or not set_other:
        return 0
    intersection = set_user & set_other
    union = set_user | set_other
    return len(intersection) / len(union) if union else 0

def combined_recommendations(G, user):
    if user not in G.nodes:
        return []

    user_obj = User.query.filter_by(username=user).first()
    user_friends = set(G.neighbors(user))
    user_interests = user_obj.interests if user_obj else ""

    scores = {}

    if user_friends:
        for other_user in G.nodes:
            if other_user == user or other_user in user_friends:
                continue

            other_obj = User.query.filter_by(username=other_user).first()
            other_friends = set(G.neighbors(other_user))
            other_interests = other_obj.interests if other_obj else ""

            intersection = user_friends & other_friends
            union = user_friends | other_friends
            friend_score = (len(intersection) / len(union)) if union else 0

            interest_score = interest_similarity(user_interests, other_interests)
            combined_score = 0.6 * friend_score + 0.4 * interest_score

            if combined_score > 0:
                scores[other_user] = combined_score
    else:
        for other_user in G.nodes:
            if other_user == user:
                continue
            other_obj = User.query.filter_by(username=other_user).first()
            other_interests = other_obj.interests if other_obj else ""

            interest_score = interest_similarity(user_interests, other_interests)
            if interest_score > 0:
                scores[other_user] = interest_score

        if not scores:
            popularity = {u: len(list(G.neighbors(u))) for u in G.nodes if u != user}
            sorted_popular = sorted(popularity.items(), key=lambda x: x[1], reverse=True)
            return [(u, 100.0) for u, _ in sorted_popular[:5]]

    max_score = max(scores.values()) if scores else 1
    sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(username, round((score / max_score) * 100, 2)) for username, score in sorted_users]

# Routes

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user = request.form['user']
    all_users = User.query.all()
    if not User.query.filter_by(username=user).first():
        return render_template("index.html", error="User not found", user=user, users=all_users)

    recommendations = combined_recommendations(G, user)
    return render_template("index.html", user=user, recommendations=recommendations, users=all_users)

@app.route('/add_friend_from_recommendation', methods=['POST'])
def add_friend_from_recommendation():
    user_name = request.form.get('user')
    friend_name = request.form.get('friend')

    user = User.query.filter_by(username=user_name).first()
    friend = User.query.filter_by(username=friend_name).first()

    if not user or not friend or user == friend:
        return redirect(url_for('index'))

    existing = Friendship.query.filter(
        ((Friendship.user_id == user.id) & (Friendship.friend_id == friend.id)) |
        ((Friendship.user_id == friend.id) & (Friendship.friend_id == user.id))
    ).first()

    if not existing:
        db.session.add(Friendship(user_id=user.id, friend_id=friend.id))
        db.session.commit()
        build_graph_from_db()

    return redirect(url_for('recommend'), code=307)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['Name']
        interests = request.form.get('Interests')
        description = request.form.get('Description')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('add.html', error="User already exists.")

        new_user = User(username=username, interests=interests, description=description)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('add_friends', username=username))

    return render_template('add.html')

@app.route('/add_friends', methods=['GET', 'POST'])
def add_friends():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        friends_list = request.form.getlist('friends')
        if not friends_list:
            return render_template('add_friends.html', username=username, users=User.query.all(), error="Please select at least one friend.")

        added_friends = []
        for friend_username in friends_list:
            friend = User.query.filter_by(username=friend_username).first()
            if friend and friend != user:
                exists = Friendship.query.filter(
                    ((Friendship.user_id == user.id) & (Friendship.friend_id == friend.id)) |
                    ((Friendship.user_id == friend.id) & (Friendship.friend_id == user.id))
                ).first()
                if not exists:
                    db.session.add(Friendship(user_id=user.id, friend_id=friend.id))
                    added_friends.append(friend.username)

        db.session.commit()
        build_graph_from_db()
        message = f"Added friends: {', '.join(added_friends)}" if added_friends else "No new friends added."
        return render_template('add_friends.html', username=username, users=User.query.all(), message=message)

    return render_template('add_friends.html', username=username, users=User.query.all())

# Main execution
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        build_graph_from_db()
    app.run(debug=True)
