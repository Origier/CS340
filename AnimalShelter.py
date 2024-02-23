from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS, HOST, PORT, DB, COL):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    # Create method accepts a dictionary object containing JSON style information
    # It ensures that the data is valid and writes to the database
    # It returns True or False if the data was able to be successfully wrote
    def create(self, data):
        if data is not None:
            try:
                # Setting the insert result to help determine if the write was successful or not
                insert_result = self.collection.insert_one(data)  # data should be dictionary  
                return insert_result.acknowledged
            except TypeError:
                raise TypeError("Data must be a dictionary")
		
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Read method accepts a key value pair to indicate what data to filter the 
    # database for, it returns a list containing all of the results from the read
    # The find_many value indcates if you wish to find every entry that matches
    # the provided key value or just one entry
    def read(self, key_value, find_many = True):
        # Ensure that find_value and update_value exist
        if key_value is None:
            raise Exception("The key_value must be a dictionary")
            
        if find_many:
            # Attempt to find - expecting an error if the data type is wrong
            try:
                # Fetching the list from the data base
                find_list = list(self.collection.find(key_value))
                return find_list
            except:
                raise TypeError("The key_value must be a dictionary")
        else:
            try:
                # Fetching the list from the data base
                find_list = self.collection.find_one(key_value)
                return [find_list]
            except:
                raise TypeError("The key_value must be a dictionary")
        
            
    # Update method accepts two key value pairs as well as a boolean value for single or many
    # The method will update the database for anything that matches the dictionary of find_value
    # and will update them with the update_value. It will update only one if update_many
    # is false - otherwise will update all entries.
    # Returns the number of entries updated
    def update(self, find_value, update_value, update_many = True):
        # Ensure that find_value and update_value exist
        if find_value is None or update_value is None:
            raise Exception("Both the find_value and update_value must be a dictionary")
            
        if update_many:
            # Attempt to update - expecting an error if the data type is wrong
            try:
                updated = self.collection.update_many(find_value, update_value)
                return updated.modified_count
            except:
                raise TypeError("find_value and update_value must be dictionaries")
        else:
            try:
                updated = self.collection.update_one(find_value, update_value)
                return updated.modified_count
            except:
                raise TypeError("find_value and update_value must be dictionaries")
    
    # Delete method accepts a key value pair for the documents to be found and 
    # deleted from the database. It will only delete the first one if delete_many
    # is set to false, otherwise it will delete every instance
    # Returns the number of documents deleted this way
    def delete(self, delete_value, delete_many = True):
        # Ensuring the delete value exists
        if delete_value is None:
            raise Exception("delete_value must be a dictionary value")
            
        if delete_many:
            # Attempt to delete - expecting an error if the data type is wrong
            try:
                deleted = self.collection.delete_many(delete_value)
                return deleted.deleted_count
            except:
                raise TypeError("delete_value must be a dictionary value")
        else:
            try:
                deleted = self.collection.delete_one(delete_value)
                return deleted.deleted_count
            except:
                raise TypeError("delete_value must be a dictionary value")
        
        