from flask import Flask, render_template, request, jsonify
import networkx as nx

# Initialize Flask app
app = Flask(__name__)

# Create Graph
G = nx.Graph()

# Define Users (Nodes) and Friendships (Edges)
users = ['A', 'B', 'C', 'D', 'E', 'F']
friendships = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('E', 'F')]

# Add nodes (users) and edges (friendships) to the graph
G.add_nodes_from(users)
G.add_edges_from(friendships)

# Function for Mutual Friends Recommendation
def mutual_friends(G, user):
    friends = set(G.neighbors(user))  # Get direct friends
    recommendations = {}

    for friend in friends:  # Loop through each direct friend
        for mutual in G.neighbors(friend):  # Get friends of the friend
            if mutual != user and mutual not in friends:  # Avoid duplicates
                recommendations[mutual] = recommendations.get(mutual, 0) + 1

    return sorted(recommendations, key=recommendations.get, reverse=True)  # Sort by highest mutual count

# Home route: Show a form to input the user's name
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation route: Get recommendations for the user
@app.route('/recommend', methods=['POST'])
def recommend():
    user = request.form['user']  # Get the username from the form
    if user not in G.nodes:
        return render_template('index.html', error="User not found.")
    
    recommendations = mutual_friends(G, user)
    return render_template('index.html', user=user, recommendations=recommendations)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
