# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask("SecretSanta")
# Configure flask-session to store data in cookies
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'bT!J12$wL@7&fA*8'  # Change this to a secure secret key

# Define your list of participants here
participants = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']

# Define a function to randomize Secret Santa assignments
# Set initial values as None if this is the first year
previous_assignments = {
    'Alice': None,
    'Bob': None,
    'Charlie': None,
    'David': None,
    'Eve': None,
    'Frank': None
}

# Function to randomize assignments with exclusions
def randomize_assignments(participants, previous_assignments):
    assignments = participants.copy()
    random.shuffle(assignments)
    
    # Ensure that no one gets the same assignment as last year
    for i in range(len(participants)):
        if previous_assignments[participants[i]] == assignments[i]:
            # Swap the assignment with someone else
            j = (i + 1) % len(participants)
            assignments[i], assignments[j] = assignments[j], assignments[i]
    
    return assignments

@app.route('/')
def index():
    # Check if a user is logged in
    if 'username' in session:
        return f"Welcome, {session['username']}! Click <a href='/secret-santa'>here</a> to see your Secret Santa assignment."
    return "Welcome to the Secret Santa application! Please log in below:<br>" + \
           "<form method='POST' action='/login'>" + \
           "<input type='text' name='username' placeholder='Enter your name'>" + \
           "<input type='submit' value='Log In'>" + \
           "</form>"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if username in participants:
        session['username'] = username
        return redirect(url_for('index'))
    return "Participant not found."

@app.route('/secret-santa')
def secret_santa():
    if 'username' in session:
        username = session['username']
        assignment = randomize_assignments(participants, previous_assignments)
        return f"Hello, {username}! Your Secret Santa assignment is: {assignment[participants.index(username)]}"
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





