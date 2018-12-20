import pickle
import os

def writeToPersistentStore(currentTerm, votedFor, log, lastApplied):
	dic = {"currentTerm": currentTerm
	, "votedFor": votedFor
	, "log": log
	, 'lastApplied':lastApplied }
	with open("checkpoint.pkl", "wb") as outFile:
		pickle.dump(dic, outFile, pickle.HIGHEST_PROTOCOL)
		# pickle.dump(log, outFile, pickle.HIGHEST_PROTOCOL)

def readFromPersistentStore():
	newDict = {}
	if os.path.exists("checkpoint.pkl") == False:
		return None
	with open("checkpoint.pkl", "rb") as inFile:
		newDict = pickle.load(inFile)
		currentTerm = newDict['currentTerm']
		votedFor = newDict['votedFor']
		log = newDict['log']
		lastApplied = newDict['lastApplied']
	return currentTerm, votedFor, log, lastApplied

def write_to_file(msg):
	if msg is not None:
		clientId = msg['clientId']
		if os.path.isdir(clientId) == False:
			os.makedirs(clientId)
		path = clientId+"/"+msg['sourceId']
		with open(path, "a") as myfile:
			myfile.write("%s"%(msg['fileData']))
