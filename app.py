# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session, url_for
import random
import itertools
import json

app = Flask("SecretSanta")
# Configure flask-session to store data in cookies
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'bT!J12$wL@7&fA*8'  # Change this to a secure secret key

participants = ['Isabel', 'Raquel', 'Angel', 'Oscar', 'Tiama', 'Tioang', 'Tiaisa', 'Tioisi']

previous_assignments = {
    'Isabel': ['Tiama'],
    'Raquel': ['Tioisi'],
    'Angel': ['Tiaisa', 'Oscar'],
    'Oscar': ['Tioang', 'Tiaisa'],
    'Tiama': ['Oscar', 'Angel'],
    'Tioang': ['Raquel'],
    'Tiaisa': ['Isabel'],
    'Tioisi': ['Angel', 'Tioang']
}
assignment_file = 'assignment.json'

def get_valid_assignments(participants, previous_assignments):
    # Generate all possible permutations of participants
    all_permutations = itertools.permutations(participants)
    
    valid_permutations = []

    for perm in all_permutations:
        valid = True

        for participant, gift in zip(participants, perm):
            # Check if the participant is gifting to themselves
            if participant == gift:
                valid = False
                break

            # Check if the participant is gifting someone they've previously gifted
            if gift in previous_assignments.get(participant, []):
                valid = False
                break
        
        # Check if every recipient is unique in a permutation
        if len(set(perm)) != len(participants):
            valid = False

        # If the permutation passes all the checks, append it to the valid permutations list
        if valid:
            valid_permutations.append(perm)
    
    return valid_permutations

# Function to select a random valid assignment and save it to a file
def select_and_save_assignment(participants, previous_assignments):
    valid_permutations = get_valid_assignments(participants, previous_assignments)
    chosen_permutation = random.choice(valid_permutations)
    
    assignment = dict(zip(participants, chosen_permutation))
    
    with open(assignment_file, 'w') as f:
        json.dump(assignment, f)

# Function to load the assignment from the file
def load_assignment():
    try:
        with open(assignment_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


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
        assignment = load_assignment()
        if username in assignment:
            return f"Hello, {username}! Your Secret Santa assignment is: {assignment[username]}"
        else:
            return "Assignments have not been made yet. Please check back later."
    return redirect(url_for('index'))

@app.route('/generate-assignments', methods=['POST'])
def generate_assignments():
    select_and_save_assignment(participants, previous_assignments)
    return "Assignments have been generated and saved."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





