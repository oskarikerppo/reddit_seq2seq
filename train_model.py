import comment_parser
import unicodedata
import numpy as np
import keras
from keras import Input, Model
from keras.layers import LSTM, Dense



#Get training data as pairs
comments, replies = comment_parser.main()

#Normalize
comments = [unicodedata.normalize('NFKD',c).encode('ascii','ignore') for c in comments]
replies = [unicodedata.normalize('NFKD',c).encode('ascii','ignore') for c in replies]

com_sentences = []
rep_sentences = []

com_chars = set()
rep_chars = set()

#Process comment and reply pairs
for i in range(len(comments)):
	comment = comments[i]
	reply = '\t' + replies[i] + '\n'

	com_sentences.append(comment)
	rep_sentences.append(reply)

	for ch in comment:
		if ch not in com_chars:
			com_chars.add(ch)

	for ch in reply:
		if ch not in rep_chars:
			rep_chars.add(ch)


tokenized_com_sentences = np.zeros(shape = (len(comments),len(max(comments, key=len)),len(com_chars)), dtype='float32')
tokenized_rep_sentences = np.zeros(shape = (len(replies),len(max(replies, key=len)),len(rep_chars)), dtype='float32')
target_data = np.zeros((len(replies),len(max(replies, key=len)),len(rep_chars)), dtype='float32')


#Vectorize sentences

for i in range(len(comments)):
	for k, ch in enumerate(comments[i]):
		tokenized_com_sentences[i, k, list(com_chars).index(ch)] = 1

	for k, ch in enumerate(replies[i]):
		tokenized_rep_sentences[i, k, list(rep_chars).index(ch)] = 1

	#decoder_target_data will be ahead by one timestep and will not include the start character
	if k > 0:
		target_data[i, k-1, list(rep_chars).index(ch)] = 1


#Encoder model
encoder_input = Input(shape = (None, len(com_chars)))
encoder_LSTM = LSTM(256, return_state = True)
encoder_outputs, encoder_h, encoder_c = encoder_LSTM(encoder_input)
encoder_states = [encoder_h, encoder_c]

print("Encoder model initialized!")

#Decoder model
decoder_input = Input(shape = (None, len(rep_chars)))
decoder_LSTM = LSTM(256,return_sequences=True, return_state=True)
decoder_out, _, _ = decoder_LSTM(decoder_input, initial_state=encoder_states)
decoder_dense = Dense(len(rep_chars), activation='softmax')
decoder_out = decoder_dense(decoder_out)

print("Decoder model initialized!")


#Train the model

model = Model(inputs=[encoder_input, decoder_input], outputs=[decoder_out])

#Run training

model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit(x=[tokenized_com_sentences, tokenized_rep_sentences],
			y = target_data,
			batch_size=64,
			epochs=50,
			verbose=2,
			validation_split=0.2)


#Encoder inference model
encoder_model_inf = Model(encoder_input, encoder_states)

#Decoder inference model
decoder_state_input_h = Input(shape=(256,))
decoder_state_input_c = Input(shape=(256,))
decoder_input_states = [decoder_state_input_h, decoder_state_input_c]

decoder_out, decoder_h, decoder_c = decoder_LSTM(decoder_input,initial_state=decoder_input_states)

decoder_states = [decoder_h, decoder_c]
decoder_out = decoder_dense(decoder_out)

decoder_model_inf = Model(inputs=[decoder_input] + decoder_input_states,
							outputs=[decoder_out] + decoder_states)



def decode_seq(inp_seq):

	#Initial states value comes from the encoder
	states_val = encoder_model_inf.predict(inp_seq)

	target_seq = np.zeros((1,1, len(rep_chars)))
	target_seq[0, 0, list(rep_chars).index('\t')] = 1

	translated_sent = ''
	stop_condition = False

	while not stop_condition:

		decoder_out, decoder_h, decoder_c = decoder_model_inf.predict(x=[target_seq] + states_val)

		max_val_index = np.argmax(decoder_out[0,-1,:])
		sampled_rep_char = list(rep_chars)[max_val_index]
		translated_sent += sampled_rep_char

		if (sampled_rep_char == '\n') or (len(translated_sent) > 250):
			stop_condition = True

		target_seq = np.zeros((1, 1, len(rep_chars)))
		target_seq[0, 0, max_val_index] = 1

		states_val = [decoder_h, decoder_c]

	return translated_sent


for seq_index in range(20):
	inp_seq = tokenized_com_sentences[seq_index: seq_index+1]
	translated_sent = decode_seq(inp_seq)
	print("---------------------------")
	print("Input sentence: ", com_sentences[seq_index])
	print("Output sentence: ", translated_sent)