import pickle
class LogEntry(object):
	def __init__(self, clientId, requestId, data, term):
		self._clientId = clientId
		self._requestId = requestId
		self._data = data
		self._term = term

	def __repr__(self):
		return "\nclientId: "+ str(self._clientId) + \
		"\nrequestId: " + str(self._requestId) + \
		"\ndata: " + str(self._data) + \
		"\nterm: " + str(self._term) + "\n "


class Log(object):
	def __init__(self, server_id):
		self._firstIndex = 0
		self._length = 1;
		self._entries = [LogEntry(-1, 0, None, 0), ]

	def __repr__(self):
		return "\nfirstIndex " + str(self._firstIndex) + \
				"\nlength " + str(self._length) + \
				"\nEntries" + str(self._entries)

	def push(self, value):
		self._length += 1
		print value, type(value)
		trans = LogEntry(value['_clientId'], value['_requestId'], value['_data'], value['_term'])
		self._entries.append(trans)

	def pop(self):
		self._length -= 1
		self._entries.pop()

	def shift(self):
		pass

	def slice(self, from1, to):
		return self._entries[from1:to]

# currentTerm = 23
# votedFor = 1
# log = Log(1)
def writeToPersistentStore():
	global currentTerm, votedFor, log
	dic = {"currentTerm": currentTerm, "votedFor": votedFor, "log": log }
	with open("checkpoint.pkl", "wb") as outFile:
		pickle.dump(dic, outFile, pickle.HIGHEST_PROTOCOL)
		# pickle.dump(log, outFile, pickle.HIGHEST_PROTOCOL)

def readFromPersistentStore():
	global currentTerm, votedFor, log
	with open("checkpoint.pkl", "rb") as inFile:
		newDic = pickle.load(inFile)
		currentTerm = newDic['currentTerm']
		votedFor = newDic['votedFor']
		log = newDic['log']
		# log = pickle.load(inFile)

def main():
	# writeToPersistentStore()
	readFromPersistentStore()
	print "\ncurrentTerm: " + str(currentTerm)
	print "\nvotedFor: "+ str(votedFor)
	print "\nlog: " + str(log)

if __name__=="__main__":
	main()
