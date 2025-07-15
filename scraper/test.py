from os.path import relpath
import json


rel_path = relpath("C:/Users/nicho/Documents/Programming/JobScraper-2/creds/cloud-demo-47f8d-firebase-adminsdk-fbsvc-1d32af7619.json")

print(rel_path)
f = open(rel_path, "r")

#TODO: Run relpath in program, works as creds/thingy

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
#print(data)

# Closing file
f.close()