import nltk, numpy, tflearn, json, pickle, os
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer
#========== INITIALIZING VARIABLES =============
stemmer = LancasterStemmer()

working_dir = os.path.dirname(os.path.abspath(__file__))+'/'

model_save_name = 'test2.tflearn'
pickle_save_name = 'data.pickle'



intents_path = working_dir+'../intents/'

model = None
training_data = None
output_data = None
words_data = None
labels_data = None
raw_data = None


# ============ DATA PREPROCESSING / CLEANING ================
def data_combine():
	intents = []
	for file in os.listdir(intents_path):
		if '.json' in file:
			with open(intents_path+file) as f:
				contents = json.load(f)
				for i in contents['intents']:
					intents.append(i)
	return {'intents':intents}

def data_preprocessor():
	global training_data, output_data, words_data, labels_data, raw_data, pickle_save_name
	
	data = data_combine()

	try:
		with open(working_dir+pickle_save_name, 'rb') as f:
			words, labels, training, output = pickle.load(f)
	except:
		words = []
		labels = []
		docs_x = []
		docs_y = []

		for intent in data['intents']:
			for pattern in intent['patterns']:
				wrds = nltk.word_tokenize(pattern)
				words.extend(wrds)
				docs_x.append(wrds)
				docs_y.append(intent['tag'])

			if intent['tag'] not in labels:
				labels.append(intent['tag'])

		words = [stemmer.stem(w.lower()) for w in words if w != '?']
		words = sorted(list(set(words)))

		labels = sorted(labels)

		training = []
		output = []

		out_empty = [0 for _ in range(len(labels))]

		for x, doc in enumerate(docs_x):
			bag = []

			wrds = [stemmer.stem(w) for w in doc]

			for w in words:
				if w in wrds:
					bag.append(1)
				else:
					bag.append(0)

			output_row = out_empty[:]
			output_row[labels.index(docs_y[x])] = 1

			training.append(bag)
			output.append(output_row)

		training = numpy.array(training)
		output = numpy.array(output)

		with open(working_dir+pickle_save_name, 'wb') as f:
			pickle.dump((words, labels, training, output), f)

	training_data = training
	output_data = output
	words_data = words
	labels_data = labels
	raw_data = data

#========== NEURAL NETWORK ===============
def neural_net(Train):
	global model, model_save_name
	data_preprocessor()
	tf.reset_default_graph()

	net = tflearn.input_data(shape=[None, len(training_data[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(output_data[0]), activation='softmax')
	net = tflearn.regression(net)

	model = tflearn.DNN(net)

	if Train:
		model.fit(training_data, output_data, n_epoch=5000, batch_size=8, show_metric=True)
		model.save(working_dir+model_save_name)
		print('Model has been trained, program will now exit...')
		exit()
	else:
		model.load(working_dir+model_save_name)



def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[i] = 1

	return numpy.array(bag)

def predict_response(inp):
	response_json = None

	results = model.predict([bag_of_words(inp, words_data)])
	results_index = numpy.argmax(results)
	tag = labels_data[results_index]

	certainty = max(results[0]).tolist()

	for x in raw_data['intents']:
		if x['tag'] == tag:
			x['certainty'] = certainty
			response_json = x

	return response_json

#============ TRAIN FUNCTION ================
def train_ai():
	for file in os.listdir(working_dir):
		if pickle_save_name in file:
			os.remove(working_dir+file)
		if model_save_name in file:
			os.remove(working_dir+file)
		if file == 'checkpoint':
			os.remove(working_dir+file)
	neural_net(True)

#============ NORMAL START FUNCTION =============
def normal_start():
	neural_net(False)






