from pymongo import MongoClient
import bcrypt

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']  # Collection for storing login details

# List of hardcoded users with their types (hospital, person, police)
users = [
    {
        'username': 'kims@gmal.com',
        'password': 'Hospital@123',
        'type': 'hospital'
    },
    {
        'username': 'karthik@gmail',
        'password': 'Karthik@123',
        'type': 'person'
    },
    {
        'username': 'ramana@gmail.com',
        'password': 'raman@123',
        'type': 'police'
    }
]

# Loop through the hardcoded users and insert them into the database
for user in users:
    # Hash the password
    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())

    # Insert user data into the MongoDB collection
    users_collection.insert_one({
        'username': user['username'],
        'password': hashed_password,
        'type': user['type']
    })

print("Hardcoded users have been added to the database!")
