from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB Atlas using environment variable
client = MongoClient(os.getenv('MONGODB_URI'))

# Access your database
db = client['hospitals']

# Access your collection
collection = db['name']

# Query all documents
print("All facilities:")
all_facilities = collection.find()
for facility in all_facilities:
    print(facility)
    print()

# Query specific facility by ID
print("\nFacility with ID 0:")
facility = collection.find_one({'id': 0})
print(facility)

# Query by name
print("\nSaint Michael's Medical Center:")
facility = collection.find_one({'name': "Saint Michael's Medical Center"})
print(facility)

# Query by city
print("\nAll Newark facilities:")
newark_facilities = collection.find({'address.city': 'Newark'})
for facility in newark_facilities:
    print(facility['name'])

# Close connection
client.close()
