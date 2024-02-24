from flask_pymongo import PyMongo

mongo = PyMongo()

# Connect to the database
def get_db():
    return mongo.db

# Close the database connection when the app is closed
def close_db(exception):
    mongo.close()
