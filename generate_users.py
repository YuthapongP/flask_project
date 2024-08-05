import bcrypt
import json




# List of mock usernames and passwords
users_data = [
    ("alice_smith", "passwordAlice123"),
    ("bob_johnson", "passwordBob123"),
    ("carol_davis", "passwordCarol123"),
    ("dave_miller", "passwordDave123"),
    ("eve_wilson", "passwordEve123"),
    ("frank_jones", "passwordFrank123"),
    ("grace_brown", "passwordGrace123"),
    ("hank_taylor", "passwordHank123"),
    ("iris_anderson", "passwordIris123"),
    ("jack_clark", "passwordJack123"),
]


users = {}

for username, password in users_data:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed.decode('utf-8')

# Save the users dictionary to a file
with open('mock_users.py', 'w') as file:
    file.write('users = ')
    json.dump(users, file, indent=4)